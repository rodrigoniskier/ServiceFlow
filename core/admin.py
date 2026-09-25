from django.contrib import admin
from .models import Category,Subcategory,ServiceRequest,ImportBatch
admin.site.register(Category); admin.site.register(Subcategory); admin.site.register(ServiceRequest); admin.site.register(ImportBatch)
admin.site.site_header="ServiceFlow Administration"; admin.site.site_title="ServiceFlow"
