from django.shortcuts import render

# Create your views here.
import cn2an
from .serializers import *
from .filters import *
from .models import *

# from django.http import HttpResponse
# from django.views.generic.base import View

from rest_framework import viewsets, mixins, permissions, filters, views
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.views import APIView
from rest_framework.response import Response


# from rest_framework import status


class Cn2An(views.APIView):
    """
    中文转数字
    """
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def get(self, request):
        text = request.GET.get("text")
        if text:
            try:
                output = cn2an.transform(str(text), "cn2an")
                return Response(data={"code": 200, "mess": "成功", "data": output}, status=200)
            except Exception as e:
                return Response(data={"code": 422, "mess": "错误", "data": e}, status=422)
        else:
            return Response(data={"code": 404, "mess": "请传递text参数", "data": None}, status=404)


class Add_LiShi(views.APIView):
    """
    用户没有当前网址的浏览记录，增加记录
    """
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def get(self, request):
        url_str = request.GET.get("url")
        if not url_str:
            return Response(data={"mess": "错误，未传递URL", "code": 422, "data": False}, status=422)
        url_data = VisitHistory.objects.filter(url=url_str)
        if url_data.count():
            lishi = url_data[0]
            user_to_lishi = UserToVisitHistory(user=request.user, lishi=lishi)
            user_to_lishi.save()
            return Response(data={"code": 200, "mess": "用户加入历史记录成功", "data": True}, status=200)
        else:
            lishi = VisitHistory(url=url_str, user=request.user)
            lishi.save()
            user_to_lishi = UserToVisitHistory(user=request.user, lishi=lishi)
            user_to_lishi.save()
            return Response(data={"code": 200, "mess": "创建历史记录，并添加用户历史记录成功", "data": True}, status=200)


class Add_ZhangJie(views.APIView):
    """
    保存章节与书籍
    """
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def post(self, request):
        type_str = request.query_params.get('type')
        data = request.data
        if not type_str:
            return Response(data={"mess": "错误，未传递type", "code": 422, "data": False}, status=422)
        if type_str == "save":
            book_data = Collection.objects.filter(name=data["book_name"].strip())
            if book_data.count():
                """书籍存在，需要创建章节的情况"""
                book_data = book_data[0]
                mess = "书籍存在，但章节不存在，已创建章节，并收藏书籍"
                zhangjie = Chapter(name=data["title_name"],
                                   user=request.user,
                                   collection=book_data,
                                   category=data["type"],
                                   url=data["url"],
                                   index=data["index"])
                zhangjie.save()
                user_book = CollectionCount.objects.filter(user=request.user, collection=book_data)
                user_book.update(collect=True)
            else:
                """书籍不存在，需要创建书籍，并创建张继，最后与用户关联的情况"""
                book_data = Collection(user=request.user, name=data["book_name"], category=data["type"])
                book_data.save()
                mess = "书籍不存在，创建书籍，章节不存在，创建章节，并关联用户书籍与章节"
                zhangjie = Chapter(name=data["title_name"],
                                   user=request.user,
                                   collection=book_data,
                                   category=data["type"],
                                   url=data["url"],
                                   index=data["index"])
                zhangjie.save()
                user_book = CollectionCount(user=request.user, collection=book_data, collect=True)
                user_book.save()
            return Response(data={"code": 200, "mess": mess, "data": True}, status=200)
        if type_str == "shouchang":
            """章节、书籍都存在，但是用户并没有收藏的情况"""
            coll = CollectionCount.objects.filter(user=request.user, collection__chapter__url=data["url"])
            if coll.count():
                """存在用户关联，但是用户并未收藏的情况"""
                user_book = Collection.objects.filter(user=request.user, collection__chapter__url=data["url"])
                user_book.update(collect=True)
                mess = "已更新用户收藏"
            else:
                """不存在用户关联，需要创建用户关联的情况"""
                book_data = Collection.objects.filter(chapter__url=data["url"])
                if book_data.count():
                    book_data = book_data[0]
                    user_book = CollectionCount(user=request.user, collection=book_data, collect=True)
                    user_book.save()
                    mess = "已创建用户收藏"
                else:
                    return Response(data={"code": 404, "mess": "不存在书籍，请创建后在收藏", "data": False}, status=404)
            return Response(data={"code": 200, "mess": mess, "data": True}, status=200)
        return Response(data={"code": 422, "mess": "错误，未开发", "data": False}, status=422)


