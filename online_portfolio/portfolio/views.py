from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .forms import BasicInfoForm, ProjectForm
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
        print(request.POST)
        data = {
            "name": request.POST["name"].strip(),
            "about": request.POST["about"],
            "tag_line": request.POST["tagline"],
            "profile_pic": request.POST["profile_pic"],
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


class EditProjects(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        project_id = int(request.POST["id"])
        project = Project.objects.get(pk=project_id)

        if project.user_profile != request.user.basicinfo:
            return JsonResponse({"success": False, "message": "error"})

        _get = request.POST.get

        data = {
            "title": _get("title", project.title),
            "description": _get("description", project.description),
            "skills": _get("skills", project.skills),
            "live_link": _get("liveLink", project.live_link),
            "code_link": _get("codeLink", project.code_link),
            "image": _get("image", project.image),
        }

        form = ProjectForm(data, instance=project)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse({"success": False, "message": "error"})

        form.save()
        return JsonResponse({"success": True, "message": "success"})


class DeleteProject(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        id_ = int(request.POST["id"])
        project = Project.objects.get(pk=id_)

        if project.user_profile != request.user.basicinfo:
            return JsonResponse({"success": True, "message": "error"})

        project.delete()

        basic_info = request.user.basicinfo
        basic_info.total_projects -= 1
        basic_info.save()

        return JsonResponse({"success": True, "message": "success"})


class AddNewProject(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        total_projects = request.user.basicinfo.total_projects

        if total_projects >= 10:
            return JsonResponse(
                {"success": False, "message": "You cannot have more than 10 projects"}
            )

        project = Project(user_profile=request.user.basicinfo)
        project.save()

        basic_info = request.user.basicinfo
        basic_info.total_projects += 1
        basic_info.save()

        project_data = project.to_dict()
        return JsonResponse(
            {"success": True, "message": "success", "project_data": project_data}
        )
