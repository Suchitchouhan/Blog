from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
# Create your views here.


def check_blank_or_null(data):
	status=True
	for x in data:
		if x=="" or x==None:
			status=False
			break
		else:
			pass					
	return status	

def check_length(data):
	status=True
	for x in data:
		if len(x[0])<=x[1]:
			status=True
		else:
			pass
	return status


def check_null(data):
	status=True
	for x in data:
		if x==None:
			status=False
			break
		else:
			pass					
	return status



def login_view(request):
	context={}
	if request.method=="POST":
		username=request.POST.get("email")
		password=request.POST.get("password")
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			return redirect("/")	
			# context['status']="login successfully"
		else:
			context['status']="email and password is not exists" 
		return render(request,"blog/signup.html",context)
	else:
		return render(request,"blog/signup.html",context)




@login_required()
def logout_view(request):
    logout(request)
    return redirect("/")

def index(request):
	context={}
	context['blog_category']=category.objects.all()
	return render(request,"blog/index.html",context)

@csrf_exempt
def signup(request):
	context={}
	if request.method == "POST":
		email=request.POST.get('email')
		firstname=request.POST.get('firstname')
		lastname=request.POST.get('lastname')
		summary=request.POST.get('summary')
		password=request.POST.get('password')
		if check_blank_or_null([email,firstname,lastname,summary,password]):
			if User.objects.filter(username=email).exists():
				context['status']="already exists"
			else:
				user=User.objects.create_user(username=email,first_name=firstname,last_name=lastname,password=password,email=email)
				user.save()
				acc=account.objects.create(user=user,summary=summary)
				acc.save()
				context['status']="successfully"
		else:
			context['status']='Any Field can not be empty'
	else:
		context['status']="Get Method Is not Allowed Please enjoy our blogs"
	return JsonResponse(context)

@login_required()
def addblog(request):
	context={}
	context['blog_category']=category.objects.all()
	context['cat']=category.objects.all()
	if request.method == "POST":
		title = request.POST.get("title")
		description = request.POST.get("description")
		readtime = request.POST.get("readtime")
		titleimage = request.FILES['titleimage']
		category_id=request.POST.get("category_id")
		content_data=request.FILES.getlist("content_data")
		content=request.POST.getlist("content")
		blogtag=request.POST.getlist("blogtag")
		if check_blank_or_null([title,description,readtime,title,readtime,category_id]) and readtime.isdigit():
			if check_length([[title,500],[description,1000]]) and len(content) == len(content_data):
				if blog.objects.filter(title=title).exists():
					context['status']="Title Exists .Please Change Title of blog"
				else:
					if category.objects.filter(pk=category_id).exists():
						b=blog.objects.create(user=request.user)
						b.title=title
						b.description=description
						b.read_time=readtime
						b.slugurl=slugify(title)
						b.image=titleimage
						b.category=category.objects.get(pk=category_id)
						for x,y in zip(content,content_data):
							bb=block.objects.create(blog=b)
							bb.content=x
							if y!="":
								bb.data=y
							bb.save()
						for z in blogtag:
							if z != "":
								t,_=tag.objects.get_or_create(name=z,slugurl=slugify(z))
								t.save()
								tt,__=blog_tag.objects.get_or_create(blog=b,tag=t)
								tt.save()
						b.save()
						context['status']="your blog has been successfully publish"
					else:
						context['status']="category is not exists"
			else:
				context['status']="Your input data"				
	return render(request,'blog/add_blog.html',context)	


def blog_by_category(request,slugurl):
	context={}
	context['blog_category']=category.objects.all() 
	if category.objects.filter(slugurl=slugurl).exists():
		cat=category.objects.get(slugurl=slugurl)
		blogs=[]
		like_count=[]
		comment_count=[]
		view_count=[]
		print(cat)
		if blog.objects.filter(category=cat).count() < 10:
			for x in blog.objects.filter(category=cat).reverse():
				print(str(x.date).split(" ")[0].split("-"))
				blogs.append(x)
				like_count.append(like.objects.filter(blog=x).count())
				comment_count.append(comment.objects.filter(blog=x).count())
				view_count.append(views.objects.filter(blog=x).count())
		else:
			for x in blog.objects.filter(category=cat).reverse()[0:10]:
				blogs.append(x)
				like_count.append(like.objects.filter(blog=x).count())
				comment_count.append(comment.objects.filter(blog=x).count())
				view_count.append(views.objects.filter(blog=x).count())
		context['blog']=zip(blogs,like_count,comment_count,view_count)
		context['cat']=cat
	return render(request,'blog/blog.html',context)	


def details_blog(request,slugurl):
	context={}
	if blog.objects.filter(slugurl=slugurl).exists():
		b=blog.objects.get(slugurl=slugurl)
		blockO=[]
		extension=[]
		file_name=[]
		for x in block.objects.filter(blog=b):
			blockO.append(x)
			extension.append(str(x.data).split(".")[-1])
			file_name.append(str(x.data))
		context['details']=zip(blockO,extension,file_name)
		context['blog_details']=b
	return render(request,'blog/single.html',context)			

