"""sis001_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

from rest_framework.authtoken import views

from users.views import *
from xiaosuo.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'lishi', VisitHistoryViewsSet)
router.register(r'book', CollectionViewsSet)
router.register(r'zhangjie', ChapterViewsSet)
router.register(r'fenlei', ClassificationViewsSet)
router.register(r'bankuai', PlateViewsSet)
router.register(r'user_url', UserToVisitHistoryViewsSet)
router.register(r'user_coll', CollectionCountViewsSet)
router.register(r'user_zj', ChapterCodeViewsSet)

from xiaosuo.views import PanDuan, Cn2An, Add_LiShi, Add_ZhangJie
from xiaosuo.views_v2 import Index, BookInfo, ZhangJieInfo, UserToBook, BanKuai, UserInfo, YiKan, index

urlpatterns = [
    path('admin/', admin.site.urls),     # 后台路径
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # 静态文件路径拼接
    # path('api-token-auth/', views.obtain_auth_token),
    # drf路由↓
    path(r'api/doc', include_docs_urls(title='API_DOC')),     # api测试接口
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # restframework认证路由，用于drf登录、注销页面的
    path('api/login', Login.as_view()),  # drf自带token登录验证
    path('api/v1/', include(router.urls)),     # 加载api路由
    path('api/panduan', PanDuan.as_view(), name="panduan"),     # 列表页判断接口
    path('api/cn2an', Cn2An.as_view(), name="cn2an"),     # 中文转数字
    path('api/add_lishi', Add_LiShi.as_view(), name="add_lishi"),
    path('api/add_zhangjie', Add_ZhangJie.as_view(), name="add_zhangjie"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]  # 静态文件路径拼接]
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]  # 静态文件路径拼接]

# handler404 = "accounts.views.page_not_found"
# handler500 = "accounts.views.error"

# uni-app v2 api
router_v2 = routers.DefaultRouter(trailing_slash=False)
router_v2.register(r'book_v2', BookInfo)
router_v2.register(r'zhangjie_v2', ZhangJieInfo)
router_v2.register(r'user_book_v2', UserToBook)
router_v2.register(r'bankuai_v2', BanKuai)
router_v2.register(r'user_zj_v2', ChapterCodeViewsSet)
router_v2.register(r'user_info_v2', UserInfo)
uni_app_v2 = [
    path('api/v2/', include(router_v2.urls)),     # 加载api路由
    path("api/v2/index_v2", Index.as_view(), name="index_v2"),
    path("api/v2/yikan_v2", YiKan.as_view(), name="yikan_v2"),
]


urlpatterns += uni_app_v2


urlpatterns += [path('', index, name='index')]
