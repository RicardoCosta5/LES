"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="home"),
    path('uc', views.homepage1, name="site1"),
    path('horario', views.homepage2, name="site2"),
    path("home", views.homepage, name="homepage"),
    path ("home", views.homepage, name="home"),
    path ("app", views.homepage5, name="app"),
    path ("register", views.meus, name="register"),
    path ("meus", views.meus, name="meus"),
    path ("outros", views.PeidosOUT, name="outros"),
    path ("update_outros/<str:pk>/",views.UPDATEPeidosOUT,name="update_outros"),
    path ("delete_outros/<str:pk>/",views.deletOutros,name="delete_outros"),

    path ("tableHorario2/<str:pk>/", views.tableHorario2, name="tableHorario2"),
    path ("update_horario2/<str:pk>/",views.updateHorario2,name="update_horario2"),
    path ("delete_horario2/<str:pk>/",views.deletHorario2,name="delete_horario2"),

    path ("tableHorario", views.tableHorario, name="tableHorario"),
    path ("update_horario/<str:pk>/",views.updateHorario,name="update_horario"),
    path ("delete_horario/<str:pk>/",views.deletHorario,name="delete_horario"),

    path("UnidadeCurricular", views.UnidadeCurricular,name="UnidadeCurricular"),
    path ("tableUC", views.tableUC, name="tableUC"),
    path ("update_UC/<str:pk>/",views.updateUC,name="update_UC"),
    path ("delete_UC/<str:pk>/",views.deletUC,name="delete_UC"),

    path("Sala", views.PedidoSalas,name="Sala"),
    path ("tableSala", views.tableSala, name="tableSala"),
    path ("update_Sala/<str:pk>/",views.updateSala,name="update_Sala"),
    path ("delete_Sala/<str:pk>/",views.deletSala,name="delete_Sala"),

    path ("UploadRUC",views.uploadRUC,name="upload_RUC"),
     path ("tableEstatisticaPedido", views.tableEstatisticaPedido, name="tableEstatisticaPedido"),


    
    


]
