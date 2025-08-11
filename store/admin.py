# bjf_project/store/admin.py

from django.contrib import admin
from solo.admin import SingletonModelAdmin
# Thêm ActionButton vào đây
from .models import Category, Product, Post, SiteConfiguration, ContactMessage, Order, OrderItem, Banner, ProductVariation, ProductImage, ActionButton

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
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

# === DÁN VÀO ĐÂY ===
@admin.register(ActionButton)
class ActionButtonAdmin(admin.ModelAdmin):
    list_display = ('button_type', 'phone_number', 'is_active', 'order')
    list_editable = ('is_active', 'order')