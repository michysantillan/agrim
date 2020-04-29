import json
from django.conf import settings
from django.contrib import messages
from django.utils.safestring import SafeString
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.gis.serializers import geojson
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth.models import User
# Authentication imports
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.urls import reverse_lazy

from cms.views import (
    BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
)

from .models import Area
from .forms import  AreaForm
from .convert_geometry import ConvertGeometry


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url =  reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class GoogleApiMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_key'] = settings.GOOGLE_API_KEY
        return context

@method_decorator(login_required, name='dispatch')
class AreaListView(GoogleApiMixin, BaseListView):

    model = Area
    paginate_by = 100  # if pagination is desired



@method_decorator(login_required, name='dispatch')
class AreaCreate(GoogleApiMixin, BaseCreateView):
    model = Area
    form_class = AreaForm
    template_name = 'geo/area_form.html'

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        form.instance.user = self.request.user
             
        if self.request.is_ajax():
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            messages.success(self.request, 'La zona ha sido guardada con exito!')
            return JsonResponse({
                'success': True,
                'url': reverse('area-list'),
            })
        return super().form_valid(form)


class AreaUpdate(GoogleApiMixin, BaseUpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'geo/area_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g = geojson.Serializer()
        geo_data = Area.objects.filter(pk=self.kwargs['pk'])
        data = g.serialize(
            geo_data, geometry_field='geom', fields=('name',))
        context['geom'] = SafeString(json.loads(data))
        return context

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        
        if self.request.is_ajax():
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            messages.success(self.request, 'La zona se ha modificado con exito!')
            return JsonResponse({
                'success': True,
                'url': reverse('area-list'),
            })
        return super().form_valid(form)


class AreaDelete(GoogleApiMixin, BaseDeleteView):
    model = Area

class HomeView(GoogleApiMixin, TemplateView):
    template_name = "geo/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Area'] = Area.objects.all()
        context['form'] = AreaForm()
        return context

def home(request):
    return render(request, 'geo/index.html', {})