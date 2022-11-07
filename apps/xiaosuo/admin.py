from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.

from .models import *

admin.site.site_title = 'sis001资源后台'
admin.site.site_header = "sis001资源后台"


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'authur', 'introduction', 'collection', 'category', 'classification', 'plate', 'index',
                    'user', 'crawling_status', 'date_joined']

    search_fields = ['name', 'collection__name', 'authur', 'introduction', 'content', 'url']
    list_filter = ['crawling_status', 'classification', 'plate']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数

    actions = ['updata_crawling_status']

    def updata_crawling_status(self, request, queryset):
        updated = queryset.update(crawling_status=False)
        self.message_user(request, ngettext(
            '%d 个数据已更新为“未爬取”',
            '%d 个数据已发布',
            updated,
        ) % updated, messages.SUCCESS)

    updata_crawling_status.short_description = "更新下载状态为”未下载“"


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'authur', 'category', 'classification', 'plate', 'introduction', 'is_look_count']

    search_fields = ['name', 'authur', 'introduction', 'classification__name']
    list_filter = ['classification', 'plate']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'bk']
    # # list_editable 设置默认可编辑字段
    # list_editable = ['bk']

    search_fields = ['name']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class PlateAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']

    search_fields = ['name']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class CollectionCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'collection', 'count', 'addbook', 'collect', 'yikan']

    search_fields = ['user__username', 'collection__name']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class UserToVisitHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'lishi']

    search_fields = ['user__username']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class VisitHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'url']

    search_fields = ['user__username', "url"]

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class ChapterCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'count', 'dow_code', 'look_code', 'end_code']

    # search_fields = ['user__name', "chapter__name", "chapter__collection__name"]
    search_fields = ["chapter__name", "chapter__collection__name"]

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Plate, PlateAdmin)
admin.site.register(CollectionCount, CollectionCountAdmin)
admin.site.register(UserToVisitHistory, UserToVisitHistoryAdmin)
admin.site.register(VisitHistory, VisitHistoryAdmin)
admin.site.register(ChapterCode, ChapterCodeAdmin)
