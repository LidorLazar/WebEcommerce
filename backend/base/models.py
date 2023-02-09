from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='no-image.png')



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'address', 'city', 'phone_number']

    def __str__(self):
        return self.username


class Product(models.Model):

    CATEGORY_CHOICES = (
        (1, 'Soccer shoes'),
        (2, 'Ball')

    )

    # RATING_CHOICES = (
    #     (1, 1),
    #     (2, 2),
    #     (3, 3),
    #     (4, 4),
    #     (5, 5)
    # )
    id = models.AutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200, null=True, blank=False)
    image = models.ImageField(null=False, blank=False, default='no-image.png')
    image2 = models.ImageField(null=False, blank=False, default='no-image.png')
    image3 = models.ImageField(null=False, blank=False, default='no-image.png')
    brand = models.CharField(max_length=100, null=False, blank=False)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField( null=False, blank=False)
    # rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    # num_reviews = models.IntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count_in_stock = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.product_name
    
    

class Reviwe(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    product = models.ManyToManyField(Product)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    name =  models.CharField(max_length=100, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    text_comment = models.TextField( null=True, blank=True)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_methods = models.CharField(max_length=20, null=False, blank=False)
    create_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id.name, )


class OrderItem(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    product =  models.ForeignKey(Product, on_delete=models.PROTECT)
    order =  models.ForeignKey(Order, on_delete=models.PROTECT)
    name = models.CharField(max_length=20, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name



class ShippingAddress(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.PROTECT, null=False, blank=False)
    address = models.CharField(max_length=1000, null=False, blank=False)
    city =  models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    zip_code = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.address