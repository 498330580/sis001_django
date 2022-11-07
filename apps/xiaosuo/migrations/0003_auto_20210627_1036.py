# Generated by Django 3.2.4 on 2021-06-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaosuo', '0002_alter_chapter_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='category',
            field=models.IntegerField(choices=[(0, '无'), (1, '小说'), (2, '图片')], default=0, verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='label',
            field=models.IntegerField(choices=[(0, '无')], default=0, verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='plate',
            field=models.IntegerField(choices=[(0, '无'), (1, '原创人生')], default=0, verbose_name='板块'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='category',
            field=models.IntegerField(choices=[(0, '无'), (1, '小说'), (2, '图片')], default=0, verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='label',
            field=models.IntegerField(choices=[(0, '无')], default=0, verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='plate',
            field=models.IntegerField(choices=[(0, '无'), (1, '原创人生')], default=0, verbose_name='板块'),
        ),
    ]