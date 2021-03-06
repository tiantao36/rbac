# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-22 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basepermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='基础访问权限名')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('deny_userinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='拒绝用户')),
            ],
        ),
        migrations.AlterField(
            model_name='permission',
            name='imgurl',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='菜单图标'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(max_length=32, verbose_name='菜单访问权限名'),
        ),
    ]
