from django.contrib import admin

# Register your models here.
from .models import ProductModel,CategoryModel,KatalogModel
admin.site.register(KatalogModel)
admin.site.register(CategoryModel)
admin.site.register(ProductModel)
