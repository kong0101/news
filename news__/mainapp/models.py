# Create your models here.
from django.db import models


class TUser(models.Model):  # 用户模型
    user_id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tuser'


class TNews(models.Model):     # 新闻模型
    news_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateField(blank=True, null=True)
    input_news_id = models.CharField(max_length=30, blank=True, null=True)
    clip = models.CharField(max_length=300, blank=True, null=True)
    press_release = models.CharField(max_length=300, blank=True, null=True)
    images = models.CharField(max_length=500, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tnews'
