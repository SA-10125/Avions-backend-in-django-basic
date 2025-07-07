from django.shortcuts import render, redirect
from django.contrib import messages #this is what we import to get flash messages.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout #imported for the user login
from django.contrib.auth.decorators import login_required,user_passes_test #this is used to restrict pages that need login or a certain login.
from .models import team_member,gallery_name, Blog
#from csv import reader #used to read from deleted_data.csv (an idea)

# Create your views here.

def render_simple_homepage(request):
    context={}
    team = team_member.objects.all() #inlcudes images as byte64 (images are in static, can change later.)
    gallery_pics = gallery_name.objects.all() #is image loaction in static
    context={"team_members": team, 'gallery':gallery_pics,}
    return render(request, 'home.html', context)

#You put image in server in static folder.
#Then you take the location relative to static and put it into the image charfield (in backend/website (/admin), not directly.)
#then it will render itself everywhere i have rendered gallery.
#same way for team members. tell me what else yall need and i will do that also accordingly.

#not reccomended:
#Theres another way to render images. you could store them in database as a long byte64 encryted string and render it on user's screen everytime (increases loading time cause its client side rendering)
#import base64
#     for i in team:
#         i.image=encode_image_to_base64(i.imagepath)
#         i.save()
# def encode_image_to_base64(image_path):
#     try:
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode("utf-8")
#     except:
#         return image_path
# #In the HTML, I loaded the images as: <img src="data:image/png;base64,{{ member.image }}" alt="{{ member.name }}" class="rounded-full mx-auto mb-4" width="200" height="200">

def login_page(request): #can add login feautures like error handling
    if request.user.is_authenticated:
        return(redirect('home'))
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user=User.objects.filter(username=username)
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                # Fallback to a specific URL, e.g., the home page
                return redirect('home') #Change this to whatever url you want them to go to after login pls
        else:
            messages.info(request,'Username or password is incorrect.')
    return render(request,'login.html')

@login_required(login_url='login')
def logout_page(request):
    #consider general data record(logouts)?
    logout(request)
    return(redirect('home'))


#if needed, i can make another app for this just like home (end product is same but this function would be in a different folder.)
#that helps with cleaner codebase sometimes and also with scalability (its mainly for readablity purpose)
def render_gallery(request): 
    context={'gallery':gallery_name.objects.all()}
    return render(request,'gallery.html',context)

#(Guys, this is just to show you that this feauture is possible. Could even make a chat room for members logged in in the website if you want or whatever.)
@login_required(login_url='login') #must be logged in to access events. 
def render_events(request):
    if request.user.is_authenticated: #precautionary even though we have the login_required decorator.
        context={}
        return(render(request,'events.html',context))
    else:
        return redirect('login')
    
def render_contact_us(request):
        context={}
        return(render(request,'contact_us.html',context))

#TODO:  #get the notify buttonw working.
        #load blogs like we did events in dajango_try. 
        #each blog should be a get send to a pk page. (simple like in dajango)

def render_about_us_page(request):
        return render(request,"temp_about.html")


def render_blogs(request):
    context={"is_superuser": False, "user": False,"blogs":[]}

    if request.user.is_authenticated:
        context["user"]=request.user
        if request.user.is_superuser:
            context["is_superuser"]=True

    for blog in Blog.objects.all():
        context["blogs"].append(blog)

    return render(request, 'blogs.html',context)

def read_blog(request,pk):
    context={"is_superuser": False, "user": False,"blog":None}

    if request.user.is_authenticated:
        context["user"]=request.user #add if the user is the author of the blog in html etc.
        if request.user.is_superuser:
            context["is_superuser"]=True

    context["blog"]=Blog.objects.get(title=pk) #might change this to UID if needed.

    return render(request, 'read_blog.html',context)

@login_required(login_url='login') #users can write blogs
def write_blog(request):
    context={"is_superuser": False, "user": False}

    if request.user.is_authenticated:
        context["user"]=request.user
        if request.user.is_superuser:
            context["is_superuser"]=True

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        author = request.user

        blog = Blog(title=title,desc=desc,content=content,author=author)
        blog.save()

        return redirect('blogs')

    return render(request, 'write_blog.html',context)

@login_required(login_url='login') #users can edit their blogs only
def edit_blog(request,pk): 
    context={"is_superuser": False, "user": False,"blog":None}

    if request.user.is_authenticated:
        context["user"]=request.user
        if request.user.is_superuser:
            context["is_superuser"]=True

    context["blog"]=Blog.objects.get(title=pk) #might change this to UID if needed.
    if context["blog"].author != request.user:
        return redirect('blogs')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        author = request.user

        context["blog"].title = title
        context["blog"].desc = desc
        context["blog"].content = content
        context["blog"].save()

        return redirect('blogs')

    return render(request, 'edit_blog.html',context)

@user_passes_test(lambda u: u.is_superuser) #admins can delete blogs
def delete_blog(request,pk):
    context={"is_superuser": False, "user": False,"blog":None}

    if request.user.is_authenticated:
        context["user"]=request.user
        if request.user.is_superuser:
            context["is_superuser"]=True

    context["blog"]=Blog.objects.get(title=pk) #might change this to UID if needed.

    context["blog"].delete()

    return redirect('blogs')