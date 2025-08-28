# bjf_project/store/models.py

from django.db import models
from django.utils import timezone
from solo.models import SingletonModel
from ckeditor.fields import RichTextField
import calendar
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=200, unique=True, help_text="Phần hiển thị trên URL, không dấu, không khoảng trắng. VD: nhan-kim-cuong")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Hình ảnh danh mục")
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Các danh mục"
        permissions = [
            ("manage_category", "Có thể quản lý toàn bộ Danh mục"),
        ]
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Danh mục")
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=255, unique=True, help_text="Phần hiển thị trên URL, sẽ được tự động tạo.", verbose_name="Đường dẫn URL", null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Mã sản phẩm (SKU)")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chi tiết")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá gốc (VND)")
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Giá khuyến mãi (VND)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Số lượng tồn kho")
    is_available = models.BooleanField(default=True, verbose_name="Đang bán?")
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Các sản phẩm"
        permissions = [
            ("manage_product", "Có thể quản lý toàn bộ Sản phẩm"),
        ]
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    is_main = models.BooleanField(default=False, verbose_name="Là ảnh chính?")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    class Meta:
        verbose_name = "Hình ảnh sản phẩm"
        verbose_name_plural = "Các hình ảnh sản phẩm"
        ordering = ['order', 'is_main']
    def __str__(self):
        return f"Hình ảnh của {self.product.name} ({self.id})"

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tiêu đề bài viết")
    slug = models.SlugField(max_length=255, unique=True, help_text="Phần hiển thị trên URL, sẽ được tự động tạo.", verbose_name="Đường dẫn URL", null=True, blank=True)
    content = RichTextField(verbose_name="Nội dung")
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Ảnh bìa")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Ngày đăng")
    author = models.CharField(max_length=100, default="BJF", verbose_name="Tác giả")
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tiêu đề SEO")
    meta_description = models.TextField(blank=True, null=True, verbose_name="Mô tả SEO")
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Từ khóa (keywords)")
    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Các bài viết"
        ordering = ['-published_date']
        permissions = [
            ("manage_post", "Có thể quản lý toàn bộ Bài viết"),
        ]
    def __str__(self):
        return self.title

class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='BJF', verbose_name="Tên website")
    site_description = models.TextField(blank=True, verbose_name="Mô tả trang web (SEO)")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Favicon (icon trên tab)")
    logo_text = models.CharField(max_length=255, default='BJF', verbose_name="Chữ trên Logo")
    hero_background_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Ảnh nền banner chính (dự phòng)")
    hero_title = models.CharField(max_length=255, default='Đẳng Cấp & Tinh Tế', verbose_name="Dòng tiêu đề chính")
    hero_subtitle = models.CharField(max_length=255, default='Trong Từng Chế Tác', verbose_name="Dòng tiêu đề phụ (chữ vàng)")
    hero_description = models.TextField(blank=True, verbose_name="Mô tả ngắn dưới tiêu đề")
    slider_delay = models.PositiveIntegerField(default=5, verbose_name="Thời gian chuyển slide (giây)")
    footer_address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ ở Footer")
    footer_phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại ở Footer")
    footer_email = models.EmailField(blank=True, verbose_name="Email ở Footer")
    footer_copyright = models.CharField(max_length=255, default='© 2025 Bản quyền thuộc về Công ty Vàng Bạc Đá Quý BJF.', verbose_name="Dòng copyright")
    class Meta:
        verbose_name = "Cài đặt chung"
        verbose_name_plural = "Cài đặt chung"
    def __str__(self):
        return "Cài đặt chung"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Nội dung tin nhắn")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")
    class Meta:
        verbose_name = "Tin nhắn liên hệ"
        verbose_name_plural = "Các tin nhắn liên hệ"
        ordering = ['-created_at']
    def __str__(self):
        return f"Tin nhắn từ {self.name} ({self.email})"

