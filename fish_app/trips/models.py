from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

class Trip(models.Model):
    class Meta:
        db_table = 'trip'
        verbose_name = '釣行'

    def __str__(self):
        return '<' 'trip_id=' + str(self.id) + 'user=' + str(self.user) + '>'

    title = models.CharField(max_length=30, verbose_name='タイトル')
    prefecture = models.CharField(max_length=4, verbose_name='都道府県')
    content = models.CharField(max_length=1000, verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Result(models.Model):
    class Meta:
        db_table = 'result'
        verbose_name = '釣果'

    def __str__(self):
        return '<' 'result_id=' + str(self.id) + '>'
    
    fish_name = models.CharField(max_length=20, verbose_name='魚名',validators=[RegexValidator(r'^([ァ-ン]|ー)+$','全角カナで入力してください')])
    image = models.ImageField(upload_to='images/', verbose_name='画像(任意)', null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, verbose_name='投稿日時')


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
        verbose_name = 'コメント'

    def __str__(self):
        return '<' 'comment_id=' + str(self.id) + '>'
    
    content = models.CharField(max_length=200, verbose_name='コメント内容')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, verbose_name='投稿日時')
    
    