from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validation import *
from .managers import UserManager
import datetime
from django.utils import timezone

# Create your models here.
CAT_CHOICES = (('Electronics', 'Electronics'), ('Vegetables', 'Vegetables'), ("Women's Clothes", "Women's Clothes"),
               ('Mens Clothes', "Mens Clothes"), ('Teddy', "Teddy"))
CAT_TYPE_CHOICES = (("peace", '/Peace'), ("kg", '/Kg'), ("packet", '/Packet'))


def get_current_time():
    return timezone.now().time()


def get_current_date():
    return timezone.now().date()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email])
    mobile = models.CharField(max_length=15, unique=True, validators=[validate_mobile_number])
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_inactive = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.email, self.mobile)


class OrderAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_address')
    country = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    landmark = models.CharField(max_length=30, null=True, blank=True)
    road = models.CharField(max_length=50, null=True, blank=True)
    place = models.CharField(max_length=50, blank=True, null=True)
    pin = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.country, self.state)


class Product(BaseModel):
    p_name = models.CharField(max_length=250)
    p_title = models.TextField(max_length=300)
    brand = models.CharField(max_length=50, blank=True, null=True)
    cat = models.CharField(choices=CAT_CHOICES, max_length=20)
    quantity_type = models.CharField(choices=CAT_TYPE_CHOICES, max_length=20)
    offer = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="images/", max_length=500)
    prize = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.p_name, self.p_title)

    @property
    def discounted_price(self):
        return self.prize * (1 - self.offer / 100)

    def save(self, *args, **kwargs):
        self.offer = self.prize * (1 - self.offer / 100)
        super().save(*args, **kwargs)


class CartItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{}".format(self.product)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()
    prize = models.IntegerField()
    total_prize = models.FloatField()
    order_date = models.DateField(default=get_current_date)
    order_time = models.TimeField(default=get_current_time)
    status = models.BooleanField(default=False)
    order_address = models.TextField(max_length=100)

    def __str__(self):
        return str(self.user) + " | " + str(self.product)
