from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Message

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {'content': 'メッセージ'}
        widgets = {'content': forms.Textarea(attrs={'rows':3})}
        error_messages = {'content':{'required':'必須です', 'mex_length':'600字以下にしてください'}}