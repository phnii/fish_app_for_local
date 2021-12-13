from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime

from .models import Connection, Room, Message
from .forms import MessageForm

class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@email.com',
            password='testpass123'
        )
        self.assertEqual(superuser.username, 'testsuperuser')
        self.assertEqual(superuser.email, 'testsuperuser@email.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

class SignupPageTests(TestCase):
    
    def setUp(self):
        url =  '/accounts/signup/'
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
        self.assertContains(self.response, 'ユーザー')
        self.assertNotContains(
            self.response, 'これは新規投稿ページではありません。'
        )

    def test_signup_form(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, user.username)
        self.assertEqual(get_user_model().objects.all()[0].email, user.email)

class FollowPageTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            id = 1,
            username='testuser1',
            email='test1@email.com',
            password='testpass123',
        )
        self.user2 = get_user_model().objects.create_user(
            id = 2,
            username='testuser2',
            email='test2@email.com',
            password='testpass123',
        )
        self.connection1 = Connection.objects.create(
            id = 1,
            follower = self.user1,
            followed = self.user2,
            created_at = datetime.date.today()
        )
        url = '/accounts/follow-list/1/'
        self.response = self.client.get(url)

    
    def test_follow_list_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/user_follow.html')
        self.assertContains(self.response, self.user1.username)
        self.assertContains(self.response, self.user2.username)

    def test_follower_list_view_for_logged_in_user(self):
        # user2がログイン状態でuser1のページを訪れるとフォローするボタン表示される
        self.client.login(email='test2@email.com', password='testpass123')
        self.response = self.client.get('/accounts/follow-list/1/')
        self.assertContains(self.response, 'フォローする')
        # 相互フォロー状態でない時はメッセージボタンは表示されない
        self.assertNotContains(self.response, 'メッセージ')
        # user2がログイン状態でフォロー状態でuser1のページを訪れるとフォローを外すボタンが表示される
        self.connection2 = Connection.objects.create(
            id = 2,
            follower = self.user2,
            followed = self.user1,
            created_at = datetime.date.today()
        )
        self.response = self.client.get('/accounts/follow-list/1/')
        self.assertContains(self.response, 'フォローを外す')
        # user1とuser2が相互フォロー状態でメッセージボタンが表示される
        self.assertContains(self.response, 'メッセージ')
    
    def test_follower_list_view_for_logged_out_user(self):
        # ログアウト状態でフォローするボタン、フォローを外すボタン、メッセージボタンは表示されない
        self.client.logout()
        self.response = self.client.get('/accounts/follow-list/1/')
        self.assertNotContains(self.response, 'フォローする')
        self.assertNotContains(self.response, 'フォローを外す')
        self.assertNotContains(self.response, 'メッセージ')

class RoomCreateTest(TestCase):
    
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            id = 1,
            username='testuser1',
            email='test1@email.com',
            password='testpass123',
        )
        self.user2 = get_user_model().objects.create_user(
            id = 2,
            username='testuser2',
            email='test2@email.com',
            password='testpass123',
        )
        self.connection1 = Connection.objects.create(
            id = 1,
            follower = self.user1,
            followed = self.user2,
            created_at = datetime.date.today(),
        )
        self.connection2 = Connection.objects.create(
            id = 2,
            follower = self.user2,
            followed = self.user1,
            created_at = datetime.date.today(),
        )
    
    def test_room_create(self):
        # Room作成できる
        self.assertEqual(Room.objects.all().count(), 0)
        self.client.login(email='test1@email.com', password='testpass123')
        data = {'sender':self.user1, 'receiver':self.user2}
        response = self.client.post(reverse('room_create', args=[2]), data)
        self.assertRedirects(response, expected_url='/accounts/room/1',status_code=302,target_status_code=301)
        self.assertEqual(Room.objects.all().count(), 1)
        # Room作成後に再度room_createを実行しても新しいRoomは作成せず、リダイレクトする
        response = self.client.post(reverse('room_create', args=[2]), data)
        self.assertRedirects(response, expected_url='/accounts/room/1',status_code=302,target_status_code=301)
        self.assertEqual(Room.objects.all().count(), 1)
    
    def test_room_detail_view(self):
        self.room = Room.objects.create(
            id = 1,
        )
        self.room.users.add(self.user1)
        self.room.users.add(self.user2)
        self.message = Message.objects.create(
            sender = self.user1,
            content = 'TEST CONTENT',
            room = self.room,
            created_at = datetime.date.today()
        )
        # 相互フォロー状態でメッセージフォームが表示される
        self.client.login(email='test1@email.com', password='testpass123')
        response = self.client.get('/accounts/room/1/')
        self.assertContains(response, '送信')
        # 投稿済みメッセージが表示される
        self.assertContains(response, 'TEST CONTENT')
        # 相互フォロー状態でない場合注意書きが表示される、投稿済みメッセージは表示される
        self.connection1.delete()
        response = self.client.get('/accounts/room/1/')
        self.assertContains(response, '※ メッセージの送信は相互フォロー状態でのみ可能です')
        self.assertContains(response, 'TEST CONTENT')
        
    def test_room_detail_view_for_outsiders(self):
        self.room = Room.objects.create(
            id = 1,
        )
        self.room.users.add(self.user1)
        self.room.users.add(self.user2)
        # ログアウト状態でメッセージルームにアクセスするとリダイレクトされる
        self.client.logout()
        response = self.client.get('/accounts/room/1/')
        self.assertRedirects(response, expected_url='/accounts/login/?next=/accounts/room/1/', status_code=302)
        # user1とuser2のメッセージルームに第三者user3がアクセスしようとすると禁止される
        self.user3 = get_user_model().objects.create_user(
            id = 3,
            username='testuser3',
            email='test3@email.com',
            password='testpass123',
        )
        self.client.login(email='test3@email.com', password='testpass123')
        response = self.client.get('/accounts/room/1/')
        self.assertEqual(response.status_code, 403)

class MessageFormTest(TestCase):

    def setUp(self):
        self.data = {
            'content':'TEST MESSAGE CONTENT'
        }
    
    def test_form_valid(self):
        # 正しい値は通過する
        form = MessageForm(self.data)
        self.assertTrue(form.is_valid())
    
    def test_wrong_content(self):
        self.data['content'] = ''
        form = MessageForm(self.data)
        self.assertFalse(form.is_valid())
