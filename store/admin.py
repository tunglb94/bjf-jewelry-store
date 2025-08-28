# bjf_project/store/admin.py

from django.contrib import admin
from solo.admin import SingletonModelAdmin
# --- IMPORT MỚI ---
from django.utils import timezone
# ------------------
from .models import (
    Category, Product, Post, SiteConfiguration, 
    ContactMessage, Order, OrderItem, Banner, 
    ProductVariation, ProductImage, ActionButton, Testimonial,
    AboutPage, JobPosting,
    # --- CÁC MODEL MỚI CHO HỆ THỐNG NHÂN SỰ ---
    PhongBan, ChucVu, NhanVien, ChamCong
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'order')

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    show_change_link = True
    fields = ('variation_type', 'variation_name', 'price_change', 'is_active')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sale_price', 'stock', 'is_available', 'is_featured')
    list_filter = ('is_available', 'is_featured', 'category')
    list_editable = ('price', 'sale_price', 'stock', 'is_available', 'is_featured')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariationInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'meta_title')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'meta_title', 'meta_description', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'content', 'image', 'author', 'published_date',)
        }),
        ('Tối ưu hóa SEO', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',),
            'description': 'Các trường này giúp bài viết được tìm kiếm tốt hơn trên Google.'
        }),
    )

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'quantity')
    extra = 0
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'full_name', 'phone_number', 'email')
    list_editable = ('status',)
    readonly_fields = ('full_name', 'phone_number', 'email', 'address', 'note', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('title', 'subtitle', 'link', 'is_active', 'order')
        }),
        ('Nội dung Banner', {
            'fields': ('file_type', 'image', 'video_url'),
            'description': "Chọn loại banner và điền thông tin tương ứng."
        }),
    )

@admin.register(ActionButton)
class ActionButtonAdmin(admin.ModelAdmin):
    list_display = ('button_type', 'phone_number', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Section Hero', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('Section Triết lý', {
            'fields': ('philosophy_tagline', 'philosophy_title', 'philosophy_content', 'philosophy_image')
        }),
        ('Section Lịch sử', {
            'fields': (
                'history_title', 'history_subtitle',
                'milestone1_year', 'milestone1_text', 'milestone1_image',
                'milestone2_year', 'milestone2_text', 'milestone2_image',
                'milestone3_year', 'milestone3_text', 'milestone3_image',
            )
        }),
         ('Section Chế tác', {
            'fields': ('craftsmanship_title', 'craftsmanship_subtitle')
        }),
    )

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'is_active', 'published_date')
    list_filter = ('is_active', 'job_type', 'location')
    search_fields = ('title', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)

# =======================================================
# ==            ADMIN CHO HỆ THỐNG NHÂN SỰ             ==
# =======================================================

class ChamCongInline(admin.TabularInline):
    model = ChamCong
    extra = 1
    fields = ('ngay_cham_cong', 'trang_thai', 'gio_check_in', 'gio_check_out', 'ghi_chu')
    ordering = ('-ngay_cham_cong',)

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('ma_nhan_vien', 'ho_ten', 'chuc_vu', 'phong_ban', 'trang_thai', 'hien_thi_luong_thang_nay')
    list_filter = ('trang_thai', 'phong_ban', 'chuc_vu')
    search_fields = ('ma_nhan_vien', 'ho_ten', 'email', 'so_dien_thoai')
    ordering = ('ho_ten',)
    inlines = [ChamCongInline]
    
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('ho_ten', 'ngay_sinh', 'so_dien_thoai', 'email')
        }),
        ('Thông tin công việc', {
            'fields': ('ma_nhan_vien', 'user', 'phong_ban', 'chuc_vu', 'ngay_vao_lam', 'luong_co_ban', 'trang_thai')
        }),
    )

    def hien_thi_luong_thang_nay(self, obj):
        today = timezone.now()
        luong = obj.tinh_luong_thang(today.year, today.month)
        return f"{int(luong):,} VND"
    
    hien_thi_luong_thang_nay.short_description = f"Lương tháng {timezone.now().month}/{timezone.now().year}"

@admin.register(ChamCong)
class ChamCongAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'ngay_cham_cong', 'trang_thai', 'gio_check_in', 'gio_check_out')
    list_filter = ('trang_thai', 'ngay_cham_cong')
    search_fields = ('nhan_vien__ho_ten', 'nhan_vien__ma_nhan_vien')
    ordering = ('-ngay_cham_cong', 'nhan_vien')
    date_hierarchy = 'ngay_cham_cong'

admin.site.register(PhongBan)
admin.site.register(ChucVu)