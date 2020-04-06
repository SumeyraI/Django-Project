from django.contrib import admin

# Register your models here.
from food.models import Category, Food, Images

class FoodImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount', 'status']
    list_filter = ['status', 'category']
    inlines = [FoodImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'food','image']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Food,FoodAdmin)
admin.site.register(Images,ImagesAdmin)

