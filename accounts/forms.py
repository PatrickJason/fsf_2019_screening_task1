from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
"""
The form for the SignUp page
"""
class UserCreateForm(UserCreationForm):

    class Meta:
        password1 = forms.CharField(widget=forms.PasswordInput(attrs ={'class': 'form-control','placeholder': "Confirm your password ...."}))
        fields = ("username", "email", "password1", "password2",)
        model = get_user_model()
        # widgets added to include the placeholder attributes
        widgets = {
            "username":forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your username ....'}),
            "email":forms.TextInput(attrs={'class': 'form-control','placeholder': "Enter your email ...."}),
            "password2":forms.TextInput(attrs ={'class': 'form-control','placeholder': "Confirm your password ...."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
