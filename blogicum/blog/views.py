from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, RegisterForm, UserEditForm
from .models import Category, Comment, Post
from .utils import get_paginated_page, get_post_queryset


def index(request):
    post_list = get_post_queryset(request.user)
    page_obj = get_paginated_page(post_list, request)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = get_post_queryset(request.user).filter(category=category)
    page_obj = get_paginated_page(post_list, request)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = get_post_queryset(request.user, profile)
    page_obj = get_paginated_page(post_list, request)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    form = UserEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=user.username)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('blog:index')
    context = {'form': form}
    return render(request, 'registration/registration_form.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        if not (
            post.is_published
            and post.pub_date <= timezone.now()
            and post.category.is_published
        ):
            return render(request, 'pages/404.html', status=404)
    form = CommentForm()
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(
            'blog:profile',
            username=request.user.username
        )
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': comment, 'form': form, 'is_edit': True}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)
