from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime


from trips.forms import TripForm, CommentForm

from trips.models import Trip, Result, Comment

class TripTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass123',
            introduce='自己紹介本文',
        )

        self.trip = Trip.objects.create(
            title='testtrip',
            prefecture='北海道',
            content='投稿本文',
            user=self.user
        )

        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@email.com',
            password='testpass123',
            introduce='自己紹介本文2'
        )
        self.trip2 = Trip.objects.create(
            title='testtrip2',
            prefecture='東京都',
            content='投稿本文2',
            user=self.user2
        )
        self.result2 = Result.objects.create(
            fish_name= 'テストウオ',
            image = 'testimage.jpg',
            trip = self.trip2
        )

    def test_trip_listing(self):
        self.assertEqual(self.trip.title, 'testtrip')
        self.assertEqual(self.trip.prefecture, '北海道')
        self.assertEqual(self.trip.content, '投稿本文')

    def test_trip_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtrip')
        self.assertTemplateUsed(response, 'trips/index.html')

    def test_trip_detail_view(self):
        response = self.client.get(reverse('trip_detail', args=[self.trip.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '投稿本文')
        self.assertTemplateUsed(response, 'trips/trip_detail.html')

    def test_trip_create_view_get_for_logged_in_user(self):
        self.client.login(email='test@email.com', password='testpass123')
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '新規投稿')
        self.assertTemplateUsed(response, 'trips/create.html')
    
    def test_trip_form(self):
        self.client.login(email='test@email.com', password='testpass123')
        response = self.client.get(reverse('create'))
        form = response.context['trip_form']
        self.assertIsInstance(form, TripForm)
        form_data={
            'title':'新規投稿',
            'prefecture':'青森県',
            'content':'投稿本文2',}
        form = TripForm(data=form_data)
        self.assertTrue(form.is_valid())
        trip = Trip(
            title=form_data['title'],
            prefecture=form_data['prefecture'],
            content=form_data['content'],
            user_id=self.user.id
            )
        self.assertTrue(Trip.objects.count(), 1)
        trip.save()
        self.assertTrue(Trip.objects.count(), 2)
        self.assertEqual(trip.title, '新規投稿')
        self.assertEqual(trip.prefecture, '青森県')
        self.assertEqual(trip.content, '投稿本文2')


    def test_trip_create_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/trips/create/' % (reverse('login'))
        )

    # マイページに自分の投稿がある

    def test_user_detail_view(self):
        self.client.login(email='test@email.com', password='testpass123')
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'testtrip')
        self.assertNotContains(response,'testtrip2')
        self.assertContains(response, '投稿数：1')
        self.assertContains(response,'編集')
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user2.id}))
        self.assertNotContains(response, '編集')
        self.client.logout()
        response = self.client.get(reverse('user_trips', kwargs={'pk':self.user2.id}))
        self.assertNotContains(response, '編集')
    # マイページに他人の投稿はない
    # マイページにそのユーザー名が表示される
    # マイページにそのユーザーの投稿数が表示される
    # マイページにログイン状態で入ると編集ボタンがある
    # 他人のマイページにログイン状態で入っても編集ボタンはない

    def test_trip_detail_view_for_all_user(self):
    # 投稿詳細ページにタイトル、投稿日、投稿者、内容、場所、釣果、画像が表示される
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtrip2')
        self.assertContains(response, 'testuser2')
        self.assertContains(response, 'テストウオ')
        self.assertContains(response, '東京都')
        self.assertContains(response, '投稿本文2')
        created_at = datetime.date.today()
        self.assertContains(response, f'{created_at.year}年{created_at.month}月{created_at.day}日')
        self.assertContains(response, 'testimage.jpg')

    def test_trip_detail_view_for_logged_in_user(self):
        self.client.login(email='test@email.com', password='testpass123')
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip2.id}))
        self.assertIsInstance(response.context['form'], CommentForm)
        self.assertContains(response, 'csrfmiddlewaretoken')
        form_data = {'content':'テストコメント', 'trip':self.trip2, 'user':self.user}
        form = CommentForm(form_data)
        self.assertEqual(form.is_valid(), True)
        form.save()
        self.assertEqual(Comment.objects.count(), 1)
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip2.id}))
        self.assertContains(response, 'テストコメント')
        self.assertContains(response, '削除')




    def test_trip_detail_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip2.id}))
        self.assertNotContains(response, 'csrfmiddlewaretoken')
        form_data = {'content':'テストコメント', 'trip':self.trip2, 'user':self.user}
        form = CommentForm(form_data)
        form.save()
        response = self.client.get(reverse('trip_detail', kwargs={'pk':self.trip2.id}))
        self.assertNotContains(response, '削除')