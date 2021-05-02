from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class account(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	summary=models.CharField(max_length=400,default="summary is not avaible right now .but the is super cool")
	image = models.ImageField(default="noimage.jpg",upload_to='account')
	is_verified=models.BooleanField(default=True)
	def __str__(self):
		return self.user.first_name+" "+self.user.last_name+"*--*"+self.user.username

class main_category(models.Model):
	name=models.CharField(max_length=100)
	description = models.CharField(default= "",max_length=300)
	slugurl = models.SlugField(max_length=500,null=True)
	def __str__(self):
		return self.name


class category(models.Model):
	name=models.CharField(max_length=100)
	description = models.CharField(default= "",max_length=300)
	slugurl = models.SlugField(max_length=500,null=True)
	image = models.ImageField(default="noimage.jpg",upload_to='category')
	main_category = models.ForeignKey(main_category,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.name


class tag(models.Model):
	name=models.CharField(default="",max_length=200)
	slugurl = models.SlugField(max_length=400,null=True)
	def __str__(self):
		return self.name


class blog(models.Model):
	title = models.CharField(max_length=500)
	description = models.CharField(max_length=1000)
	read_time=models.IntegerField(default=0)    
	slugurl = models.SlugField(max_length=500,null=True)
	image = models.ImageField(default="noimage.jpg",upload_to='block')
	category = models.ForeignKey(category,on_delete=models.CASCADE,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField(auto_now=True)
	def __str__(self):
	    return self.title



class block(models.Model):
	blog = models.ForeignKey(blog,on_delete=models.CASCADE,null=True)
	content = RichTextField(blank=True,null=True)
	data = models.FileField(default="noimage.jpg",upload_to='titleimage')
	def __str__(self):
		return self.content

class blog_tag(models.Model):
	blog = models.ForeignKey(blog,on_delete=models.CASCADE,null=True)
	tag = models.ForeignKey(tag,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.blog.title+"--"+self.tag.name


class like(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	blog=models.ForeignKey(blog,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username+" -- "+self.blog.title


class comment(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	blog=models.ForeignKey(blog,on_delete=models.CASCADE)
	content=models.CharField(default="",max_length=200)
	date = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username+" -- "+self.blog.title+" - "+self.content		



class user_cookies(models.Model):
	u_id=models.CharField(default="",max_length=100)
	p_id=models.CharField(default="",max_length=100)
	address=models.CharField(default="0.0.0.0",max_length=100)
	def __str__(self):
		return self.u_id
		
class views(models.Model):
	blog=models.ForeignKey(blog,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.blog.title