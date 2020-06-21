from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from .models import BasicInfo
from .forms import BasicInfoForm
from .helper import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PortfolioEdit(LoginRequiredMixin, View):
    template = "portfolio/portfolio_edit.html"

    def get(self, request):
        email = request.user.email

        # if basic_info of user does not exists, default basic info will be shown
        basic_info = list(
            BasicInfo.objects.filter(pk__in=[email, settings.DEFAULT_PORTFOLIO])
        )

        if len(basic_info) > 1:
            basic_info = list(
                filter(lambda x: True if x.email == email else False, basic_info)
            )

        basic_info = basic_info[0]

        context = {
            "name": basic_info.name,
            "phone1": basic_info.phone1,
            "phone2": basic_info.phone2,
            "about": basic_info.about,
            "tag_line": basic_info.tag_line,
            "call_of_contact": basic_info.call_of_contact,
        }

        return render(request, template_name=self.template, context=context)


class UpdateAboutSection(LoginRequiredMixin, View):
    """
    Updates the about section of the portfolio.
    """

    @staticmethod
    def post(request):
        user_email = request.user.email

        data = {
            "name": request.POST["name"].strip(),
            "email": user_email,
            "about": request.POST["about"],
            "tag_line": request.POST["tagline"],
            "profile_pic": None,
        }

        # check if BasicInfo object exists.
        infos = BasicInfo.objects.filter(email=user_email)

        if infos.count() == 0:
            # validate the data
            form = BasicInfoForm(data)

            # show error if data is invalid
            if not form.is_valid():
                print(form.errors)
                return JsonResponse({"success": False, "message": "error"})

            form.save()
        else:
            basic_info = list(infos)[0]
            basic_info.update(data)

            try:
                basic_info.save()
            except Exception as e:
                print(e)
                return JsonResponse({"success": True, "message": "error"})

        return JsonResponse({"success": True, "message": "success"})
