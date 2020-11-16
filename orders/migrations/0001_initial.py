# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-06 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appconf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u66f4\u65b0\u63cf\u8ff0')),
                ('script_name', models.CharField(max_length=255, null=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('status', models.BooleanField(default=False, verbose_name='\u90e8\u7f72\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('operating_time', models.DateTimeField(null=True, verbose_name='\u9884\u7ea6\u64cd\u4f5c\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('order_user', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63d0\u4ea4\u7528\u6237')),
                ('db_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              to='appconf.Database', verbose_name='\u6570\u636e\u5e93')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Deploy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u66f4\u65b0\u63cf\u8ff0')),
                ('version', models.CharField(max_length=255, verbose_name='\u7248\u672c\u53f7')),
                ('status', models.BooleanField(default=False, verbose_name='\u90e8\u7f72\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('operating_time', models.DateTimeField(null=True, verbose_name='\u9884\u7ea6\u64cd\u4f5c\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('order_user', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63d0\u4ea4\u7528\u6237')),
                ('order_status', models.BooleanField(default=False, verbose_name='\u5de5\u5355\u72b6\u6001')),
                ('app_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to='appconf.Project', verbose_name='\u5e94\u7528\u540d\u79f0')),
                ('dbscript', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to='orders.DBScript', verbose_name='\u6570\u636e\u5e93\u5de5\u5355')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_id', models.IntegerField(default=0, verbose_name='\u6587\u6863\u7f16\u53f7')),
                ('name', models.CharField(default=None, max_length=50, verbose_name='\u5e94\u7528\u540d\u79f0')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5e94\u7528\u63cf\u8ff0')),
                ('current_ver', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5f53\u524d\u7248\u672c')),
                ('next_ver', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u540e\u7eed\u7248\u672c')),
                ('language_type', models.CharField(max_length=30, null=True, verbose_name='\u8bed\u8a00\u7c7b\u578b')),
                ('app_type', models.CharField(max_length=30, null=True, verbose_name='\u7a0b\u5e8f\u7c7b\u578b')),
                ('app_arch', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7a0b\u5e8f\u6846\u67b6')),
                ('code_address', models.CharField(max_length=255, null=True, verbose_name='\u4ee3\u7801\u5e93\u5730\u5740')),
                ('start_cmd', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u542f\u52a8\u547d\u4ee4')),
                ('stop_cmd', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u505c\u6b62\u547d\u4ee4')),
                ('config_detail', models.TextField(blank=True, max_length=1000, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u8bf4\u660e')),
                ('docker_expose', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Docker\u5bb9\u5668\u8bf4\u660e')),
                ('app_monitor', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9700\u8981\u7684\u4e1a\u52a1\u76d1\u63a7\u9879')),
                ('need_ha', models.CharField(default='\u65e0\u9700\u9ad8\u53ef\u7528', max_length=30, verbose_name='\u9ad8\u53ef\u7528\u8bf4\u660e')),
                ('need_dn', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9700\u8981\u65b0\u589e\u57df\u540d')),
                ('need_location', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9700\u8981\u65b0\u589e\u4e8c\u7ea7\u76ee\u5f55')),
                ('uri_mapping_from', models.CharField(blank=True, max_length=255, null=True, verbose_name='URI\u6620\u5c04\u6765\u6e90')),
                ('uri_mapping_to', models.CharField(blank=True, max_length=255, null=True, verbose_name='URI\u6620\u5c04\u76ee\u6807')),
                ('need_wan', models.CharField(default='\u5426', max_length=2, verbose_name='\u662f\u5426\u9700\u8981\u8bbf\u95ee\u5916\u7f51')),
                ('requester', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u8c03\u7528\u65b9')),
                ('rely_on', models.TextField(blank=True, max_length=255, null=True, verbose_name='\u5e94\u7528\u4f9d\u8d56\u7684\u5176\u4ed6\u9700\u6c42')),
                ('product_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u6240\u5c5e\u4ea7\u54c1\u7ebf')),
                ('dev_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5f00\u53d1\u8d1f\u8d23\u4eba')),
                ('ops_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u8fd0\u7ef4\u8d1f\u8d23\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='Require',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='\u6807\u9898')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9700\u6c42\u63cf\u8ff0')),
                ('status', models.BooleanField(default=False, verbose_name='\u90e8\u7f72\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('operating_time', models.DateTimeField(null=True, verbose_name='\u9884\u7ea6\u64cd\u4f5c\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('order_user', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63d0\u4ea4\u7528\u6237')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to='appconf.AppOwner', verbose_name='\u8d1f\u8d23\u4eba')),
            ],
            options={
                'ordering': ['operating_time'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('doc_id', 'current_ver')]),
        ),
        migrations.AlterUniqueTogether(
            name='deploy',
            unique_together=set([('app_name', 'version')]),
        ),
    ]