from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from shop.views import RegisterView, MyProductListCreateView, ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='token_obtain'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('my-products/', MyProductListCreateView.as_view(), name='my-product-list-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
]
