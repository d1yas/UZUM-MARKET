from django.contrib import admin
from .models import *


admin.site.site_header = 'Uzum Market'
admin.site.register(SalerApp)
# Register your models here.
