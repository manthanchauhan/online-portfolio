from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from http import HTTPStatus
from django.template.loader import render_to_string
from online_portfolio.classes import MediaStorage

from .forms import BasicInfoForm, ProjectForm
import os
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
        basic_info = request.user.basicinfo

        name = (
            request.POST["name"].strip()
            if request.POST.get("name", "") != ""
            else basic_info.name
        )
        tagline = (
            request.POST["tag_line"].strip()
            if request.POST.get("tag_line", "") != ""
            else basic_info.tag_line
        )
        about = (
            request.POST["about"].strip()
            if request.POST.get("about", "") != ""
            else basic_info.about
        )
        picture = (
            request.POST["profile_pic"]
            if request.POST.get("profile_pic", "") != ""
            else basic_info.profile_pic
        )

        data = {
            "name": name,
            "about": about,
            "tag_line": tagline,
            "profile_pic": picture,
        }

        form = BasicInfoForm(data)

        # show error if data is invalid
        if not form.is_valid():
            error_dict = dict(form.errors.items())
            print(error_dict)

            return JsonResponse(
                data=error_dict,
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
                reason="Invalid Data",
            )

        basic_info.update(data)
        basic_info.save()

        return JsonResponse(
            data={}, status=HTTPStatus.OK, reason="Data Edited Successfully!"
        )


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
            return JsonResponse({"success": False, "message": "error"})

        if request.user.basicinfo.total_projects == 1:
            return JsonResponse(
                {"succes": False, "message": "Cannot Delete All Projects"}
            )

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

        project = create_default_project(request.user)

        project_data = project.to_dict()
        return JsonResponse(
            {"success": True, "message": "success", "project_data": project_data}
        )


class ExportPortfolio(LoginRequiredMixin, View):
    template = "portfolio/portfolio_export.html"

    def post(self, request):
        # print(request.POST)
        basic_info = request.user.basicinfo
        about_data = {
            "name": basic_info.name,
            "profile_pic": basic_info.profile_pic,
            "tag_line": basic_info.tag_line,
            "about": as_markdown(basic_info.about),
        }

        projects = Project.objects.filter(user_profile=request.user.basicinfo)
        projects = [project.to_dict() for project in projects]

        for project in projects:
            project["description"] = as_markdown(project["description"])

        context = {
            "projects": projects,
            "username": request.user.username,
            "avoid_navbar": True,
            "copyright_link": request.scheme + "://" + request.get_host(),
            "copyright_value": request.get_host(),
        }
        context = {**context, **about_data}

        portfolio = render_to_string(self.template, context)

        with open(os.path.join(settings.BASE_DIR, "media", "port.html"), "wb") as file:
            file.write(portfolio.encode("utf-8"))

        with open(os.path.join(settings.BASE_DIR, "media", "port.html"), "rb") as file:
            fs = MediaStorage()
            file = fs.save(request.user.username + "portfolio.html", file)
            url = fs.url(file)
            basic_info.portfolio = url

        basic_info.save()
        os.remove(os.path.join(settings.BASE_DIR, "media", "port.html"))

        return JsonResponse({"success": True, "message": "success", "url": url})
