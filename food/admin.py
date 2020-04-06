from django.contrib import admin

# Register your models here.
from food.models import Category, Food, Images

class FoodImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [FoodImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'food','image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Food,FoodAdmin)
admin.site.register(Images,ImagesAdmin)



