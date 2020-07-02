from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def _existing_email(email):
    """
    It is a validator which checks if the any user with the given email exists in the system.
    :param email: email to check
    :type: str
    :rtype: bool
    """
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return False

    return True


def existing_email(should_exist=False):
    """
    It is a validator which checks if the any user with the given email exists in the system.
    :param email: email to check
    :param should_exist: the desired result, regarding email existence
    :type: str
    :rtype: bool
    """

    def validator(email):
        result = _existing_email(email)

        if result != should_exist:
            if not should_exist:
                raise forms.ValidationError(
                    "User with this email already exists. Please login."
                )

            raise forms.ValidationError(
                mark_safe(
                    "User with this email does not exists. Please <a href='/accounts/signup/'>signup</a>."
                )
            )

        return

    return validator


class EnterEmailForm(forms.Form):
    user_email = forms.EmailField(
        label="Enter Email Here",
        max_length=100,
        validators=[existing_email],
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter Your Email", "class": "form-control"}
        ),
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        validators=[existing_email()],
        widget=forms.EmailInput(
            attrs={"readonly": True, "id": "email", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"id": "username", "class": "form-control"}
            ),
            "password1": forms.TextInput(
                attrs={"id": "password1", "class": "form-control"}
            ),
            "password2": forms.TextInput(
                attrs={"id": "password2", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["id"] = "password1"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["id"] = "password2"


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password"}),
        help_text=mark_safe(
            'Forgot Password? Click <a href="/accounts/password_reset/">here</a>.'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class CustomPassReset(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"id": "emailInput", "class": "form-control"}),
        validators=[existing_email(should_exist=True)],
    )

    def __init__(self, *args, **kwargs):
        super(CustomPassReset, self).__init__(*args, **kwargs)
