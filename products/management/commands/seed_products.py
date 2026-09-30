"""
Management command to seed demo cosmetics products.
Run: python manage.py seed_products
Safe to run multiple times - skips duplicates.
"""

from django.core.management.base import BaseCommand
from products.models import Category, Product


SEED_DATA = {
    "Makeup": [
        {
            "name": "Luminous Foundation",
            "description": "Buildable full-coverage foundation with a natural satin finish.",
            "price": "599.00",
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Flawless Concealer",
            "description": "Full-coverage concealer that hides dark circles and blemishes.",
            "price": "349.00",
            "stock": 35,
            "image_url": "https://images.unsplash.com/photo-1631730359585-38a4935cbec4?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Rosy Blush",
            "description": "Silky smooth blush in a flattering rose tone for a natural flush.",
            "price": "299.00",
            "stock": 30,
            "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Makeup Brush Set",
            "description": "Professional 12-piece brush set with soft synthetic bristles.",
            "price": "799.00",
            "stock": 20,
            "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Skincare": [
        {
            "name": "Vitamin C Serum",
            "description": "Brightening serum with 20% Vitamin C for a radiant, even skin tone.",
            "price": "899.00",
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Hydrating Moisturizer",
            "description": "Rich yet lightweight moisturizer with hyaluronic acid for deep hydration.",
            "price": "649.00",
            "stock": 30,
            "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Gentle Face Cleanser",
            "description": "Mild foaming cleanser that removes impurities without stripping moisture.",
            "price": "399.00",
            "stock": 45,
            "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Sunscreen SPF 50",
            "description": "Lightweight, non-greasy sunscreen with broad spectrum SPF 50 protection.",
            "price": "499.00",
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Lipsticks": [
        {
            "name": "Velvet Lip Color",
            "description": "Long-lasting velvet lipstick in a rich, bold shade.",
            "price": "449.00",
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Nude Lipstick",
            "description": "Creamy nude lipstick that complements every skin tone beautifully.",
            "price": "399.00",
            "stock": 45,
            "image_url": "https://images.unsplash.com/photo-1631214499101-c1d98de6e02e?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Glossy Lip Tint",
            "description": "Sheer glossy tint for plump, luminous lips all day long.",
            "price": "299.00",
            "stock": 55,
            "image_url": "https://images.unsplash.com/photo-1559599101-f09722fb4948?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Berry Matte Lipstick",
            "description": "Deep berry matte finish for a bold, dramatic statement look.",
            "price": "479.00",
            "stock": 38,
            "image_url": "https://images.unsplash.com/photo-1612817288484-6f916006741a?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Eye Makeup": [
        {
            "name": "Waterproof Eyeliner",
            "description": "Smudge-proof waterproof eyeliner for precise, long-lasting definition.",
            "price": "249.00",
            "stock": 60,
            "image_url": "https://images.unsplash.com/photo-1583001931096-959e9a1a6223?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Lengthening Mascara",
            "description": "Volumising mascara that lengthens and curls lashes for a dramatic look.",
            "price": "399.00",
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Eyeshadow Palette",
            "description": "18-shade highly pigmented eyeshadow palette with matte and shimmer finishes.",
            "price": "899.00",
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Kohl Kajal",
            "description": "Intensely black kajal for bold eye looks that last all day.",
            "price": "149.00",
            "stock": 70,
            "image_url": "https://images.unsplash.com/photo-1583001931096-959e9a1a6223?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Hair Care": [
        {
            "name": "Nourishing Shampoo",
            "description": "Sulfate-free shampoo with argan oil for soft, shiny, healthy hair.",
            "price": "449.00",
            "stock": 35,
            "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Hair Growth Serum",
            "description": "Nourishing hair serum with biotin and keratin to reduce frizz and boost shine.",
            "price": "699.00",
            "stock": 28,
            "image_url": "https://images.unsplash.com/photo-1519735777090-ec97162dc266?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Deep Repair Hair Mask",
            "description": "Intensive hair mask that repairs damaged hair and restores moisture.",
            "price": "549.00",
            "stock": 22,
            "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Moisturising Conditioner",
            "description": "Daily conditioner with coconut milk for detangled, silky smooth hair.",
            "price": "349.00",
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Perfumes": [
        {
            "name": "Floral Eau De Parfum",
            "description": "A fresh floral bouquet of rose, jasmine and peony. Long-lasting 8+ hrs.",
            "price": "1299.00",
            "stock": 20,
            "image_url": "https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Rose Perfume",
            "description": "Rich, romantic rose perfume with hints of musk and sandalwood.",
            "price": "999.00",
            "stock": 18,
            "image_url": "https://images.unsplash.com/photo-1563170351-be82bc888aa4?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Vanilla Fragrance",
            "description": "Warm, sensual vanilla and amber fragrance for a cozy, inviting scent.",
            "price": "849.00",
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Fresh Citrus Perfume",
            "description": "Light, energising citrus perfume with notes of lemon, bergamot and mint.",
            "price": "749.00",
            "stock": 30,
            "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Body Care": [
        {
            "name": "Body Lotion",
            "description": "Rich moisturising body lotion with shea butter for silky soft skin.",
            "price": "399.00",
            "stock": 45,
            "image_url": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Exfoliating Body Scrub",
            "description": "Coffee and sugar scrub that gently exfoliates and leaves skin glowing.",
            "price": "499.00",
            "stock": 32,
            "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Luxe Shower Gel",
            "description": "Moisturising shower gel with a fresh floral fragrance for a spa experience.",
            "price": "299.00",
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Body Butter",
            "description": "Intensely nourishing body butter with cocoa and mango butter.",
            "price": "649.00",
            "stock": 28,
            "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80",
        },
    ],
    "Nail Care": [
        {
            "name": "Nail Polish",
            "description": "Quick-dry nail polish in a range of vivid shades with chip-resistant formula.",
            "price": "199.00",
            "stock": 80,
            "image_url": "https://images.unsplash.com/photo-1610992015732-2449b76344bc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Nail Polish Remover",
            "description": "Acetone-free nail polish remover with vitamin E that conditions nails.",
            "price": "149.00",
            "stock": 65,
            "image_url": "https://images.unsplash.com/photo-1610992015732-2449b76344bc?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Nail Care Kit",
            "description": "Complete 8-piece manicure kit with file, buffer, cuticle oil and more.",
            "price": "599.00",
            "stock": 20,
            "image_url": "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=600&q=80",
        },
        {
            "name": "Nail Strengthener",
            "description": "Fortifying base coat that hardens and protects brittle, weak nails.",
            "price": "249.00",
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=600&q=80",
        },
    ],
}


class Command(BaseCommand):
    help = "Seed demo cosmetics products for all 8 categories (safe, no duplicates)."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for category_name, products in SEED_DATA.items():
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                category = Category.objects.create(name=category_name)
                self.stdout.write(f"  Created category: {category_name}")

            for p in products:
                exists = Product.objects.filter(
                    category=category,
                    name=p["name"]
                ).exists()

                if exists:
                    skipped_count += 1
                    self.stdout.write(f"  Skipped (exists): {p['name']}")
                else:
                    Product.objects.create(
                        category=category,
                        name=p["name"],
                        description=p["description"],
                        price=p["price"],
                        stock=p["stock"],
                        image_url=p["image_url"],
                    )
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  Created: {p['name']} [{category_name}]")
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created: {created_count} products, Skipped: {skipped_count} existing."
            )
        )
