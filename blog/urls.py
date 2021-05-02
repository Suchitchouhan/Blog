from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('',index,name='index'),
	path("signup",signup,name='signup'),
	path("login",login_view,name='login_view'),
	path('logout',logout_view,name='logout_view'),
	path('addblog',addblog,name='addblog'),
	path('@<str:slugurl>',blog_by_category,name='blog_by_category'),
	path('$<str:slugurl>',details_blog,name='details_blog'),
	

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

