from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {"first_name": "Name", "password2": "confirm password"}

    def __init__(self, *args, **kwargs):
        # inherits the form(telling it the class we are modifying)
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # can set the classes one at a time or just use a for loop
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "username",
            "location",
            "bio",
            "short_intro",
            "profile_image",
            "social_github",
            "social_instagram",
            "social_twitter",
            "social_linkedin",
        ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
