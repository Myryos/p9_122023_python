from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label="Nom d’utilisateur",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Mot de passe",
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields["username"].label = "Nom d’utilisateur"
        self.fields["password"].label = "Mot de passe"

        # Add class to labels
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="REQUIRED")

    class Meta:
        model = User

        fields = ("email", "name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Add classes to labels and form controls
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.label = field_name.capitalize()
