from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.utils import timezone

from .models import Post


def get_post_queryset(request_user=None, profile_user=None) -> QuerySet:
    queryset = Post.objects.select_related(
        'category', 'location', 'author'
    ).annotate(comment_count=Count('comments'))
    if profile_user:
        queryset = queryset.filter(author=profile_user)
    if request_user != profile_user:
        queryset = queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    return queryset.order_by('-pub_date')


def get_paginated_page(queryset: QuerySet, request) -> Paginator.page:
    paginator = Paginator(queryset, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
