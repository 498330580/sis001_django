import os

from django.db import models

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    GENDER_TYPE = (
        (0, "无"),
        (1, "男"),
        (2, "女")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.IntegerField(choices=GENDER_TYPE, default=0, verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d',
                               default='avatar/default.png',
                               blank=True,
                               null=True,
                               verbose_name='用户头像')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        if 'avatar/default.png' not in self.avatar.path.replace('\\', '/'):
            os.remove(self.avatar.path)
        super(UserProfile, self).delete(*args, **kwargs)
