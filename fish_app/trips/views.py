from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import DetailView, ListView, DeleteView
from django.views import View
from django.views.generic.edit import FormMixin
from .forms import CommentForm, TripForm, TripFindForm
from .models import Comment, Trip, Result
from django.shortcuts import redirect
from . import graph
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse


class TopView(ListView):
    template_name = 'trips/index.html'
    model = Trip
    paginate_by = 6

    def get_queryset(self):
        return Trip.objects.all().select_related('user').prefetch_related('result_set').order_by('-created_at')


@login_required
def make_inline_formset(request):

    ResultFormSet = forms.inlineformset_factory(
        parent_model=Trip,
        model=Result,
        fields=('fish_name','image'),
        extra=1,
        can_delete=False,
        widgets={'image':forms.FileInput(attrs={'class':'form-control-file'}),
                 'fish_name':forms.TextInput(attrs={'placeholder':'全角カナ'})
        }
    )
    if request.method == 'POST':
        title = request.POST['title']
        prefecture = request.POST['prefecture']
        content = request.POST['content']
        user = request.user
        trip = Trip(title=title, prefecture=prefecture, content=content, user=user)
 
        formset = ResultFormSet(
            data=request.POST,
            files=request.FILES,
            instance=trip,
            queryset=Result.objects.none(),
        )
        if formset.is_valid():
            trip.save()
            formset.save()
            return redirect(to='/trips/index')
        else:
            return render(request, 'trips/create.html',{'formset':formset,'trip_form':TripForm(request.POST)})
    else:
        formset = ResultFormSet(
            queryset=Result.objects.none(),
        )
    return render(request, 'trips/create.html',{'formset':formset,'trip_form':TripForm()})


@login_required
def update_inline_formset(request,pk):
    if not request.user.id == Trip.objects.get(id=pk).user_id:
        return redirect(to='/trips/index')

    ResultFormSet = forms.inlineformset_factory(
        parent_model=Trip,
        model=Result,
        fields=('fish_name','image'),
        extra=1,
        can_delete=False,
        widgets={'image':forms.FileInput(attrs={'class':'form-control-file'}),
                 'fish_name':forms.TextInput(attrs={'placeholder':'全角カナ'})
        }
    )
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk)
        trip.title = request.POST['title']
        trip.prefecture = request.POST['prefecture']
        trip.content = request.POST['content']
        trip.user = request.user

        formset = ResultFormSet(
            data=request.POST,
            files=request.FILES,
            instance=trip,
            queryset=Result.objects.none(),
        )

        if formset.is_valid():
            trip.save()
            formset.save()
            result_ids = request.POST.getlist('delete')
            Result.objects.filter(pk__in=result_ids).delete()
            return redirect(to='trip_detail', pk=trip.id)
        else:
            return render(request, 'trips/update.html',{'pk':pk, 'formset':formset,'trip_form':TripForm(request.POST)})
    else:
        formset = ResultFormSet(
            instance=Trip.objects.get(id=pk),
            queryset=Result.objects.none(),
        )
    results = Result.objects.filter(trip__id=pk)
    return render(request, 'trips/update.html',{'results':results,'pk':pk,'formset':formset,'trip_form':TripForm(instance=Trip.objects.get(id=pk),initial={'prefecture':Trip.objects.get(id=pk).prefecture})})


def search(request):
    if (request.method == 'POST'):
        form = TripFindForm(request.POST)
        keyword_fish_name = request.POST['keyword_fish_name']
        keyword_prefecture = request.POST['keyword_prefecture']
        if keyword_prefecture == '':
            results = Result.objects.filter(fish_name=keyword_fish_name).values(
                'fish_name','image','trip_id','created_at','trip__title','trip__prefecture','trip__user__username','trip__user__id')
            for result in results:
                result['image_url'] = f"/media/{result['image']}"
        else:
            results = Result.objects.filter(fish_name=keyword_fish_name).filter(trip__prefecture=keyword_prefecture).values(
                'fish_name','image','trip_id','created_at','trip__title','trip__prefecture','trip__user__username','trip__user__id')
            for result in results:
                result['image_url'] = f"/media/{result['image']}"
        result_list = list(results.values_list('created_at__month',flat=True))
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        y = []
        for i in range(1,13):
            y.append(result_list.count(i))
        chart = graph.plot_graph(x,y)

        return render(request, 'trips/trip_search.html', {'form':form, 'results':results, 'chart':chart})
    else:
        form =TripFindForm()
        return render(request, 'trips/trip_search.html', {'form':form})


class TripDetailView(FormMixin, DetailView):
    model = Trip
    form_class = CommentForm

    def get_success_url(self):
        return reverse('trip_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'trip': self.object})
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.id:
            return redirect(to='login')
        copied = request.POST.copy()
        copied['user'] = request.user.id
        self.object = self.get_object()
        form = CommentForm(copied)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)




class UserTripsView(ListView):
    model = Trip
    template_name = 'trips/user_trips.html'
    paginate_by = 6

    def get_queryset(self,**kwargs):
        return Trip.objects.filter(user_id=self.kwargs['pk']).select_related('user').prefetch_related('result_set').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = get_user_model().objects.get(id=self.kwargs['pk'])
        return context


class TripDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Trip
    success_url = '/trips/index'

    def test_func(self):
        user = self.request.user
        return user == Trip.objects.get(id=self.kwargs['pk']).user


class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
    model = Comment

    def test_func(self):
        user = self.request.user
        return user == Comment.objects.get(id=self.kwargs['pk']).user

    def post(self,request,*args,**kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        trip = comment.trip
        comment.delete()
        return redirect(to='trip_detail', pk=trip.id)