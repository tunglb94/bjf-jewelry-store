# store/management/commands/relink_media.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Product, Post, Category # Import các model cần xử lý

class Command(BaseCommand):
    help = 'Scans the media directory and tries to relink orphaned images to database entries based on slug.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Bắt đầu quá trình kết nối lại media ---'))

        # Xử lý cho model Product
        self.relink_model(Product, 'products')

        # Xử lý cho model Post
        self.relink_model(Post, 'posts')

        # Xử lý cho model Category
        self.relink_model(Category, 'categories')

        self.stdout.write(self.style.SUCCESS('--- Hoàn tất! ---'))

    def relink_model(self, Model, media_subdir):
        media_path = os.path.join(settings.MEDIA_ROOT, media_subdir)
        model_name = Model.__name__
        self.stdout.write(f"\nScanning for {model_name} images in {media_path}...")

        if not os.path.exists(media_path):
            self.stdout.write(self.style.WARNING(f"Thư mục {media_path} không tồn tại, bỏ qua."))
            return

        items_without_image = Model.objects.filter(image__isnull=True) | Model.objects.filter(image='')
        count = 0

        for item in items_without_image:
            if not item.slug:
                continue

            # Thử tìm các file ảnh có tên trùng với slug
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
                    break # Chuyển sang item tiếp theo khi đã tìm thấy ảnh

        self.stdout.write(f"Đã kết nối lại được {count} ảnh cho {model_name}.")