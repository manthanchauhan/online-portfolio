from django.shortcuts import render, redirect
from django.views import View
import threading
from .forms import EnterEmailForm, SignUpForm, CustomPassReset
from helper import *
from portfolio.helper import create_default_project
from decouple import config
from datetime import datetime
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login


class EnterEmail(View):
    """
    This view accepts email from new user and sends him the signup link.
    """

    template = "accounts/enter_email.html"
    email = "accounts/signup_email.html"

    def get(self, request):
        form = EnterEmailForm()
        return render(
            request=request, template_name=self.template, context={"form": form}
        )

    def post(self, request):
        form = EnterEmailForm(request.POST)

        # if form is invalid, show errors to user
        if not form.is_valid():
            return render(
                request=request, template_name=self.template, context={"form": form}
            )

        # prepare the encrypted signup link
        user_email = form.cleaned_data["user_email"]
        encoded_email = encode_data(config("NEW_EMAIL_HASH"), user_email)
        signup_link = (
            request.scheme
            + "://"
            + request.get_host()
            + "/accounts/signup/"
            + encoded_email
            + "/"
        )

        # send encrypted signup link to user
        email_content = render_to_string(
            template_name=self.email, context={"signup_link": signup_link}
        )
        email_subject = "<Port>folio Signup Link"

        mail = threading.Thread(
            target=send_mail, args=(user_email, email_content, email_subject)
        )
        mail.start()
        # return to the same page
        messages.success(request, "Please check your email")
        return redirect("accounts:enter_email")


class SignupView(View):
    template = "accounts/signup.html"

    def get(self, request, encoded_email):
        # decode the email
        user_email = decode_data(config("NEW_EMAIL_HASH"), encoded_email)

        """
        if user has already signed up, form submission will give error
        therefore no need to check here.
        """

        # create signup form for the email
        form = SignUpForm(initial={"email": user_email})

        # render the form
        return render(request, template_name=self.template, context={"form": form})

    def post(self, request, encoded_email):
        form = SignUpForm(request.POST)

        # if form is invalid, show errors to user
        if not form.is_valid():
            return render(request, template_name=self.template, context={"form": form})

        """
        check email field for any tampering by the user, by comparing to encoded_email.
        """
        decoded_email = decode_data(config("NEW_EMAIL_HASH"), encoded_email)

        # warn user about the tampering
        if decoded_email != form.cleaned_data["email"]:
            messages.error(request, "Don't act over-smart!!")
            return render(request, template_name=self.template, context={"form": form})

        # in case of no tampering, register as new user.
        form.save()

        # login the new user
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        create_default_project(user)

        login(request=request, user=user)

        return redirect("home")


class CustomPasswordResetDone(View):
    @staticmethod
    def get(request):
        messages.success(request, "Check your mail!")
        return redirect(to="accounts:password_reset")


class CustomPassResetComp(View):
    @staticmethod
    def get(request):
        messages.success(request, "Password Changed Successfully")
        return redirect(to="accounts:login")
