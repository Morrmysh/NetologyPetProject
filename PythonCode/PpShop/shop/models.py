from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_ready_for_orders = models.BooleanField(default=False)

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара"
    )
    comment = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Описание товара"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Продавец"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        default=0
    )
    available = models.BooleanField(
        default=False,
        verbose_name="Доступен"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
