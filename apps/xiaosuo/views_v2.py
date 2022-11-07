# uni-app前端v2 api

from .serializers import *
from .filters import *
from .models import *
from users.models import UserProfile

from django.db.models import Q
from django.shortcuts import render

from rest_framework import viewsets, mixins, permissions, filters, views, serializers
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


def index(request):
    return render(request, 'index.html')


class ListSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class Index(views.APIView):

    def get(self, request):
        data_list = []
        bankuai = Plate.objects.all()
        for plate in PlateSerializer(bankuai, many=True, context={'request': request}).data:
            coll_data = Collection.objects.filter(plate=plate["id"]).order_by("-is_look_count")
            plate["books"] = CollectionSerializer(coll_data, many=True, context={'request': request}).data[:3]
            data_list.append(plate)
        tuijian_list = CollectionSerializer(Collection.objects.all().order_by("-is_look_count")[:3], many=True,
                                            context={'request': request}).data
        return Response({"tuijian": tuijian_list, "list": data_list}, status=200)


# 判断书籍是否已看的路由
class YiKan(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def get(self, request):
        bookid = request.GET.get("bookid")
        book = Collection.objects.get(id=bookid)
        user_book = CollectionCount.objects.filter(user=request.user, collection=book)[0]
        user_to_zj = ChapterCode.objects.filter(user=request.user, chapter__collection=book)
        if user_to_zj.count() == Chapter.objects.filter(collection=book).count():
            if not user_to_zj.filter(look_code__lt=1).count():
                user_book.yikan = True
                user_book.save()
        return Response(data={"code": 200, "mess": "成功"}, status=200)


class BookInfo(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    # serializer_class = CollectionSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction']
    ordering_fields = ['user', 'name', 'category', 'classification', 'plate', 'date_joined', 'update_time', 'is_look_count']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     for data in self.queryset:
    #         print(data.chapter_set.filter(crawling_status=False))
    #     return self.queryset.filter(chapter__crawling_status=True)

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionGetSerializer
        return CollectionSerializer

    # def update(self, request, *args, **kwargs):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_look_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 章节
class ZhangJieInfo(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ChapterFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction', 'content']
    ordering_fields = ['user', 'name', 'index', 'category', 'classification', 'plate', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(crawling_status=True)


# 用户书籍
class UserToBook(viewsets.ModelViewSet):
    queryset = CollectionCount.objects.all()
    # serializer_class = CollectionCountSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionCountFilter
    search_fields = ['user__username', 'collection__name']
    ordering_fields = ['user', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        lishi = self.request.GET.get("ls")
        shouchang = self.request.GET.get("sc")
        shouchang_to_notlook = self.request.GET.get("sc_notlook")
        yk = self.request.GET.get("yk")
        if lishi:
            return self.queryset.filter(Q(user=self.request.user) & ~Q(jindu=None)).order_by("-update_time")
        if shouchang:
            return self.queryset.filter(user=self.request.user, collect=True)
        if shouchang_to_notlook:
            return self.queryset.filter(user=self.request.user, collect=True, yikan=False)
        if yk:
            return self.queryset.filter(user=self.request.user, collect=True, yikan=True).order_by("-update_time")
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionCountGetSerializer
        return CollectionCountSerializer


# 板块
class BanKuai(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    pagination_class = None  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = PlateFilter
    search_fields = ['user__username', 'name']
    ordering_fields = ['user', 'name', 'date_joined', 'update_time']

    def get_queryset(self):
        return self.queryset.filter(~Q(collection=None))


# 用户信息
class UserInfo(mixins.ListModelMixin, mixins.RetrieveModelMixin , viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoSerializer
    pagination_class = None  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = UserInfoFilter
    search_fields = ['username']
    ordering_fields = ['username', 'gender', 'date_joined', 'update_time']

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)

