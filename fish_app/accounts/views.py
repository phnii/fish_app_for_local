from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from accounts.forms import SignupForm, MessageForm
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser, Connection, Room, Message


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        customuser = form.save()
        login(self.request, customuser)
        self.object = customuser
        return HttpResponseRedirect(self.get_success_url())


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

login = LoginView.as_view()



class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = CustomUser
    template_name = 'accounts/user_update.html'
    fields = ['username','introduce']
    success_url = 'user_trips'
    
    def test_func(self):
        user = self.request.user
        return user.id == self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('user_trips', kwargs={'pk': self.object.id})


class FollowListView(DetailView):
    model = CustomUser
    template_name = 'accounts/user_follow.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = int(self.kwargs['pk'])
        following_list = Connection.objects.filter(follower=CustomUser.objects.get(id=self.kwargs['pk'])).select_related('followed')
        followed_by_list = Connection.objects.filter(followed=CustomUser.objects.get(id=self.kwargs['pk'])).select_related('follower')
        context['following_list'] = following_list
        context['followed_by_list'] = followed_by_list
        if self.request.user.username:
            follower = CustomUser.objects.get(username=self.request.user.username)
            followed = CustomUser.objects.get(id=self.kwargs['pk'])
            connection_exist = Connection.objects.filter(follower=follower, followed=followed).exists()
            context['connection_exist'] = connection_exist
            reverse_connection_exist = Connection.objects.filter(follower=followed, followed=follower).exists()
            mutural_follow = connection_exist and reverse_connection_exist
            context['mutural_follow'] = mutural_follow
            sender = CustomUser.objects.get(id=self.request.user.id)
            receiver = CustomUser.objects.get(id=self.kwargs['pk'])
            room_exist = Room.objects.filter(users__in=[sender]).filter(users__in=[receiver]).exists()
            context['room_exist'] = room_exist
        return context

@login_required
def follow(request, *args, **kwargs):
    if request.method == 'POST':
        follower = CustomUser.objects.get(username=request.user.username)
        followed = CustomUser.objects.get(id=kwargs['pk'])
        Connection.objects.create(follower=follower, followed=followed)
        return redirect(to='/accounts/follow-list/{}/'.format(kwargs['pk']))
    else:
        return render(request, 'user_follow.html',)

@login_required
def unfollow(request, *args, **kwargs):
    if request.method == 'POST':
        follower = CustomUser.objects.get(username=request.user.username)
        followed = CustomUser.objects.get(id=kwargs['pk'])
        Connection.objects.get(follower=follower, followed=followed).delete()
        return redirect(to='/accounts/follow-list/{}/'.format(kwargs['pk']))
    else:
        return render(request, 'user_follow.html',)

@login_required
def room_create(request, **kwargs):
    if request.method == 'POST':
        sender = CustomUser.objects.get(id=request.user.id)
        receiver = CustomUser.objects.get(id=kwargs['pk'])
        if Room.objects.filter(users__in=[sender]).filter(users__in=[receiver]).count() == 0:
            room = Room.objects.create()
            room.users.add(sender)
            room.users.add(receiver)
        else:
            room = Room.objects.filter(users__in=[sender]).filter(users__in=[receiver]).first()
    return redirect(to='/accounts/room/{}'.format(room.id))

class RoomDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Room
    template_name = 'accounts/room_detail.html'

    def test_func(self):
        user = self.request.user
        room = Room.objects.get(id = self.kwargs['pk'])
        room_users = room.users.all().values_list('id', flat=True)
        room_users = {id for id in room_users}
        return {user.id} < room_users

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        form = MessageForm()
        context['form'] = form
        messages = Message.objects.filter(room_id=self.kwargs['pk']).order_by('-created_at')
        context['messages'] = messages
        # 相互フォロー状態の真偽を'mutural_follow'で返す
        room = Room.objects.get(id=self.kwargs['pk'])
        room_users = room.users.all().values_list('id', flat=True)
        room_users = list(room_users)
        user1 = CustomUser.objects.get(id=room_users[0])
        user2 = CustomUser.objects.get(id=room_users[1])
        connection_exist = Connection.objects.filter(follower=user1, followed=user2).exists()
        reverse_connection_exist = Connection.objects.filter(follower=user2, followed=user1).exists()
        mutural_follow = connection_exist and reverse_connection_exist
        context['mutural_follow'] = mutural_follow
        return context

@login_required
def message_create(request, **kwargs):
    if request.method == 'POST':
        sender = request.user
        content = request.POST['content']
        room = Room.objects.get(id=kwargs['pk'])
        Message.objects.create(sender=sender, content=content, room=room)
    return redirect(to='/accounts/room/{}/'.format(kwargs['pk']))