class Order(models.Model):
    STATUS_CHOICES = (('pending', 'Chờ xác nhận'), ('processing', 'Đang xử lý'), ('shipped', 'Đang giao hàng'), ('completed', 'Đã hoàn thành'), ('cancelled', 'Đã hủy'),)
    full_name = models.CharField(max_length=255, verbose_name="Họ và tên")
    phone_number = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ giao hàng")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú của khách hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái đơn hàng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo đơn")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Các đơn hàng"
        ordering = ['-created_at']
        permissions = [
            ("manage_order", "Có thể quản lý toàn bộ Đơn hàng"),
        ]
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá tại thời điểm mua")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    class Meta:
        verbose_name = "Sản phẩm trong đơn hàng"
        verbose_name_plural = "Các sản phẩm trong đơn hàng"
    def __str__(self):
        return str(self.id)

class Banner(models.Model):
    BUTTON_TYPE_CHOICES = (('image', 'Hình ảnh'), ('video', 'Video'),)
    file_type = models.CharField(max_length=10, choices=BUTTON_TYPE_CHOICES, default='image', verbose_name="Loại banner")
    image = models.ImageField(upload_to='banners/', verbose_name="Hình ảnh banner", blank=True, null=True, help_text="Tải lên nếu loại banner là 'Hình ảnh'.")
    video_url = models.URLField(blank=True, null=True, verbose_name="Đường dẫn Video (YouTube/Vimeo Embed)", help_text="Dán link EMBED vào đây nếu loại banner là 'Video'. Ví dụ: https://www.youtube.com/embed/your_video_id")
    title = models.CharField(max_length=255, blank=True, verbose_name="Tiêu đề chính (tùy chọn)")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Tiêu đề phụ (tùy chọn)")
    link = models.URLField(blank=True, verbose_name="Đường dẫn (tùy chọn)")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị?")
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị, số nhỏ hơn hiện trước", verbose_name="Thứ tự")
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Các Banner"
        ordering = ['order']
        permissions = [
            ("manage_banner", "Có thể quản lý toàn bộ Banner"),
        ]
    def __str__(self):
        return self.title or f"Banner {self.id}"

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations', verbose_name="Sản phẩm")
    variation_type = models.CharField(max_length=50, verbose_name="Loại biến thể", choices=(('gold', 'Vàng'), ('color', 'Màu sắc'), ('stone_type', 'Loại hạt'),))
    variation_name = models.CharField(max_length=100, verbose_name="Tên biến thể")
    price_change = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Thay đổi giá (VND)")
    is_active = models.BooleanField(default=True, verbose_name="Hoạt động?")
    class Meta:
        verbose_name = "Biến thể sản phẩm"
        verbose_name_plural = "Các biến thể sản phẩm"
        unique_together = ('product', 'variation_type', 'variation_name')
    def __str__(self):
        return f"{self.product.name} - {self.get_variation_type_display()}: {self.variation_name}"

class ActionButton(models.Model):
    BUTTON_TYPE_CHOICES = (('zalo', 'Zalo'), ('phone', 'Gọi điện'),)
    button_type = models.CharField(max_length=10, choices=BUTTON_TYPE_CHOICES, verbose_name="Loại nút")
    phone_number = models.CharField(max_length=20, verbose_name="Số điện thoại")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị?")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    class Meta:
        verbose_name = "Nút hành động"
        verbose_name_plural = "Các nút hành động"
        ordering = ['order']
    def __str__(self):
        return f"{self.get_button_type_display()} - {self.phone_number}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên khách hàng")
    title = models.CharField(max_length=100, verbose_name="Chức danh/Địa chỉ", help_text="Ví dụ: Doanh nhân, TP.HCM")
    quote = models.TextField(verbose_name="Nội dung nhận xét")
    image = models.ImageField(upload_to='testimonials/', verbose_name="Ảnh đại diện khách hàng")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị?")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    class Meta:
        verbose_name = "Nhận xét của khách hàng"
        verbose_name_plural = "Các nhận xét của khách hàng"
        ordering = ['order']
    def __str__(self):
        return self.name

class AboutPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="Câu Chuyện Về BJF", verbose_name="Tiêu đề chính")
    hero_subtitle = models.CharField(max_length=300, default="Nơi mỗi tuyệt tác không chỉ là trang sức, mà là di sản của đam mê và sự tinh xảo.", verbose_name="Tiêu đề phụ")
    hero_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Ảnh nền Hero")
    philosophy_tagline = models.CharField(max_length=100, default="Triết Lý Của Chúng Tôi", verbose_name="Dòng giới thiệu Triết lý")
    philosophy_title = models.CharField(max_length=200, default="Tôn Vinh Vẻ Đẹp Vĩnh Cửu", verbose_name="Tiêu đề Triết lý")
    philosophy_content = models.TextField(default="Tại BJF, chúng tôi tin rằng trang sức là ngôn ngữ của cảm xúc...", verbose_name="Nội dung Triết lý")
    philosophy_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Ảnh Triết lý")
    history_title = models.CharField(max_length=200, default="Dấu Ấn Qua Từng Thời Kỳ", verbose_name="Tiêu đề Lịch sử")
    history_subtitle = models.CharField(max_length=300, default="Hơn hai thập kỷ không ngừng nỗ lực để xây dựng một thương hiệu trang sức Việt Nam uy tín và đẳng cấp.", verbose_name="Tiêu đề phụ Lịch sử")
    milestone1_year = models.CharField(max_length=50, default="2005: Khởi Đầu Đam Mê", verbose_name="Cột mốc 1 - Năm & Tiêu đề")
    milestone1_text = models.TextField(default="BJF ra đời từ một xưởng chế tác nhỏ...", verbose_name="Cột mốc 1 - Nội dung")
    milestone1_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Cột mốc 1 - Ảnh")
    milestone2_year = models.CharField(max_length=50, default="2015: Khẳng Định Vị Thế", verbose_name="Cột mốc 2 - Năm & Tiêu đề")
    milestone2_text = models.TextField(default="Trở thành một trong những thương hiệu được tin cậy hàng đầu...", verbose_name="Cột mốc 2 - Nội dung")
    milestone2_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Cột mốc 2 - Ảnh")
    milestone3_year = models.CharField(max_length=50, default="2025: Vươn Ra Thế Giới", verbose_name="Cột mốc 3 - Năm & Tiêu đề")
    milestone3_text = models.TextField(default="Ra mắt nền tảng thương mại điện tử...", verbose_name="Cột mốc 3 - Nội dung")
    milestone3_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Cột mốc 3 - Ảnh")
    craftsmanship_title = models.CharField(max_length=200, default="Nghệ Thuật Chế Tác Đỉnh Cao", verbose_name="Tiêu đề Chế tác")
    craftsmanship_subtitle = models.CharField(max_length=300, default="Mỗi sản phẩm là một bản giao hưởng của vật liệu quý hiếm và bàn tay tài hoa của nghệ nhân.", verbose_name="Tiêu đề phụ Chế tác")
    class Meta:
        verbose_name = "Trang Về Chúng Tôi"
    def __str__(self):
        return "Trang Về Chúng Tôi"

class JobPosting(models.Model):
    JOB_TYPE_CHOICES = (('full-time', 'Toàn thời gian'), ('part-time', 'Bán thời gian'), ('internship', 'Thực tập'),)
    title = models.CharField(max_length=255, verbose_name="Chức danh")
    slug = models.SlugField(max_length=255, unique=True, help_text="Phần hiển thị trên URL, sẽ được tự động tạo.", verbose_name="Đường dẫn URL", null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name="Địa điểm làm việc")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name="Loại hình công việc")
    description = RichTextField(verbose_name="Mô tả công việc")
    requirements = RichTextField(verbose_name="Yêu cầu ứng viên")
    is_active = models.BooleanField(default=True, verbose_name="Đang tuyển?")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Ngày đăng")
    class Meta:
        verbose_name = "Tin tuyển dụng"
        verbose_name_plural = "Các tin tuyển dụng"
        ordering = ['-published_date']
    def __str__(self):
        return self.title

