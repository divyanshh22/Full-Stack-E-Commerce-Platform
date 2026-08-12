from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Category, Item, OrderItem


def make_category():
    return Category.objects.create(
        title="T-Shirts",
        slug="tshirts",
        description="Cotton tees",
        image=SimpleUploadedFile("cat.png", b"png", content_type="image/png"),
    )


def make_item(category):
    return Item.objects.create(
        title="Basic Tee",
        price=19.99,
        category=category,
        label="N",
        slug="basic-tee",
        stock_no="T-100",
        description_short="A plain cotton tee",
        description_long="A comfortable everyday cotton tee.",
        image=SimpleUploadedFile("tee.png", b"png", content_type="image/png"),
    )


class AddToCartTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="testpass123")
        self.client.force_login(self.user)
        self.item = make_item(make_category())
        self.url = reverse("core:add-to-cart", kwargs={"slug": self.item.slug})

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=" + self.url,
            fetch_redirect_response=False,
        )

    def test_missing_size_and_color_is_rejected(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("core:product", kwargs={"slug": self.item.slug}))
        self.assertFalse(OrderItem.objects.filter(user=self.user).exists())
        followed = self.client.get(
            reverse("core:product", kwargs={"slug": self.item.slug}))
        self.assertContains(followed, "Please select a size and color")

    def test_only_size_is_rejected(self):
        response = self.client.get(self.url, {"size": "M"})
        self.assertRedirects(
            response, reverse("core:product", kwargs={"slug": self.item.slug}))
        self.assertFalse(OrderItem.objects.filter(user=self.user).exists())

    def test_size_and_color_creates_order_item(self):
        self.client.get(self.url, {"size": "M", "color": "Black"})
        order_item = OrderItem.objects.get(user=self.user, item=self.item)
        self.assertEqual(order_item.size, "M")
        self.assertEqual(order_item.color, "Black")
        self.assertEqual(order_item.quantity, 1)

    def test_same_variant_increments_quantity(self):
        self.client.get(self.url, {"size": "M", "color": "Black"})
        self.client.get(self.url, {"size": "M", "color": "Black"})
        self.assertEqual(
            OrderItem.objects.filter(user=self.user, item=self.item).count(), 1)
        order_item = OrderItem.objects.get(user=self.user, item=self.item)
        self.assertEqual(order_item.quantity, 2)

    def test_different_variants_create_separate_items(self):
        self.client.get(self.url, {"size": "M", "color": "Black"})
        self.client.get(self.url, {"size": "L", "color": "Blue"})
        self.assertEqual(
            OrderItem.objects.filter(user=self.user, item=self.item).count(), 2)
