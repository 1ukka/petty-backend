from collections import UserDict
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


User = get_user_model()

class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)



class profile(Entity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name=models.CharField(max_length=100)
    email = models.EmailField('Email Address', unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    img=models.ImageField(upload_to='profile/',null=True,blank=True)


    def __str__(self):
        return self.name

class Product(Entity):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    height = models.FloatField('height', null=True, blank=True)
    qty = models.IntegerField('qty', null=True, blank=True)
    cost = models.IntegerField('cost', null=True, blank=True)
    price = models.IntegerField('price')  
    discounted_price = models.IntegerField('discounted price', null=True, blank=True)
    category = models.ForeignKey('ecommerce.Category', verbose_name='category', related_name='products',null=True,blank=True,on_delete=models.SET_NULL)
    is_featured = models.BooleanField('is featured')
    is_active = models.BooleanField('is active')


    def __str__(self):
        return self.name

    @property
    def images(self):
        return self.images.all()

class Category(Entity):
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children',null=True,
                            blank=True,
                            on_delete=models.CASCADE)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to='category/')
    is_active = models.BooleanField('is active')

    created = models.DateField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        if self.parent:
            return f'-   {self.name}'
        return f'{self.name}'

class Order(Entity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey('ecommerce.OrderStatus', verbose_name='status', related_name='orders', on_delete=models.SET_NULL, null=True)
    items=models.ManyToManyField('ecommerce.Item',related_name='orders',blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f'{self.user} {self.order_total}'

    @property
    def order_total(self):
        order_total = sum(
            i.product.price_discounted * i.item_qty for i in self.items.all()
        )

        return order_total

class Item(Entity):
    user = models.ForeignKey(User, verbose_name='user', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('ecommerce.Product', verbose_name='product',on_delete=models.CASCADE)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered')

    def __str__(self):
        return f'{self.product.name} quantity: {self.item_qty}'

class OrderStatus(Entity):
    NEW = 'NEW'
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'
    COMPLETED = 'COMPLETED'
    REFUNDED = 'REFUNDED'

    title = models.CharField('title', max_length=255, choices=[
        (NEW, NEW),
        (PROCESSING, PROCESSING),
        (SHIPPED, SHIPPED),
        (COMPLETED, COMPLETED),
        (REFUNDED, REFUNDED),
    ])
    is_default = models.BooleanField('is default')

    def __str__(self):
        return self.title

class Article(Entity):

    title = models.CharField('title', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to='article/')
    is_active = models.BooleanField('is active')

    def __str__(self):
        return self.title

class Images(Entity):
    image = models.ImageField('image', upload_to='product/')
    is_default_image = models.BooleanField('is default image')
    product = models.ForeignKey(Product, verbose_name='product', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)