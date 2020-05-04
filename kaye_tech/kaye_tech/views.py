from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# @method_decorator(login_required(login_url="/accounts/splash"), name="dispatch")
class IndexView(TemplateView):
    template_name = "index.html"
