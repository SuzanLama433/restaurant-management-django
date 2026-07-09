from django.contrib import admin
from .models import *

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_featured", "is_hot")
    list_filter = ("category", "is_featured", "is_hot")
    search_fields = ("title", "description", "tags")
    
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    
@admin.register(Chefs)
class ChefsAdmin(admin.ModelAdmin):
    list_display =['name','role']

@admin.register(Reservation)
class ChefsAdmin(admin.ModelAdmin):
    list_display =['name']