from django.db import models
from users.models import UserProfile

# Create your models here.

TYPE = (
    (0, "无"),
    (1, "小说"),
    (2, "图片")
)


# Label = (
#     (0, "无"),
# )
#
# PLATE_TYPE = (
#     (0, "无"),
#     (1, "原创人生")
# )


# 版块
class Plate(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="板块", max_length=500)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


# 分类
class Classification(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="标签", max_length=500)
    bk = models.ForeignKey(Plate, verbose_name="板块", on_delete=models.SET_NULL, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


# 合集（BOOK)
class Collection(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", max_length=100, default="无")
    category = models.IntegerField(verbose_name="类别", choices=TYPE, default=0)
    classification = models.ForeignKey(Classification, verbose_name="分类", on_delete=models.SET_NULL, null=True,
                                       blank=True)
    plate = models.ForeignKey(Plate, verbose_name="板块", on_delete=models.SET_NULL, null=True, blank=True)
    introduction = models.TextField(verbose_name="简介", default="无")
    is_look_count = models.IntegerField(verbose_name="点击次数", default=0, help_text="记录书本被点击的次数")
    img = models.ImageField(upload_to='book_img/%Y/%m/%d',
                            default='img/book.png',
                            blank=True,
                            null=True,
                            verbose_name='封面')

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '合集'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lstrip()
        super().save(*args, **kwargs)


# 章节
class Chapter(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", max_length=100, default="无")
    category = models.IntegerField(verbose_name="类别", choices=TYPE, default=0)
    classification = models.ForeignKey(Classification, verbose_name="分类", on_delete=models.SET_NULL, null=True,
                                       blank=True)
    plate = models.ForeignKey(Plate, verbose_name="板块", on_delete=models.SET_NULL, null=True, blank=True)
    introduction = models.TextField(verbose_name="简介", default="无")
    is_look_count = models.IntegerField(verbose_name="点击次数", default=0, help_text="记录书本被点击的次数")
    content = models.TextField(verbose_name="内容", null=True, blank=True)
    url = models.URLField(verbose_name="URL")
    crawling_status = models.BooleanField(verbose_name="爬取状态", default=False, help_text="用于判断后台脚本是否已爬取内容")
    index = models.IntegerField(verbose_name="索引", default=0)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ['crawling_status', 'collection', "index", '-date_joined']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lstrip()
        super().save(*args, **kwargs)


# sis001已访问的网页
class VisitHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(verbose_name="URL", db_index=True, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '所有访问sis001的历史'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.url


# 用户与网址记录的状态
class UserToVisitHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, blank=True)
    lishi = models.ForeignKey(VisitHistory, verbose_name="访问网址ID", on_delete=models.CASCADE)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户与sis001访问历史'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.user}-{self.lishi}"


# 用户章节的状态（对于自己的前端）
class ChapterCode(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, blank=True)
    chapter = models.ForeignKey(Chapter, verbose_name="章节", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="个人点击次数", default=0)
    dow_code = models.BooleanField(verbose_name="下载状态", default=False, help_text="用于判断用户是否使用脚本下载过该章节")
    look_code = models.FloatField(verbose_name="章节观看进度", null=True, blank=True, default=0)
    end_code = models.BooleanField(verbose_name="是否已观看完毕", default=False)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户与章节状态（个人进度）'
        verbose_name_plural = verbose_name
        ordering = ['count', '-date_joined']

    def __str__(self):
        return f"{self.user}-{self.chapter}-{self.count}"


# 用户与合集的状态
class CollectionCount(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="个人点击次数", default=0)
    addbook = models.BooleanField(verbose_name="是否加入书架", help_text="判断个人看书页面是否将书加入书架", default=False)
    collect = models.BooleanField(verbose_name="是否加入收藏", help_text="判断油猴插件界面是否保存", default=False)
    yikan = models.BooleanField(verbose_name="是否已看", default=False)
    jindu = models.OneToOneField(ChapterCode, null=True, blank=True, on_delete=models.SET_NULL)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户与书籍状态'
        verbose_name_plural = verbose_name
        ordering = ['count', '-date_joined']

    def __str__(self):
        return f"{self.user}-{self.collection}-{self.count}"
