# Generated by Django 3.2.4 on 2022-02-18 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiaosuo', '0016_auto_20220212_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncount',
            name='jindu',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='xiaosuo.chaptercode'),
        ),
    ]
