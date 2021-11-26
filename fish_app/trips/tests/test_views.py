import datetime
from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from trips.forms import  TripFindForm
from trips.models import Trip, Result, Comment

class TestViews(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test1@email.com',
            password='testpass123',
            introduce='自己紹介本文1',
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@email.com',
            password='testpass123',
            introduce='自己紹介本文2',
        )
        self.trip1 = Trip.objects.create(
            title='testtitle1',
            prefecture='北海道',
            content='投稿本文1',
            user=self.user1
        )
        self.trip2 = Trip.objects.create(
            title='testtitle2',
            prefecture='沖縄県',
            content='投稿本文2',
            user=self.user2
        )
        self.result1 = Result.objects.create(
            fish_name= 'テストウオイチ',
            image = 'testimage1.jpg',
            trip = self.trip1
        )
        self.result2 = Result.objects.create(
            fish_name='テストウオニ',
            image='testimage2.jpg',
            trip=self.trip2
        )
        self.comment1 = Comment.objects.create(
            content='コメント本文1',
            user=self.user1,
            trip=self.trip1
        )
        self.comment2 = Comment.objects.create(
            content='コメント本文2',
            user=self.user2,
            trip=self.trip2
        )
    
    def test_top_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtitle1')
        self.assertContains(response, 'testtitle2')
        self.assertTemplateUsed(response, 'trips/index.html')
    
    def test_create_view_for_logged_in_user(self):
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '新規投稿')
        self.assertTemplateUsed(response, 'trips/create.html')
    
    def test_create_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/trips/create/')
    
    def test_user_trips_view(self):
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user1.id}))
        self.assertEqual(response.status_code, 200)
        # そのページのユーザーが投稿したtripのタイトルが表示される
        self.assertContains(response,'testtitle1')
        # 他のユーザーが投稿したtripは表示されない
        self.assertNotContains(response,'testtitle2')
        # そのユーザーのユーザー名、自己紹介、投稿数が表示される
        self.assertContains(response, self.trip1.user.username)
        self.assertContains(response, self.trip1.user.introduce)
        self.assertContains(response, '投稿数：1')
        self.assertContains(response,'編集')
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user2.id}))
        self.assertNotContains(response, '編集')
        self.client.logout()
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user1.id}))
        self.assertNotContains(response, '編集')
    
    def test_user_trips_view_for_logged_in_user(self):
        # そのページのユーザー自身はログイン状態でユーザー情報の編集ボタンが表示される
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('user_trips', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'編集')

    def test_trip_detail_view(self):
        #釣行詳細ページで釣行のタイトル、投稿者名、本文、投稿日、釣果の魚名、釣果の画像が表示される
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtitle1')
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'テストウオイチ')
        self.assertContains(response, '北海道')
        self.assertContains(response, '投稿本文1')
        created_at = datetime.date.today()
        self.assertContains(response, f'{created_at.year}年{created_at.month}月{created_at.day}日')
        self.assertContains(response, 'testimage1.jpg')
    
    def test_trip_detail_view_for_logged_in_user(self):
        # ログイン状態で自身のtrip投稿の編集ボタン、削除ボタン、コメント入力フォーム、自身のコメント削除ボタン、各コメントが表示される
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('trip_detail', args=[self.trip1.id]))
        self.assertContains(response, '編集')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'コメント本文1')
        self.assertNotContains(response, 'コメント本文2')
        # ログイン状態で他者のコメントの削除ボタンが表示されない
        self.assertContains(response, '削除')
        self.client.logout()
        # ログイン状態で他者のtrip詳細ページに移動してもtrip編集ボタン、削除ボタンは表示されない
        self.client.login(email='test2@email.com', password='testpass123')
        response = self.client.get(reverse('trip_detail', args=[self.trip1.id]))
        self.assertNotContains(response, '編集')
        self.assertNotContains(response, '削除')

    def test_trip_detail_view_for_logged_out_user(self):
        # ログアウト状態で投稿の編集ボタン、コメント入力フォーム、コメント削除ボタンは表示されない
        self.client.logout()
        response = self.client.get(reverse('trip_detail', args=[self.trip1.id]))
        self.assertNotContains(response, 'csrfmiddlewaretoken')
        self.assertNotContains(response, '編集')
        self.assertNotContains(response, '削除')

    def test_comment_delete_view_for_logged_in_user(self):
        # ログイン状態でコメント投稿者は自身のコメントを削除できる
        self.client.login(email='test1@email.com', password='testpass123')
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), True)
        response = self.client.post(reverse('delete', args=[self.trip1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), False)
        # ログイン状態でも他者のコメントは削除できない
        response = self.client.post(reverse('delete', args=[self.trip2.id]))
        self.assertEqual(Comment.objects.filter(id=self.comment2.id).exists(), True)
    
    def test_comment_delete_view_for_logged_out_user(self):
        # ログアウト状態でコメントの削除はできない
        self.client.logout()
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), True)
        response = self.client.post(reverse('delete', args=[self.trip1.id]))
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), True)
    
    def test_search_view(self):
        # 検索フォームが表示される
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trips/trip_search.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertIsInstance(response.context['form'], TripFindForm)
        # 検索すると魚名と都道府県が一致するresultが表示される
        data={'keyword_fish_name':self.result1.fish_name, 'keyword_prefecture':'北海道'}
        response = self.client.post(reverse('search'),data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trip1.title)
        self.assertContains(response, self.trip1.user.username)
        self.assertContains(response, self.trip1.prefecture)
        created_at = datetime.date.today()
        self.assertContains(response, f'{created_at.year}年{created_at.month}月{created_at.day}日')
        # 検索すると魚名が一致して都道府県が一致しないresultは表示されない
        data={'keyword_fish_name':self.result1.fish_name, 'keyword_prefecture':'東京都'}
        response = self.client.post(reverse('search'),data)
        self.assertNotContains(response, self.trip1.title)
        # 検索すると都道府県が一致して魚名が一致しないresultは表示されない
        data={'keyword_fish_name':'テストウオデハナイ', 'keyword_prefecture':self.trip1.prefecture}
        response = self.client.post(reverse('search'),data)
        self.assertNotContains(response, self.trip1.title)
    
    def test_trip_delete_view(self):
        # ログイン状態でtrip投稿者は自身の投稿を削除できる
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('delete', args=[self.trip1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trips/trip_confirm_delete.html')
        response = self.client.post(reverse('delete', args=[self.trip1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Trip.objects.filter(id=self.trip1.id).exists())
        # ログイン状態でも他者のtripは削除できない
        response = self.client.get(reverse('delete', args=[self.trip2.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Trip.objects.filter(id=self.trip2.id).exists())

    def test_trip_update_view_for_logged_in_user(self):
        # ログイン状態で自身が投稿したtripの編集ページに移動するとタイトル、内容、場所、子resultのfish_name、画像が既にフォームに入力してある
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get(reverse('update', args=[self.trip1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trip1.title )
        self.assertContains(response, self.trip1.content)
        self.assertContains(response, self.trip1.prefecture)
        self.assertContains(response, self.result1.fish_name)
        self.assertContains(response, self.result1.image)
        # ログイン状態でも他者のtripの編集ページに移動しようとするとトップページにリダイレクトされる
        response = self.client.get(reverse('update',args=[self.trip2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/trips/index',status_code=302,target_status_code=301)

    def test_trip_update_view_for_logged_out_user(self):
        # ログアウト状態で編集ページに移動しようとするとログインページにリダイレクトされる
        self.client.logout()
        response = self.client.get(reverse('update', args=[self.trip1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/trips/{self.trip1.id}/update/')