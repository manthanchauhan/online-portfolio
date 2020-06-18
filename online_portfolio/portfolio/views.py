from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PortfolioEdit(LoginRequiredMixin, View):
    template = "portfolio/portfolio_edit.html"

    def get(self, request):
        return render(request, template_name=self.template)


class UpdateAboutSection(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        print(request.POST)

        return JsonResponse({"success": True, "message": "success"})
