from django.contrib.auth import get_user_model
from django.test import TestCase

from trips.forms import CommentForm, TripForm, TripFindForm
from trips.models import Trip

class TestTripForm(TestCase):
    def setUp(self):
        self.data = {
            'title': 'テストタイトル',
            'content': 'テスト内容',
            'prefecture': '北海道'
        }

    def test_form_valid(self):
        # 正しい値は通過する
        form = TripForm(self.data)
        self.assertTrue(form.is_valid())

    def test_wrong_title(self):
        # タイトルが空白ではエラーが起こる
        self.data['title'] = ''
        form = TripForm(self.data)
        self.assertFalse(form.is_valid())


    def test_wrong_content(self):
        # 内容が空白ではエラーが起こる
        self.data['content'] = ''
        form = TripForm(self.data)
        self.assertFalse(form.is_valid())

    def test_wrong_prefecture(self):
        # 都道府県が空白ではエラーが起こる
        self.data['prefecture'] = ''
        form = TripForm(self.data)
        self.assertFalse(form.is_valid())


class TestCommentForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass123',
        )
        self.trip = Trip.objects.create(
            title='testtitle',
            prefecture='北海道',
            content='投稿本文',
            user=self.user
        )
        self.data = {
            'content': 'コメント本文',
            'trip': self.trip, 
            'user': self.user
        }
    
    def test_form_valid(self):
        # 正しい値は通過する
        form = CommentForm(self.data)
        self.assertTrue(form.is_valid())
    
    def test_form_wrong_content(self):
        # contentが空の値ではエラーが起こる
        self.data['content'] = ''
        form = CommentForm(self.data)
        self.assertFalse(form.is_valid())


class TestTripFindView(TestCase):
    def setUp(self):
        self.data = {
            'keyword_fish_name': 'カレイ',
            'keyword_prefecture': '東京都'
        }

    def test_form_valid(self):
        # 正しい値は通過する
        form = TripFindForm(self.data)
        self.assertTrue(form.is_valid())
        # keyword_prefectureの値が空白でも通過する
        self.data['keyword_prefecture'] = ''
        form = TripFindForm(self.data)
        self.assertTrue(form.is_valid())
    
    def test_form_wrong_find(self):
        # keyword_fish_nameの値が空白ではエラーが起こる
        self.data['keyword_fish_name'] = ''
        form = TripFindForm(self.data)
        self.assertFalse(form.is_valid())
        # keyword_fish_nameの値がひらがなではエラーが起こる
        self.data['keyword_fish_name'] = 'かれい'
        form = TripFindForm(self.data)
        self.assertFalse(form.is_valid())
        # keyword_fish_nameの値がアルファベットではエラーが起こる
        self.data['keyword_fish_name'] = 'karei'
        form = TripFindForm(self.data)
        self.assertFalse(form.is_valid())