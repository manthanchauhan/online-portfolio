from django.views import View
from django.shortcuts import redirect


class Home(View):
    @staticmethod
    def get(request):
        return redirect("accounts:login")
