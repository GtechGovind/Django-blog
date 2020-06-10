from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

# USER
User = get_user_model()

class Author(models.Model):
    user            = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_picture   = models.ImageField(upload_to='profile_picture')

    def __str__(self):
        return self.user.username

# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

# POSTS
class Post(models.Model):
    post_id         = models.IntegerField(unique = True)
    title           = models.CharField(max_length = 100)
    author          = models.ForeignKey(Author, on_delete = models.CASCADE)
    overview        = models.TextField()
    body            = HTMLField()
    timestamp       = models.DateTimeField(auto_now_add=True)
    thumbnail       = models.ImageField(upload_to = 'post')
    category        = models.ManyToManyField(Category)
    view_count      = models.IntegerField(blank = True)
    featured        = models.BooleanField()

    def __str__(self):
            return self.title + ' | ' + str(self.author.user.username) + ' | ' + str(self.post_id)

# MEME
class Meme(models.Model):
    meme_id   = models.IntegerField(unique = True)
    meme      = models.ImageField(upload_to = 'meme')
    view_count      = models.IntegerField(blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    source    = models.CharField(max_length = 100)
    category  = models.OneToOneField(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.source + ' | ' + str(self.meme_id)

# COMMENTS
class Comments(models.Model):
    username    = models.CharField(max_length = 100)
    useremail   = models.EmailField(blank = True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    usercomment = models.TextField()
    post        = models.ForeignKey(Post, on_delete = models.CASCADE)
    def __str__(self):
        return self.username