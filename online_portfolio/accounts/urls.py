"""online_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from .forms import LoginForm, CustomPassReset, CustomPassResetConf

app_name = "accounts"

urlpatterns = [
    path("signup/", views.EnterEmail.as_view(), name="enter_email"),
    path("signup/<str:encoded_email>/", views.SignupView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_sub.txt",
            success_url="/accounts/password_reset_done/",
            form_class=CustomPassReset,
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        views.CustomPasswordResetDone.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=CustomPassResetConf,
            success_url="/accounts/password_reset_complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        views.CustomPassResetComp.as_view(),
        name="password_reset_complete",
    ),
]
