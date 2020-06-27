"""online_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("edit/", views.PortfolioEdit.as_view(), name="portfolio_edit"),
    path("update_about/", views.UpdateAboutSection.as_view(), name="update_about"),
    path("edit_projects/", views.EditProjects.as_view(), name="edit_projects"),
    path("delete_project/", views.DeleteProject.as_view(), name="delete_project"),
    path("add_project/", views.AddNewProject.as_view(), name="add_project"),
    path("export_portfolio/", views.ExportPortfolio.as_view(), name="export_portfolio"),
]
