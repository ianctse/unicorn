from django.urls import path

from . import views

app_name = 'pvmodules'
urlpatterns = [
    path('', views.PvModuleIndexView.as_view(), name='index'),
    path('<int:pk>/', views.PvModuleView.as_view(), name='pvmodule'),
    path('mfg/<int:company_id>/', views.ManufacturerView.as_view(), name='manufacturer'),
    path('<int:pvmodule_id>/datasheet/<int:pk>/', views.PvModuleDatasheetView.as_view(), name='pvmoduledatasheet')
]