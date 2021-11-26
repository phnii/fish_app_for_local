from django.contrib.auth.forms import UserCreationForm
# from django.forms import widgets

from .models import CustomUser

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')