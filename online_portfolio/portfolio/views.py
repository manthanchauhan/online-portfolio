from django.shortcuts import render
from django.views import View

# Create your views here.
class PortfolioEdit(View):
    template = "portfolio/portfolio_edit.html"

    def get(self, request):
        return render(request, template_name=self.template)
