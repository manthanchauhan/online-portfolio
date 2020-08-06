from django.views import View
from django.shortcuts import redirect, render


class Home(View):
    @staticmethod
    def get(request):
        return redirect("portfolio:portfolio_edit")


class About(View):
    template_name = "about.html"

    def get(self, request):
        return render(request, template_name=self.template_name)
