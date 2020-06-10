from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from . models import *
from django.db.models import Q


# COMMON DECLARATION
#POST
LATEST_POSTS   = Post.objects.all().order_by('-timestamp')

# MEME
LATEST_MEMES   = Meme.objects.all().order_by('-timestamp')

# ASIDE POST
FEATURED_POSTS =  Post.objects.filter(featured = True).order_by('-timestamp')[:5]

# ASIDE CATEGORIES
CATEGORIES = Category.objects.all()

# ASIDE MEME
ASIDE_LATEST_MEMES = LATEST_MEMES[:5]

def search(request):

    # SEARCH
    QUERYSET_POST = Post.objects.all()
    QUERYSET_MEME = Meme.objects.all()
    query_un = request.GET.get('search')
    query = query_un.split("/")[0]
    QUERY = str(query).upper()

    # SEARCH  POST
    if query:
        QUERYSET_POST = QUERYSET_POST.filter(
                Q(title__icontains = query) | Q(overview__icontains = query) | Q(body__icontains = query) |
                Q(category__name__icontains = query)
            ).distinct().order_by('-timestamp')

    # SEARCH PAGINATION POST
    paginator_post = Paginator(QUERYSET_POST, 4)
    page_request_var = 'page'
    try:
        page = query_un.split("/")[1].split("=")[1]
    except:
        page = request.GET.get(page_request_var)
        
    try:
        paginated_queryset_post = paginator_post.page(page)
    except PageNotAnInteger:
        paginated_queryset_post = paginator_post.page(1)
    except EmptyPage:
        paginated_queryset_post = paginator_post.page(paginator.num_page)

    # SEARCH QUERYSET MEME
    if query:
        QUERYSET_MEME = QUERYSET_MEME.filter(
                Q(source__icontains = query) | Q(category__name__icontains = query)
        ).distinct().order_by('-timestamp')

    # SEARCH PAGINATION POST
    paginator_meme = Paginator(QUERYSET_MEME, 1)
    page_request_var_meme = 'meme'
    try:
        page = query_un.split("/")[1].split("=")[1]
    except:
        page = request.GET.get(page_request_var)
        
    try:
        paginated_queryset_meme = paginator_meme.page(page)
    except PageNotAnInteger:
        paginated_queryset_meme = paginator_meme.page(1)
    except EmptyPage:
        paginated_queryset_meme = paginator_meme.page(paginator.num_page)


    return render(request, 'Search.html', { 'paginated_queryset_post': paginated_queryset_post, 'paginated_queryset_meme': paginated_queryset_meme,
                                            'QUERY': QUERY, 'CATEGORIES': CATEGORIES, 'LATEST_MEMES': LATEST_MEMES,
                                            'ASIDE_LATEST_MEMES': ASIDE_LATEST_MEMES, 'FEATURED_POSTS': FEATURED_POSTS,
                                            'page_request_var': page_request_var,  'page_request_var_meme': page_request_var_meme })

def home(request):

    # POSTS
    FEATURED_POSTS =  Post.objects.filter(featured = True).order_by('-timestamp')[:3]

    return render(request, 'home.html', { 'FEATURED_POSTS': FEATURED_POSTS, 'LATEST_POSTS': LATEST_POSTS[:3],
                           'LATEST_MEMES': LATEST_MEMES[:4]})

def blog(request):

    # PAGINATOR POST
    paginator_post = Paginator(LATEST_POSTS, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset_post = paginator_post.page(page)
    except PageNotAnInteger:
        paginated_queryset_post = paginator_post.page(1)
    except EmptyPage:
        paginated_queryset_post = paginator_post.page(paginator.num_page)

    # PAGINATOR MEME
    paginator_meme = Paginator(LATEST_MEMES, 1)
    page_request_var_meme = 'meme'
    page = request.GET.get(page_request_var_meme)
    try:
        paginated_queryset_meme = paginator_meme.page(page)
    except PageNotAnInteger:
        paginated_queryset_meme = paginator_meme.page(1)
    except EmptyPage:
        paginated_queryset_meme = paginator_meme.page(paginator.num_page)

    return render(request, 'blog.html', { 'paginated_queryset_post': paginated_queryset_post, 'FEATURED_POSTS': FEATURED_POSTS[:5],
                                          'CATEGORIES': CATEGORIES, 'paginated_queryset_meme': paginated_queryset_meme,
                                          'ASIDE_LATEST_MEMES': ASIDE_LATEST_MEMES,
                                          'page_request_var': page_request_var, 'page_request_var_meme': page_request_var_meme})

def post(request, post_id):

    post = Post.objects.get(post_id = post_id)

    # VIEW COUNT
    post.view_count += 1
    post.save()

    LAST_POST = Post.objects.last()
    LAST_POST_ID = LAST_POST.post_id

    if post_id < LAST_POST_ID:
        next_post = Post.objects.get(post_id = post_id + 1)
    else:
        next_post = False

    if post_id > 1:
        pre_post = Post.objects.get(post_id = post_id - 1)
    else:
        pre_post = False

    return render(request, 'post.html', { 'post': post, 'next_post': next_post, 'pre_post': pre_post,
    'FEATURED_POSTS': FEATURED_POSTS[:5], 'CATEGORIES': CATEGORIES, 'LATEST_MEMES': LATEST_MEMES[:5],
                                          'ASIDE_LATEST_MEMES': ASIDE_LATEST_MEMES })

def meme(request, meme_id):
    meme = Meme.objects.get(meme_id = meme_id)

    # VIEW COUNT
    meme.view_count += 1
    meme.save()

    LAST_MEME = Meme.objects.last()
    LAST_MEME_ID = LAST_MEME.meme_id

    if meme_id < LAST_MEME_ID:
        next_meme = Meme.objects.get(meme_id = meme_id + 1)
    else:
        next_meme = False

    if meme_id > 1:
        pre_meme = Meme.objects.get(meme_id = meme_id - 1)
    else:
        pre_meme = False

    return render(request, 'meme.html', { 'meme': meme, 'next_meme': next_meme, 'pre_meme': pre_meme,
    'FEATURED_MEMES': FEATURED_POSTS[:5], 'CATEGORIES': CATEGORIES, 'LATEST_MEMES': LATEST_MEMES[:5],
                                          'ASIDE_LATEST_MEMES': ASIDE_LATEST_MEMES, 'FEATURED_POSTS': FEATURED_POSTS[:5] })