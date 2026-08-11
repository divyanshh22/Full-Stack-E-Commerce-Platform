import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Category, Item

CATEGORY_IMAGES = [
    "categories/shirts-and-jeans.jpg",
    "categories/t-shirts.jpg",
    "categories/skirts.jpg",
    "categories/hoodies-and-sweatshirts.jpg",
]
ITEM_IMAGES = [
    "item-01.webp", "item-02.webp", "item-03.webp", "item-04.webp",
    "item-05.webp", "item-06.webp", "item-07.webp", "item-08.webp",
    "item-09.webp", "item-10.webp", "item-11.webp", "item-12.webp",
]
PRODUCT_IMAGES = {
    "oxford-shirt": "products/oxford-shirt.jpg",
    "linen-shirt": "products/linen-shirt.jpg",
    "denim-shirt": "products/denim-shirt.jpg",
    "chambray-shirt": "products/chambray-shirt.jpg",
    "flannel-shirt": "products/flannel-shirt.jpg",
    "striped-shirt": "products/striped-shirt.jpg",
    "poplin-shirt": "products/poplin-shirt.jpg",
    "check-shirt": "products/check-shirt.jpg",
    "classic-cotton-tee": "products/classic-cotton-tee.jpg",
    "v-neck-tee": "products/v-neck-tee.jpg",
    "graphic-tee": "products/graphic-tee.jpg",
    "polo-tee": "products/polo-tee.jpg",
    "boxy-fit-tee": "products/boxy-fit-tee.jpg",
    "striped-tee": "products/striped-tee.jpg",
    "raglan-tee": "products/raglan-tee.jpg",
    "slim-fit-tee": "products/slim-fit-tee.jpg",
    "pleated-skirt": "products/pleated-skirt.jpg",
    "denim-skirt": "products/denim-skirt.jpg",
    "midi-skirt": "products/midi-skirt.jpg",
    "mini-skirt": "products/mini-skirt.jpg",
    "wrap-skirt": "products/wrap-skirt.jpg",
    "a-line-skirt": "products/a-line-skirt.jpg",
    "tulle-skirt": "products/tulle-skirt.jpg",
    "zip-hoodie": "products/zip-hoodie.jpg",
    "pullover-hoodie": "products/pullover-hoodie.jpg",
    "fleece-hoodie": "products/fleece-hoodie.jpg",
    "oversized-hoodie": "products/oversized-hoodie.jpg",
    "graphic-sweatshirt": "products/graphic-sweatshirt.jpg",
    "crewneck-sweatshirt": "products/crewneck-sweatshirt.jpg",
    "hooded-sweatshirt": "products/hooded-sweatshirt.jpg",
}

# (title, slug, description, image)
CATEGORIES = [
    ("Shirts and Jeans", "shirts-and-jeans",
     "Sharp, crisp and office-ready shirts and everyday jeans.",
     CATEGORY_IMAGES[0]),
    ("T-Shirts", "t-shirts",
     "Comfortable everyday tees in classic and modern fits.",
     CATEGORY_IMAGES[1]),
    ("Skirts", "skirts",
     "Flowy, structured and everything in between for your wardrobe.",
     CATEGORY_IMAGES[2]),
    ("Hoodies & Sweatshirts", "hoodies-and-sweatshirts",
     "Cozy hoodies and sweatshirts for chill days and cold nights.",
     CATEGORY_IMAGES[3]),
]

