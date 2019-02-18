from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Manufacturer, PvModule, PvModuleDatasheet

class ManufacturerView(generic.DetailView):

    model = Manufacturer
    template_name = 'pvmodules/manufacturer.html'

class PvModuleIndexView(generic.ListView):

    template_name = 'pvmodules/pvmoduleindex.html'
    context_object_name = 'pvmodule_models_list'

    def get_queryset(self):
        """Return all pvmodules."""
        return PvModule.objects.order_by('manufacturer', 'model_name')[:25]

class PvModuleView(generic.DetailView):

    model = PvModule
    template_name = 'pvmodules/pvmoduledetail.html'

class PvModuleDatasheetView(generic.DetailView):

    model = PvModuleDatasheet
    template_name = 'pvmodules/pvmoduledatasheet.html'