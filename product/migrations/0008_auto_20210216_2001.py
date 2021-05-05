# Generated by Django 3.1.6 on 2021-02-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210216_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug_ar',
            field=models.SlugField(allow_unicode=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='slug_en',
            field=models.SlugField(allow_unicode=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_ar',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
