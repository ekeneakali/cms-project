from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=120)
    profile_pic = models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Profile Picture')
    biography = models.TextField()

    def __str__(self):
        return self.team_name

    class Meta():
        verbose_name_plural='Our Team'

    def get_profile(self):
        if self.profile_pic:
            return self.profile_pic.url

class Category(models.Model):
    cat_name = models.CharField(max_length=30, verbose_name='Category Name')
    cat_desc = models.TextField(blank=True, null=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cat_name

    class Meta():
        verbose_name_plural = 'Category'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Upload an image')
    biography = models.TextField()

    def __str__(self):
        return self.biography

    class Meta():
        verbose_name_plural='Profile'


class Post(models.Model):
    pst_title = models.CharField(max_length=150)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pst_image = models.FileField(null=True, blank=True, upload_to='uploads/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    num_site = models.IntegerField(default=0, verbose_name='visited')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pst_title

    class Meta():
        verbose_name_plural = 'Post'
        
    def total_likes(self):
        return self.likes.count()


    


class Comment(models.Model):
    name = models.CharField(max_length=150)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.pst_title

    class Meta():
        verbose_name_plural = 'Comment'

class Reply(models.Model):
    name = models.CharField(max_length=150)
    comment = models.TextField()
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Reply'






class NewsLetter(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'NewsLetter'


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=700)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Contact'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Upload an image')
    biography = models.TextField()

    def __str__(self):
        return self.biography

    class Meta():
        verbose_name_plural='Profile'
