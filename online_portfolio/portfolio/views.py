from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .forms import BasicInfoForm
from .helper import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PortfolioEdit(LoginRequiredMixin, View):
    template = "portfolio/portfolio_edit.html"

    def get(self, request):
        basic_info = get_basic_info(request.user)
        projects = get_projects_info(request.user)

        context = basic_info
        context["projects"] = projects

        return render(request, template_name=self.template, context=context)


class UpdateAboutSection(LoginRequiredMixin, View):
    """
    Updates the about section of the portfolio.
    """

    @staticmethod
    def post(request):
        data = {
            "name": request.POST["name"].strip(),
            "about": request.POST["about"],
            "tag_line": request.POST["tagline"],
        }

        basic_info = request.user.basicinfo

        # validate the data
        form = BasicInfoForm(data)

        # show error if data is invalid
        if not form.is_valid():
            print(form.errors)
            return JsonResponse({"success": False, "message": "error"})

        basic_info.update(data)
        basic_info.save()

        return JsonResponse({"success": True, "message": "success"})


class AddProject(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        print(request.POST)
