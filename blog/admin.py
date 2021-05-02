from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(main_category)
class Main_categoryAdmin(admin.ModelAdmin):
	list_display = ('name','description','slugurl')

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
	list_display = ('name','description','slugurl','image','main_category')

admin.site.register(account)
# admin.site.register(category)
admin.site.register(tag)
admin.site.register(block)
admin.site.register(blog_tag)
admin.site.register(like)
admin.site.register(comment)
admin.site.register(user_cookies)
admin.site.register(views)

@admin.register(blog)
class blogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'read_time','image','category','user','date')
    ordering = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('date', 'category')