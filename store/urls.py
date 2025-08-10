# bjf_project/store/urls.py

from django.urls import path
from . import views

# Dòng này rất quan trọng để định danh nhóm URL này
app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('san-pham/', views.product_list, name='product_list'),
    path('san-pham/<slug:slug>/', views.product_detail, name='product_detail'),
    path('tin-tuc/', views.post_list, name='post_list'),
    path('tin-tuc/<slug:slug>/', views.post_detail, name='post_detail'),
    path('lien-he/', views.contact, name='contact'),
    
    # URLs cho giỏ hàng
    path('gio-hang/', views.cart_detail, name='cart_detail'),
    path('them-vao-gio-hang/', views.add_to_cart, name='add_to_cart'),
    path('xoa-khoi-gio-hang/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('thanh-toan/', views.checkout, name='checkout'),
]
