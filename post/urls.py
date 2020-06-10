from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('blog/', views.blog, name = 'blog'),
    path('blog/search/', views.search, name = 'search'),
    path('blog/post/<int:post_id>', views.post, name = 'post'),
    path('blog/meme/<int:meme_id>', views.meme, name = 'meme'),
]