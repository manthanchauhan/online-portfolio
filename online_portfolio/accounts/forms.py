from django import forms
from django.contrib.auth.models import User


def existing_email(email):
    """
    It is a validator which checks if the any user with the given email exists in the system.
    :param email: email to check
    :type: str
    :rtype: bool
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # no such user exists
        return

    # user exists
    raise forms.ValidationError("User with this email already exists. Please login.")


class EnterEmailForm(forms.Form):
    user_email = forms.EmailField(
        label="Enter Email Here",
        max_length=100,
        validators=[existing_email],
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter Your Email", "class": "form-control"}
        ),
    )