# =======================================================
# ==               HỆ THỐNG QUẢN LÝ NHÂN SỰ            ==
# =======================================================

class PhongBan(models.Model):
    ten_phong_ban = models.CharField(max_length=100, unique=True, verbose_name="Tên phòng ban")
    class Meta:
        verbose_name = "Phòng Ban"
        verbose_name_plural = "Các Phòng Ban"
    def __str__(self):
        return self.ten_phong_ban

class ChucVu(models.Model):
    ten_chuc_vu = models.CharField(max_length=100, unique=True, verbose_name="Tên chức vụ")
    class Meta:
        verbose_name = "Chức Vụ"
        verbose_name_plural = "Các Chức Vụ"
    def __str__(self):
        return self.ten_chuc_vu

class NhanVien(models.Model):
    class TrangThaiLamViec(models.TextChoices):
        DANG_LAM_VIEC = 'DLV', 'Đang làm việc'
        DA_NGHI_VIEC = 'DNV', 'Đã nghỉ việc'
        TAM_NGHI = 'TN', 'Tạm nghỉ'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tài khoản")
    ma_nhan_vien = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    ho_ten = models.CharField(max_length=100, verbose_name="Họ và tên")
    ngay_sinh = models.DateField(verbose_name="Ngày sinh")
    so_dien_thoai = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    email = models.EmailField(unique=True, verbose_name="Email")
    phong_ban = models.ForeignKey(PhongBan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Phòng ban")
    chuc_vu = models.ForeignKey(ChucVu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Chức vụ")
    ngay_vao_lam = models.DateField(verbose_name="Ngày vào làm")
    luong_co_ban = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Lương cơ bản (VND)")
    trang_thai = models.CharField(max_length=3, choices=TrangThaiLamViec.choices, default=TrangThaiLamViec.DANG_LAM_VIEC, verbose_name="Trạng thái làm việc")
    class Meta:
        verbose_name = "Nhân Viên"
        verbose_name_plural = "Danh sách Nhân Viên"
        permissions = [
            ("manage_nhanvien", "Có thể quản lý toàn bộ Nhân sự"),
        ]
    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"
    def tinh_luong_thang(self, year, month):
        if self.luong_co_ban <= 0: return 0
        _, so_ngay_trong_thang = calendar.monthrange(year, month)
        if so_ngay_trong_thang == 0: return 0
        luong_theo_ngay = self.luong_co_ban / so_ngay_trong_thang
        so_ngay_di_lam = ChamCong.objects.filter(nhan_vien=self, ngay_cham_cong__year=year, ngay_cham_cong__month=month, trang_thai=ChamCong.TrangThaiChamCong.DI_LAM).count()
        luong_thuc_te = luong_theo_ngay * so_ngay_di_lam
        return luong_thuc_te

class ChamCong(models.Model):
    class TrangThaiChamCong(models.TextChoices):
        DI_LAM = 'DL', 'Đi làm'
        NGHI_PHEP = 'NP', 'Nghỉ phép'
        VANG_KHONG_PHEP = 'VKP', 'Vắng không phép'
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, verbose_name="Nhân viên")
    ngay_cham_cong = models.DateField(verbose_name="Ngày chấm công")
    trang_thai = models.CharField(max_length=3, choices=TrangThaiChamCong.choices, default=TrangThaiChamCong.DI_LAM, verbose_name="Trạng thái")
    gio_check_in = models.TimeField(null=True, blank=True, verbose_name="Giờ check-in")
    gio_check_out = models.TimeField(null=True, blank=True, verbose_name="Giờ check-out")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    class Meta:
        verbose_name = "Chấm Công"
        verbose_name_plural = "Dữ liệu Chấm Công"
        unique_together = ('nhan_vien', 'ngay_cham_cong')
    def __str__(self):
        return f"Chấm công {self.nhan_vien.ho_ten} - {self.ngay_cham_cong}"

# =======================================================
# ==         HỆ THỐNG QUẢN LÝ BẤT ĐỘNG SẢN           ==
# =======================================================

class LoaiBatDongSan(models.Model):
    ten_loai = models.CharField(max_length=100, unique=True, verbose_name="Tên loại BĐS")
    class Meta:
        verbose_name = "Loại Bất động sản"
        verbose_name_plural = "Các Loại Bất động sản"
    def __str__(self):
        return self.ten_loai

class BatDongSan(models.Model):
    # I. Thông tin cơ bản
    id_tai_san = models.CharField(max_length=50, unique=True, verbose_name="ID tài sản")
    loai_bds = models.ForeignKey(LoaiBatDongSan, on_delete=models.SET_NULL, null=True, verbose_name="Loại BĐS")
    dia_chi = models.CharField(max_length=255, verbose_name="Địa chỉ")
    google_maps_link = models.URLField(blank=True, null=True, verbose_name="Link Google Maps")
    chi_tiet_su_dung_dat = models.CharField(max_length=255, verbose_name="Chi tiết sử dụng đất", help_text="Ví dụ: Đất thổ cư 5100 m2")
    mat_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Mặt tiền (m)")
    chieu_sau = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Chiều sâu (m)")
    huong = models.CharField(max_length=50, blank=True, verbose_name="Hướng")
    phap_ly = models.CharField(max_length=100, default="Sổ đỏ/Sổ hồng", verbose_name="Pháp lý")
    tinh_trang_xay_dung = models.CharField(max_length=100, default="Đất trống", verbose_name="Tình trạng xây dựng")
    hien_trang_su_dung = models.TextField(blank=True, verbose_name="Hiện trạng sử dụng")
    # II. Giá và giao dịch
    gia_rao_cam_co = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Giá chủ nhà rao cầm cố (VNĐ)")
    gia_chot_ky_vong = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Khoảng giá chốt kỳ vọng (VNĐ)")
    don_gia_tham_khao = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Đơn giá tham khảo (VNĐ/m2)")
    # III. Phân tích tiềm năng
    phan_tich_tiem_nang = models.TextField(blank=True, verbose_name="Phân tích tiềm năng và hạ tầng")
    uu_diem_vi_tri = models.TextField(blank=True, verbose_name="Ưu điểm vị trí")
    nhuoc_diem = models.TextField(blank=True, verbose_name="Nhược điểm/Hạn chế")
    quy_hoach = models.TextField(blank=True, verbose_name="Quy hoạch/Kế hoạch sử dụng đất")
    # V. Người khảo sát
    nguoi_khao_sat = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người khảo sát")
    thoi_gian_khao_sat = models.DateField(null=True, blank=True, verbose_name="Thời gian khảo sát")
    ghi_chu_them = models.TextField(blank=True, verbose_name="Ghi chú thêm")
    class Meta:
        verbose_name = "Bất động sản"
        verbose_name_plural = "Danh sách Bất động sản"
        permissions = [
            ("manage_batdongsan", "Có thể quản lý toàn bộ Bất động sản"),
        ]
    def __str__(self):
        return self.id_tai_san

class HinhAnhBatDongSan(models.Model):
    bat_dong_san = models.ForeignKey(BatDongSan, on_delete=models.CASCADE, related_name='hinh_anh', verbose_name="Bất động sản")
    image = models.ImageField(upload_to='bds/hien_trang/', verbose_name="Hình ảnh")
    mo_ta = models.CharField(max_length=255, blank=True, verbose_name="Mô tả ngắn")
    class Meta:
        verbose_name = "Hình ảnh Bất động sản"
        verbose_name_plural = "Các Hình ảnh Bất động sản"
    def __str__(self):
        return f"Hình ảnh cho {self.bat_dong_san.id_tai_san}"