from django import forms
from .models import  Comment, Trip
from django.core.validators import RegexValidator
from .prefectures import choice_prefectures

class TripForm(forms.ModelForm):
    prefecture = forms.ChoiceField(label='場所',choices=choice_prefectures)
    class Meta:
        model = Trip
        fields = ['title', 'content',]
        widgets = {'content': forms.Textarea(attrs={'rows':3})}


class TripFindForm(forms.Form):
    keyword_fish_name = forms.CharField(label='魚名',required=True,
                validators=[RegexValidator(r'^([ァ-ン]|ー)+$','全角カナで入力してください')],
                widget=forms.TextInput(attrs={'placeholder':'全角カナ','class':'form-control mr-3'}))
    keyword_prefecture = forms.ChoiceField(label='場所',choices=choice_prefectures,required=False,
                widget=forms.Select(attrs={'class':'form-control mr-3'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'trip', 'user']
        widgets = {'content': forms.Textarea(attrs={'rows':3,'class':'form-control col-8 m-auto'})}