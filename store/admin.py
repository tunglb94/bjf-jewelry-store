# bjf_project/store/admin.py

from django.contrib import admin, messages
from solo.admin import SingletonModelAdmin
from django.utils import timezone
from django.http import HttpResponse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm
import io
import os
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import (
    Category, Product, Post, SiteConfiguration,
    ContactMessage, Order, OrderItem, Banner,
    ProductVariation, ProductImage, ActionButton, Testimonial,
    AboutPage, JobPosting,
    PhongBan, ChucVu, NhanVien, ChamCong,
    BatDongSan, HinhAnhBatDongSan, LoaiBatDongSan
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

# =======================================================
# ==         ADMIN CHO HỆ THỐNG BẤT ĐỘNG SẢN           ==
# =======================================================

@admin.register(LoaiBatDongSan)
class LoaiBatDongSanAdmin(admin.ModelAdmin):
    list_display = ('ten_loai',)
    search_fields = ('ten_loai',)

class HinhAnhBatDongSanInline(admin.TabularInline):
    model = HinhAnhBatDongSan
    extra = 3
    fields = ('image', 'mo_ta')
    verbose_name = "Hình ảnh"
    verbose_name_plural = "Thêm các hình ảnh (sổ đỏ, hiện trạng...)"


def export_as_docx(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Vui lòng chỉ chọn 1 tài sản để xuất file.", messages.WARNING)
        return

    bds = queryset.first()

    template_path = os.path.join(settings.BASE_DIR, 'store', 'docx_templates', 'template.docx')
    doc = DocxTemplate(template_path)

    context = {
        'id_tai_san': bds.id_tai_san,
        'loai_bds': bds.loai_bds.ten_loai if bds.loai_bds else "",
        'dia_chi': bds.dia_chi,
        'chi_tiet_su_dung_dat': bds.chi_tiet_su_dung_dat,
        'mat_tien': bds.mat_tien,
        'chieu_sau': bds.chieu_sau,
        'huong': bds.huong,
        'phap_ly': bds.phap_ly,
        'tinh_trang_xay_dung': bds.tinh_trang_xay_dung,
        'hien_trang_su_dung': bds.hien_trang_su_dung,
        'gia_rao_cam_co': f"{bds.gia_rao_cam_co:,.0f} VNĐ",
        'gia_chot_ky_vong': f"{bds.gia_chot_ky_vong:,.0f} VNĐ",
        'phan_tich_tiem_nang': bds.phan_tich_tiem_nang,
        'uu_diem_vi_tri': bds.uu_diem_vi_tri,
        'nhuoc_diem': bds.nhuoc_diem,
        'quy_hoach': bds.quy_hoach,
        'nguoi_khao_sat': bds.nguoi_khao_sat.ho_ten if bds.nguoi_khao_sat else "",
        'sdt_nguoi_khao_sat': bds.nguoi_khao_sat.so_dien_thoai if bds.nguoi_khao_sat else "",
        'thoi_gian_khao_sat': bds.thoi_gian_khao_sat.strftime('%d/%m/%Y') if bds.thoi_gian_khao_sat else "",
        'ghi_chu_them': bds.ghi_chu_them,
    }

    # === PHẦN GỠ LỖI BẮT ĐẦU ===
    image_paths_to_check = []
    hinh_anh_list = list(bds.hinh_anh.all())

    for i, hinh_anh in enumerate(hinh_anh_list[:3]):
        if hinh_anh.image and hasattr(hinh_anh.image, 'path'):
            image_path = hinh_anh.image.path
            image_paths_to_check.append(image_path)
            
            # Kiểm tra xem tệp có tồn tại không
            if os.path.exists(image_path):
                try:
                    context[f'anh_{i+1}'] = InlineImage(doc, image_path, width=Cm(15))
                except Exception as e:
                    messages.error(request, f"Lỗi khi xử lý ảnh {i+1}: {e}")
                    return
            else:
                # Nếu không tồn tại, báo lỗi chi tiết
                messages.error(request, f"Lỗi: Không tìm thấy tệp ảnh {i+1} tại đường dẫn: {image_path}")
                return
    
    if not image_paths_to_check:
        messages.warning(request, "Bất động sản này không có hình ảnh nào để chèn vào file.")
    # === PHẦN GỠ LỖI KẾT THÚC ===

    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename={bds.id_tai_san}.docx'
    return response

export_as_docx.short_description = "Tải về file thông tin BĐS (.docx)"

@admin.register(BatDongSan)
class BatDongSanAdmin(admin.ModelAdmin):
    list_display = ('id_tai_san', 'dia_chi', 'loai_bds', 'nguoi_khao_sat')
    list_filter = ('loai_bds', 'nguoi_khao_sat')
    search_fields = ('id_tai_san', 'dia_chi')
    actions = [export_as_docx]

    inlines = [HinhAnhBatDongSanInline]

    fieldsets = (
        ("I. Thông tin cơ bản", {"fields": ("id_tai_san", "loai_bds", "dia_chi", "google_maps_link", "chi_tiet_su_dung_dat", "mat_tien", "chieu_sau", "huong", "phap_ly", "tinh_trang_xay_dung", "hien_trang_su_dung")}),
        ("II. Giá và giao dịch", {"fields": ("gia_rao_cam_co", "gia_chot_ky_vong", "don_gia_tham_khao")}),
        ("III. Phân tích", {"fields": ("phan_tich_tiem_nang", "uu_diem_vi_tri", "nhuoc_diem", "quy_hoach")}),
        ("V. Khảo sát", {"fields": ("nguoi_khao_sat", "thoi_gian_khao_sat", "ghi_chu_them")}),
    )

# =======================================================
# ==          TÙY CHỈNH TRANG QUẢN LÝ GROUP            ==
# =======================================================

def assign_hr_permissions(modeladmin, request, queryset):
    hr_models = [NhanVien, ChamCong, PhongBan, ChucVu]
    content_types = ContentType.objects.get_for_models(*hr_models)
    permissions = Permission.objects.filter(content_type__in=content_types.values())
    for group in queryset:
        group.permissions.add(*permissions)
    modeladmin.message_user(request, f"Đã gán thành công {permissions.count()} quyền Nhân sự cho {queryset.count()} nhóm.", messages.SUCCESS)
assign_hr_permissions.short_description = "Gán toàn bộ quyền Quản lý Nhân sự"


def assign_sales_permissions(modeladmin, request, queryset):
    sales_models = [Order, Product, Category, Testimonial, ContactMessage]
    content_types = ContentType.objects.get_for_models(*sales_models)
    permissions = Permission.objects.filter(content_type__in=content_types.values())
    for group in queryset:
        group.permissions.add(*permissions)
    modeladmin.message_user(request, f"Đã gán thành công {permissions.count()} quyền Kinh doanh cho {queryset.count()} nhóm.", messages.SUCCESS)
assign_sales_permissions.short_description = "Gán toàn bộ quyền Quản lý Kinh doanh"

class CustomGroupAdmin(BaseGroupAdmin):
    actions = [assign_hr_permissions, assign_sales_permissions]

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)