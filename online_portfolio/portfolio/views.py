from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PortfolioEdit(LoginRequiredMixin, View):
    template = "portfolio/portfolio_edit.html"

    def get(self, request):
        return render(request, template_name=self.template)
