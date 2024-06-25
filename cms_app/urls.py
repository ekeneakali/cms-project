from django.urls import path
from cms_app import views


app_name="cms_app"

urlpatterns = [
    path('', views.about, name='about'),
    path('about-detail/<int:abt_id>/', views.about_detail, name='ekene_detail'),
    path('service-page/', views.service, name='service'),
    path('posts/', views.post_list, name='post_list'),
    path('single-post/<int:post_id>/', views.single_post, name='single_post'),
    path('post-from-cat/<int:cat_id>/', views.post_from_cat, name='post_from_cat'),
    path('contact/', views.contact, name='contact'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('activateEmail', views.activateEmail, name='activateEmail'),
    path('register', views.register, name='register'),
    path('login', views.custom_login, name='custom_login'),
    path('custom_logout', views.custom_logout, name='custom_logout'),
    path('confirm_logout', views.confirm_logout, name='confirm_logout'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('category', views.category, name='category'),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
    path('news', views.news, name='news'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('comment_detail/<int:id>/', views.comment_detail, name='comment_detail'),
    path('like_blog/<int:pk>/', views.like_blog, name='like_blog'),
    path('profile-form', views.profile_form, name='profile_form'),
    path('edit-pic', views.edit_pic, name='edit_pic'),
    path('edit-form/<int:id>/', views.edit_form, name='edit_form'),
    path('profile-delete/<int:id>/', views.profile_delete, name='profile_delete'),
]