class PanDuan(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def get(self, request, format=None):
        type_str = request.GET.get("type")
        url_str = request.GET.get("url")
        if not type_str:
            return Response(data={"mess": "未传递类型"}, status=422)

        if not url_str:
            return Response(data={"mess": "错误，未传递URL"}, status=422)

        if type_str == "xiaosuo":
            xiaosuo = False
            lishi = False
            url_zz = str(url_str).split("/")[-1].split("-")
            url_zz = f"\S*{url_zz[0]}-{url_zz[1]}\S*"
            if UserToVisitHistory.objects.filter(user=request.user, lishi__url__regex=url_zz):
                lishi = True

            # if VisitHistory.objects.filter(url=url_str):
            #     lishi = True

            if CollectionCount.objects.filter(user=request.user, collect=True, collection__chapter__url__regex=url_zz):
                xiaosuo = True

            # if Chapter.objects.filter(url=url_str):
            #     xiaosuo = True
            data = {
                "mess": "成功",
                "data": {
                    "xiaosuo": xiaosuo,
                    "lishi": lishi
                }
            }
            return Response(data=data, status=200)
        else:
            return Response(data={"mess": "该类型未开发"}, status=404)


class ListSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class VisitHistoryViewsSet(viewsets.ModelViewSet):
    queryset = VisitHistory.objects.all()
    serializer_class = VisitHistorySerializer  # 控制显示字段
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = VisitHistoryFilter  # 控制可以筛选的字段
    search_fields = ['user__username', 'url']
    ordering_fields = ['user', 'url', 'date_joined', 'update_time']

    # 超级管理员显示全部，其他显示自己的数据
    def get_queryset(self):
        if self.request is not None:
            if self.request.user.is_superuser:
                return self.queryset
            else:
                return self.queryset.filter(user=self.request.user)
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionViewsSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    # serializer_class = CollectionSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction']
    ordering_fields = ['user', 'name', 'category', 'classification', 'plate', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionGetSerializer
        return CollectionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_look_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ChapterViewsSet(viewsets.ModelViewSet):
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


class ClassificationViewsSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ClassificationFilter
    search_fields = ['user__username', 'name']
    ordering_fields = ['user', 'name', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlateViewsSet(viewsets.ModelViewSet):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = PlateFilter
    search_fields = ['user__username', 'name']
    ordering_fields = ['user', 'name', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserToVisitHistoryViewsSet(viewsets.ModelViewSet):
    queryset = UserToVisitHistory.objects.all()
    serializer_class = UserToVisitHistorySerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = UserToVisitHistoryFilter
    search_fields = ['user__username', 'lishi__url']
    ordering_fields = ['user', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request is not None:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.all()


class CollectionCountViewsSet(viewsets.ModelViewSet):
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
        # print(self.request.method == "GET")
        if self.request is not None:
            return self.queryset.filter(user=self.request.user, collect=True)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionCountGetSerializer
        return CollectionCountSerializer


class ChapterCodeViewsSet(viewsets.ModelViewSet):
    queryset = ChapterCode.objects.all()
    serializer_class = ChapterCodeSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ChapterCodeFilter
    search_fields = ['user__username', 'chapter__name']
    ordering_fields = ['user', 'chapter', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # print(self.request.method == "GET")
        # if self.request is not None:
        #     return self.queryset.filter(user=self.request.user)
        # return self.queryset.all()

        return self.queryset.filter(user=self.request.user)

    # def partial_update(self, request, *args, **kwargs):

    # def get_serializer_class(self):
    #     if self.request is not None:
    #         if self.request.method == "GET":
    #             return CollectionCountGetSerializer
    #     return CollectionCountSerializer