# (title, price_inr, discount_inr, category_slug, label, stock, short, long)
PRODUCTS = [
    ("Oxford Shirt", 2299, 1799, "shirts-and-jeans", "S", "SH001",
     "Classic Oxford weave shirt",
     "A timeless Oxford cotton shirt with a regular fit, button-down collar and chest pocket. Dress it up or keep it casual."),
    ("Linen Shirt", 2499, None, "shirts-and-jeans", "N", "SH002",
     "Breathable summer linen shirt",
     "Lightweight pure linen shirt that keeps you cool in the summer heat. Relaxed fit with natural texture."),
    ("Denim Shirt", 2999, 2399, "shirts-and-jeans", "P", "SH003",
     "Everyday denim shirt",
     "Rugged mid-weight denim shirt with a soft wash. Pairs perfectly with chinos or jeans."),
    ("Chambray Shirt", 1999, None, "shirts-and-jeans", "N", "SH004",
     "Soft chambray everyday shirt",
     "Soft, garment-washed chambray with a tailored silhouette. A wardrobe staple that goes with anything."),
    ("Flannel Shirt", 2599, 1999, "shirts-and-jeans", "S", "SH005",
     "Warm brushed flannel shirt",
     "Brushed cotton flannel with a classic plaid pattern. Ideal for layering in cooler months."),
    ("Striped Shirt", 2199, None, "shirts-and-jeans", "N", "SH006",
     "Fine stripe poplin shirt",
     "Crisp poplin with fine vertical stripes. Modern collar and a slim, clean fit."),
    ("Poplin Shirt", 2199, 1699, "shirts-and-jeans", "P", "SH007",
     "Smooth poplin office shirt",
     "Smooth, wrinkle-resistant poplin in a sharp regular fit. A reliable choice for the office."),
    ("Check Shirt", 2399, None, "shirts-and-jeans", "N", "SH008",
     "Casual checked shirt",
     "Relaxed checked shirt in soft brushed cotton. Button-up or wear open over a tee."),
    ("Classic Cotton Tee", 999, 749, "t-shirts", "S", "TS001",
     "Soft staple cotton tee",
     "Heavyweight cotton tee with a classic crew neck. Pre-shrunk and built to last wash after wash."),
    ("V-Neck Tee", 899, None, "t-shirts", "N", "TS002",
     "Everyday v-neck tee",
     "Comfortable v-neck tee in soft combed cotton. A clean silhouette that works under jackets."),
    ("Graphic Tee", 1199, 899, "t-shirts", "P", "TS003",
     "Bold printed graphic tee",
     "Street-style graphic print on a heavyweight blank. Boxy, comfortable and statement-making."),
    ("Polo Tee", 1499, None, "t-shirts", "N", "TS004",
     "Two-button cotton polo",
     "Classic pique polo with a two-button placket. Smart enough for the weekend dress code."),
    ("Boxy Fit Tee", 1099, 849, "t-shirts", "S", "TS005",
     "Oversized boxy fit tee",
     "Relaxed boxy silhouette in mid-weight jersey. The modern laid-back essential."),
    ("Striped Tee", 999, None, "t-shirts", "N", "TS006",
     "Mariner striped tee",
     "Nautical stripes on soft jersey cotton. A bright, easy pick for summer days."),
    ("Raglan Tee", 1199, 949, "t-shirts", "P", "TS007",
     "Baseball raglan tee",
     "Retro baseball raglan with contrasting sleeves. Sporty styling in soft cotton."),
    ("Slim Fit Tee", 999, None, "t-shirts", "N", "TS008",
     "Sleek slim fit tee",
     "Streamlined slim-fit tee with a curved hem. Layers neatly or wears great on its own."),
    ("Pleated Skirt", 1999, 1499, "skirts", "S", "SK001",
     "Flowing pleated skirt",
     "Graceful pleats that move with you, finished with an elastic waistband. Midi length for all-day comfort."),
    ("Denim Skirt", 1799, None, "skirts", "N", "SK002",
     "Classic denim skirt",
     "Structured denim skirt with a button fly and five-pocket detailing. A timeless casual pick."),
    ("Midi Skirt", 2199, 1699, "skirts", "P", "SK003",
     "Elegant midi skirt",
     "Flattering A-line midi with a smooth drape and back zip. Effortless from desk to dinner."),
    ("Mini Skirt", 1599, None, "skirts", "N", "SK004",
     "Chic pleated mini skirt",
     "Playful pleated mini with a high rise. Pairs beautifully with tees and sweaters."),
    ("Wrap Skirt", 1899, 1399, "skirts", "S", "SK005",
     "Adjustable wrap skirt",
     "Wraparound skirt with an adjustable tie waist. Lightweight fabric with a flattering fall."),
    ("A-Line Skirt", 1799, None, "skirts", "N", "SK006",
     "Soft A-line skirt",
     "Easy A-line silhouette in soft stretch fabric. Comfortable waistband and knee length."),
    ("Tulle Skirt", 2499, 1899, "skirts", "P", "SK007",
     "Dreamy tulle skirt",
     "Layer upon layer of soft tulle for a floaty, romantic look. Fully lined with a satin waistband."),
    ("Zip Hoodie", 2599, 1999, "hoodies-and-sweatshirts", "S", "HS001",
     "Classic zip-up hoodie",
     "Full-zip fleece hoodie with front pockets and a drawstring hood. Mid-weight warmth for layering."),
    ("Pullover Hoodie", 2399, None, "hoodies-and-sweatshirts", "N", "HS002",
     "Comfy pullover hoodie",
     "Brushed-back fleece pullover with a hood and kangaroo pocket. Your go-to cozy layer."),
    ("Fleece Hoodie", 2799, 2199, "hoodies-and-sweatshirts", "P", "HS003",
     "Warm fleece hoodie",
     "Thick fleece-lined hoodie built for cold days. Raglan sleeves and a soft brushed interior."),
    ("Oversized Hoodie", 2699, None, "hoodies-and-sweatshirts", "N", "HS004",
     "Trendy oversized hoodie",
     "Relaxed oversized fit with dropped shoulders. Heavy cotton fleece for a premium feel."),
    ("Graphic Sweatshirt", 2299, 1799, "hoodies-and-sweatshirts", "S", "HS005",
     "Printed crew sweatshirt",
     "Crewneck sweatshirt with a front print. Mid-weight fleece that holds its shape."),
    ("Crewneck Sweatshirt", 2199, None, "hoodies-and-sweatshirts", "N", "HS006",
     "Everyday crewneck sweatshirt",
     "Classic crewneck in brushed-back fleece. Ribbed cuffs and hem keep the fit clean."),
    ("Hooded Sweatshirt", 2499, 1899, "hoodies-and-sweatshirts", "P", "HS007",
     "Hooded pullover sweatshirt",
     "A warm hooded sweatshirt with an adjustable drawstring. Soft interior and roomy fit."),
]

