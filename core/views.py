from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category

import random
import string
import stripe

try:
    from stripe import errors as stripe_errors
except ImportError:  # older stripe versions expose exceptions under stripe.error
    stripe_errors = stripe.error

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def get_active_order(user):
    """Return the active (unpaid) order for a user or None."""
    qs = Order.objects.filter(user=user, ordered=False)
    return qs.first() if qs.exists() else None


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = get_active_order(self.request.user)
        if not order:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = get_active_order(self.request.user)
        if not order:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")

        if not order.items.exists():
            messages.warning(self.request, "Your cart is empty")
            return redirect("core:order-summary")

        token = self.request.POST.get('stripeToken')
        if not token:
            messages.error(self.request, "Payment token is missing")
            return redirect("core:payment", payment_option='stripe')

        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Order was successful")
            return redirect("/")

        except stripe_errors.CardError as e:
            # Since it's a decline, stripe_errors.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, err.get('message', "Card was declined"))
            return redirect("core:payment", payment_option='stripe')

        except stripe_errors.RateLimitError:
            messages.error(self.request, "Too many requests made to the API too quickly")
            return redirect("core:payment", payment_option='stripe')

        except stripe_errors.InvalidRequestError:
            messages.error(self.request, "Invalid parameters were supplied to Stripe's API")
            return redirect("core:payment", payment_option='stripe')

        except stripe_errors.AuthenticationError:
            messages.error(self.request, "Authentication with Stripe's API failed")
            return redirect("core:payment", payment_option='stripe')

        except stripe_errors.APIConnectionError:
            messages.error(self.request, "Network communication with Stripe failed")
            return redirect("core:payment", payment_option='stripe')

        except stripe_errors.StripeError:
            messages.error(self.request, "Something went wrong with the payment")
            return redirect("core:payment", payment_option='stripe')

        except Exception:
            messages.error(self.request, "A serious error occurred")
            return redirect("core:payment", payment_option='stripe')


class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = get_active_order(self.request.user)
        if not order:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")
        context = {
            'object': order
        }
        return render(self.request, 'order_summary.html', context)


class ShopView(ListView):
    model = Item
    queryset = Item.objects.filter(is_active=True).order_by('id')
    paginate_by = 30
    template_name = "shop.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related = Item.objects.filter(
            category=self.object.category, is_active=True
        ).exclude(pk=self.object.pk)[:4]
        context['related_items'] = related
        return context


class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = get_active_order(self.request.user)
        if not order:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")
        form = CheckoutForm()
        context = {
            'form': form,
            'couponform': CouponForm(),
            'order': order,
            'DISPLAY_COUPON_FORM': True
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = get_active_order(self.request.user)
        if not order:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")

        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip')
            payment_option = form.cleaned_data.get('payment_option')

            billing_address = BillingAddress(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip_code,
                address_type='B'
            )
            billing_address.save()
            order.billing_address = billing_address
            order.save()

            if payment_option == 'S':
                return redirect('core:payment', payment_option='stripe')
            elif payment_option == 'P':
                return redirect('core:payment', payment_option='paypal')
            else:
                messages.warning(self.request, "Invalid payment option selected")
                return redirect('core:checkout')

        messages.error(self.request, "Please fix the errors in the form below")
        context = {
            'form': form,
            'couponform': CouponForm(),
            'order': order,
            'DISPLAY_COUPON_FORM': True
        }
        return render(self.request, "checkout.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    size = (request.GET.get('size') or request.POST.get('size') or '').strip()
    color = (request.GET.get('color') or request.POST.get('color') or '').strip()
    if not size or not color:
        messages.error(
            request,
            "Please select a size and color before adding to cart."
        )
        return redirect("core:product", slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        size=size,
        color=color,
    )
    order = get_active_order(request.user)
    if order:
        if order.items.filter(pk=order_item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    size = request.GET.get('size') or request.POST.get('size')
    color = request.GET.get('color') or request.POST.get('color')
    order = get_active_order(request.user)
    if not order:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)
    qs = order.items.filter(item=item)
    if size:
        qs = qs.filter(size=size)
    if color:
        qs = qs.filter(color=color)
    if qs.exists():
        order.items.remove(qs.first())
        messages.info(request, "Item was removed from your cart.")
    else:
        messages.info(request, "Item was not in your cart.")
    return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    size = request.GET.get('size') or request.POST.get('size')
    color = request.GET.get('color') or request.POST.get('color')
    order = get_active_order(request.user)
    if not order:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)
    qs = order.items.filter(item=item)
    if size:
        qs = qs.filter(size=size)
    if color:
        qs = qs.filter(color=color)
    if qs.exists():
        order_item = qs.first()
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order.items.remove(order_item)
        messages.info(request, "This item quantity was updated.")
    else:
        messages.info(request, "Item was not in your cart.")
    return redirect("core:order-summary")


def get_coupon(request, code):
    try:
        return Coupon.objects.get(code=code)
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        raise


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            order = get_active_order(self.request.user)
            if not order:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:shop")
            try:
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
            except ObjectDoesNotExist:
                pass
            return redirect("core:checkout")
        return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")
        return render(self.request, "request_refund.html", {'form': form})
