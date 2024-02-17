from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import (
    login,
    authenticate,
    logout,
)


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides."
    return render(
        request, "authentication/login.html", context={"form": form, "message": message}
    )


def signup(request):
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = forms.SignUpForm()
    return render(request, "authentication/signup_page.html", {"form": form})


def logout_view(request):
    logout(request=request)
    return redirect("login")


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