LEGACY_CATEGORY_SLUGS = {
    "shirts-and-blouses": "shirts-and-jeans",
}


class Command(BaseCommand):
    help = "Seed the database with sample categories and products (idempotent)."

    def handle(self, *args, **options):
        src_dir = os.path.join(settings.BASE_DIR, "static_in_env", "images")
        media_root = settings.MEDIA_ROOT

        def ensure_media(name):
            src = os.path.join(src_dir, name)
            dst = os.path.join(media_root, name)
            if os.path.exists(src) and not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            return name

        for legacy, new in LEGACY_CATEGORY_SLUGS.items():
            Category.objects.filter(slug=legacy).update(slug=new)

        cats = {}
        for title, slug, desc, img in CATEGORIES:
            ensure_media(img)
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults=dict(title=title, description=desc,
                              image=img, is_active=True),
            )
            cat.title = title
            cat.description = desc
            cat.image = img
            cat.is_active = True
            cat.save()
            cats[slug] = cat

        created = 0
        updated = 0
        for i, (title, price, discount, cat_slug, label, stock, short, long) in enumerate(PRODUCTS):
            slug = title.lower().replace(" & ", " ").replace(" ", "-")
            img = ensure_media(PRODUCT_IMAGES.get(slug, ITEM_IMAGES[i % len(ITEM_IMAGES)]))
            item, was_created = Item.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    title=title, price=price, discount_price=discount,
                    category=cats[cat_slug], label=label, stock_no=stock,
                    description_short=short, description_long=long,
                    image=img, is_active=True,
                ),
            )
            if was_created:
                created += 1
            else:
                dirty = False
                for field, value in [
                    ("title", title), ("price", price),
                    ("discount_price", discount),
                    ("category", cats[cat_slug]), ("label", label),
                    ("stock_no", stock), ("description_short", short),
                    ("description_long", long), ("image", img),
                    ("is_active", True),
                ]:
                    if getattr(item, field) != value:
                        setattr(item, field, value)
                        dirty = True
                if dirty:
                    item.save()
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Item.objects.count()} products across "
            f"{Category.objects.count()} categories "
            f"(created: {created}, updated: {updated})."
        ))
