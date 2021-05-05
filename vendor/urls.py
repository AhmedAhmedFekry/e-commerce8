from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor-admin/', views.vendor_admin, name='vendor_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/',
         views.edit_product,
         name='edit_product'),
    # path('edit-vendor/', views.edit_vendor, name='edit_vendor'),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_vendor, name='login_vendor'),
    # path('', views.vendors, name='vendors'),
    # path('<int:vendor_id>/', views.vendor, name='vendor'),
]