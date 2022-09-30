from os import name
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db.models.fields import SlugField

from store_django.settings import BASE_REQUEST_URL

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
         return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to= 'uploads/', blank=True, null =True)
    thumbnail= models.ImageField(upload_to= 'uploads/', blank=True, null =True)
    date_added =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)# in descending order

    def __str__(self):
        return self.name

    def get_absolute_url(self):
         return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return f'{BASE_REQUEST_URL}'+ self.image.url
        return ''
    def get_thumbnail(self):
        if self.thumbnail:
            return f'{BASE_REQUEST_URL}'+ self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return f'{BASE_REQUEST_URL}'+ self.thumbnail.url
            return ''
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img. thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail




