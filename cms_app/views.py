
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from . forms import *

from .models import *

from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
import os
from .forms import SetPasswordForm
from .forms import PasswordResetForm

 
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.core.paginator import Paginator
import copy
from django.conf import settings
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import permission_required

# Create your views here.

def home(request):
    latest_post = Post.objects.all().order_by('-created_at')
    return render(request, 'cms_app/index.html', {'latest':latest_post})

def about(request):
    team = Team.objects.all()
    return render(request, 'cms_app/about.html', {'team':team})

def about_detail(request, abt_id):
    team_detail = Team.objects.get(id=abt_id)
    return render(request, 'cms_app/detail.html', {'detail':team_detail})

def post_list(request):
    post = Post.objects.all().order_by('-created_at')
    return render(request, 'cms_app/post-list.html', {'show_post':post})

def single_post(request, post_id):
    single = Post.objects.get(id=post_id)
    
    get_comment = Comment.objects.filter(post__id=post_id).order_by('-created_at')[:3]
    
    if request.method == 'POST':
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        Comment.objects.create(name=name, comment=comment, post=single)
        messages.success(request, 'Comment created')
    
    single.num_site = single.num_site + 1
    single.save()

    is_liked = False
    if single.likes.filter(id=request.user.id).exists():
        is_liked = True
    
    

    
    return render(request, 'cms_app/single-blog.html', {'single':single, 'comment':get_comment, 'is_liked':is_liked, 'total_likes':single.total_likes, 'profile':profile})

def comment_detail(request, id):

    comment_reply = Comment.objects.get(pk=id)

    reply = Reply.objects.filter(reply__pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        Reply.objects.create(name=name, comment=comment, reply=comment_reply)
        messages.success(request, 'Thanks for replying')
    

    return render(request, 'cms_app/comment-reply.html', {'comment_reply':comment_reply, 'reply':reply})

def like_blog(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
        messages.success(request, 'You have dislike this post')
    else:

        post.likes.add(request.user)
        is_liked = True
        messages.success(request, 'thank you for liking this post')
            
    return HttpResponseRedirect(reverse('cms_app:single_post', args=[str(pk)]))
def subscribe_user(request, pk):
    post = get_object_or_404(Profile, id=request.POST.get('post_id'))
    is_liked = False
    if post.subscribe.filter(id=request.user.id).exists():
        post.subscribe.remove(request.user)
        is_liked = False
        messages.success(request, 'Subscription remove successfully')
    else:

        post.subscribe.add(request.user)
        is_liked = True
        messages.success(request, 'Subscription addedd successfully')
            
    return HttpResponseRedirect(reverse('cms_app:profile_detail', args=[str(pk)]))



def post_from_cat(request, cat_id):
    count = Post.objects.filter(category__id=cat_id).count()
    single = Category.objects.get(id=cat_id)
    post_cat = Post.objects.filter(category__id=cat_id)
    return render(request, 'cms_app/post-cat.html', {'post':post_cat, 'count':count, 'single':single})


def service(request):
    return render(request, 'cms_app/services.html')

def profile(request):

    profile = Profile.objects.filter(user=request.user)

    post = Post.objects.filter(user=request.user).count()
    return render(request, 'cms_app/profile.html', {'profile':profile, 'post':post})

def edit_pic(request):

    profile = Profile.objects.filter(user=request.user)
    return render(request, 'cms_app/edit-pic.html', {'profile':profile})


def profile_form(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            messages.success(request, 'Profile added successfully ')
            return redirect('cms_app:profile') 

    else:
        form = ProfileForm()

    return render(request, "cms_app/profile-form.html", {'form':form})
def profile_detail(request, id):
    if not request.user.is_authenticated:
        messages.success(request, 'Login to continue')
        return redirect('cms_app:custom_login')
        
    profile = Profile.objects.get(pk=id)
    post = Post.objects.filter(user_id=id)
    profile_count = Post.objects.filter(user=request.user).count()

    is_liked = False
    if profile.subscribe.filter(id=request.user.id).exists():
        is_liked = True
    
    
    return render(request, 'cms_app/profile-detail.html', {'profile':profile, 'post':post, 'profile_count':profile_count, 'is_liked':is_liked, 'total_subscribe':profile.total_subscribe})

def post_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            messages.success(request, 'Post added successfully ')
            return redirect('cms_app:post_view') 

    else:
        form = PostForm()

    return render(request, "cms_app/post-form.html", {'form':form})



def post_view(request):

    view_post = Post.objects.filter(created_by=request.user)

    return render(request, "cms_app/view-post.html", {'view_post':view_post})


def edit_post(request, id):
    edit = Post.objects.get(pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=edit)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            messages.success(request, 'Post edited successfully ')
            return redirect('cms_app:post_view') 

    else:
        form = PostForm(instance=edit)

    return render(request, "cms_app/edit-post.html", {'form':form})
        

def del_post(request, id):

    post = Post.objects.get(pk=id)

    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('cms_app:post_view') 


def edit_form(request, id):

    edit = Profile.objects.get(pk=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=edit)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            messages.success(request, 'Profile edited successfully ')
            return redirect('cms_app:profile') 

    else:
        form = ProfileForm(instance=edit)

    return render(request, "cms_app/edit-profile-form.html", {'form':form})

def profile_delete(request, id):

    profile_del = Profile.objects.get(pk=id)

    profile_del.delete()

    messages.success(request, 'Profile picture deleted successfully')
    return redirect('cms_app:profile')
        


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('cms_app:register')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = Register()

    return render(request, "cms_app/register.html", {'form':form})
        


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('cms_app/account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
def activate(request, uidb64, token):
    user = User()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('cms_app:custom_login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('home')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello {user.username} You have been logged in")

                return redirect('home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm() 
    
    return render(request, "cms_app/login.html", {'form': form}
        )
# Same as in all places where we request some input from the user, we use the POST method; not an exception is the login function. We use the built-in Django Authentication form to receive the username and password from the user and check if it's valid. If the form is valid, we call the built-in Django authentication function that checks if such a 

def custom_logout(request):
    
    logout(request)
    
    messages.success(request, 'Log out successfully!')
    return redirect('cms_app:custom_login')

def confirm_logout(request):

    return render(request, 'cms_app/confirm-logout.html')

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('cms_app:custom_login')

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile edited successfully')
            return redirect('cms_app:profile')
        else:
            messages.error(request, 'user not edited')
    else:
        form = EditProfile(instance=request.user)


    return render(request, 'cms_app/edit-profile.html', {'form':form})


def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('cms_app:custom_login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'cms_app/password_reset_confirm.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("cms_app/reset.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(request, "cms_app/password_reset.html", {"form": form}
        )
def passwordResetConfirm(request, uidb64, token):
    user = User()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('cms_app:custom_login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'cms_app/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")

def news(request):
        if request.method == 'POST':
            email = request.POST.get('email')
        
        NewsLetter.objects.create(email=email)
        send_mail(
            email,
            email,
            'belletrade55@gmail.com',
            ['waltrade42@gmail.com'],
            fail_silently=False,
            
        )
        messages.success(request, 'thanks for subscribing!')
        # return redirect('cms_app:base')
    

    
        return render(request, "cms_app/base.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            description = form.cleaned_data.get('description')
            send_mail(
            email,
            description,
            'akaliekene42@gmail.com',
            ['waltrade42@gmail.com'],
            fail_silently=False,
            
        )

            messages.success(request, 'mail sent succesfully')
            return redirect('cms_app:contact')

    else:
        form = ContactForm()

    return render(request, "cms_app/contact.html", {"form": form}
        )

def category(request):

    category = Category.objects.all()

    return render(request, "cms_app/category.html", {"category": category}
        )

def category_detail(request, id):

    category = Category.objects.get(pk=id)

    post = Post.objects.filter(category=category)

    return render(request, "cms_app/category-detail.html", {"category": category, 'post':post}
        )



