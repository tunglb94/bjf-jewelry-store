# store/management/commands/relink_media.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Product, Post, Category, ProductImage

class Command(BaseCommand):
    help = 'Scans the media directory and tries to relink orphaned images to database entries based on slug.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Bắt đầu quá trình kết nối lại media ---'))
        
        self.relink_product_images()
        self.relink_single_image_model(Post, 'posts')
        self.relink_single_image_model(Category, 'categories')

        self.stdout.write(self.style.SUCCESS('--- Hoàn tất! ---'))

    def relink_product_images(self):
        media_path = os.path.join(settings.MEDIA_ROOT, 'products')
        self.stdout.write(f"\nScanning for Product images in {media_path}...")

        if not os.path.exists(media_path):
            self.stdout.write(self.style.WARNING(f"Thư mục {media_path} không tồn tại, bỏ qua."))
            return

        # Tìm các sản phẩm chưa có bất kỳ ảnh nào trong ProductImage
        products_without_images = Product.objects.filter(images__isnull=True)
        count = 0

        for product in products_without_images:
            if not product.slug:
                continue

            possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            for ext in possible_extensions:
                image_filename = f"{product.slug}{ext}"
                image_filepath = os.path.join(media_path, image_filename)
                
                if os.path.exists(image_filepath):
                    # Tạo một bản ghi ProductImage mới để kết nối
                    image_db_path = os.path.join('products', image_filename)
                    ProductImage.objects.create(
                        product=product,
                        image=image_db_path,
                        is_main=True # Đặt làm ảnh chính
                    )
                    self.stdout.write(self.style.SUCCESS(f"  [OK] Đã kết nối '{image_db_path}' cho Product '{product}'"))
                    count += 1
                    break 
        
        self.stdout.write(f"Đã kết nối lại được {count} ảnh cho Product.")

    def relink_single_image_model(self, Model, media_subdir):
        media_path = os.path.join(settings.MEDIA_ROOT, media_subdir)
        model_name = Model.__name__
        self.stdout.write(f"\nScanning for {model_name} images in {media_path}...")

        if not os.path.exists(media_path):
            self.stdout.write(self.style.WARNING(f"Thư mục {media_path} không tồn tại, bỏ qua."))
            return

        items_without_image = Model.objects.filter(image__isnull=True) | Model.objects.filter(image='')
        count = 0

        for item in items_without_image:
            if not hasattr(item, 'slug') or not item.slug:
                continue

            possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            for ext in possible_extensions:
                image_filename = f"{item.slug}{ext}"
                image_filepath = os.path.join(media_path, image_filename)
                
                if os.path.exists(image_filepath):
                    image_db_path = os.path.join(media_subdir, image_filename)
                    item.image = image_db_path
                    item.save()
                    self.stdout.write(self.style.SUCCESS(f"  [OK] Đã kết nối '{image_db_path}' cho {model_name} '{item}'"))
                    count += 1
                    break
        
        self.stdout.write(f"Đã kết nối lại được {count} ảnh cho {model_name}.")