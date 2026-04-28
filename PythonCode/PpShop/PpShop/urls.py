from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from shop.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='token_obtain'),
]
