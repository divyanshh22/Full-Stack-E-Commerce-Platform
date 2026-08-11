from .models import Category, Slide


def shop_context(request):
    return {
        'all_categories': Category.objects.filter(is_active=True).order_by('title'),
        'all_slides': Slide.objects.filter(is_active=True).order_by('pk'),
    }
