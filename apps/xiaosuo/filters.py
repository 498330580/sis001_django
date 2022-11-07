# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
# from rest_framework import filters
# from django.db.models import Q
# from rest_framework.response import Response

from .models import *
from users.models import UserProfile


class VisitHistoryFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = VisitHistory
        fields = ['user', 'url']


class CollectionFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Collection
        fields = ['category', 'name', 'classification', 'plate', 'category']


class ChapterFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Chapter
        fields = ['name', 'url', 'collection', 'classification', 'plate', 'category', 'crawling_status']


class ClassificationFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Classification
        fields = ['user__username', 'name']


class PlateFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Plate
        fields = ['user__username', 'name']


class UserToVisitHistoryFilter(django_filters.rest_framework.FilterSet):
    username = django_filters.CharFilter(field_name='user__username', label="用户名")  # 跨表操作
    url = django_filters.CharFilter(field_name='lishi__url', label="url")  # 跨表操作

    class Meta:
        model = UserToVisitHistory
        fields = ['username', 'url']


class CollectionCountFilter(django_filters.rest_framework.FilterSet):
    username = django_filters.CharFilter(field_name='user__username', label="用户名")  # 跨表操作
    url = django_filters.CharFilter(field_name='collection__chapter__url', label="url")  # 跨表操作

    class Meta:
        model = CollectionCount
        fields = ['username', 'url', 'yikan', 'addbook', 'collect', 'collection']


class ChapterCodeFilter(django_filters.rest_framework.FilterSet):
    collection = django_filters.CharFilter(field_name='chapter__collection_id', label="书籍")  # 跨表操作
    # collection = django_filters.CharFilter(field_name='chapter__collection', label="书籍")  # 跨表操作

    class Meta:
        model = ChapterCode
        fields = ['user', 'chapter', 'end_code', 'collection']


class UserInfoFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['username', 'gender']
