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
    #Home page
    path("", views.homepage, name="home"),
    path("home", views.homepage, name="homepage"),
    path ("home", views.homepage, name="home"),
    path ("app", views.homepage5, name="app"),
    
    #Fazer Pedidos
    path("UnidadeCurricular", views.PedidoUnidadeCurricular,name="UnidadeCurricular"),
    path ("update_UC/<str:pk>/",views.updateUC,name="update_UC"),
    path ("delete_UC/<str:pk>/",views.deletUC,name="delete_UC"),

    
    path('horario', views.PedidoHorarios, name="site2"),
    path ("update_horario/<str:pk>/",views.updateHorario,name="update_horario"),
    path ("delete_horario/<str:pk>/",views.deletHorario,name="delete_horario"),

    
    path ("outros", views.PeidosOUT, name="outros"),
    path ("update_outros/<str:pk>/",views.UPDATEPeidosOUT,name="update_outros"),
    path ("delete_outros/<str:pk>/",views.deletOutros,name="delete_outros"),

    path("Sala", views.PedidoSalas,name="Sala"),
    path ("update_Sala/<str:pk>/",views.updateSala,name="update_Sala"),
    path ("delete_Sala/<str:pk>/",views.deletSala,name="delete_Sala"),


#Login e register

    path ("register", views.meus, name="register"),
    path ("meus", views.meus, name="meus"),


#Tabelas
    path ("tablePedidos", views.tablePedidos, name="tablePedidos"),
    path ("tableEstatisticaPedido", views.tableEstatisticaPedido, name="tableEstatisticaPedido"),

    path ("tableHorario2/<str:pk>/", views.tableHorario2, name="tableHorario2"),
    path ("update_horario2/<str:pk>/",views.updateHorario2,name="update_horario2"),
    path ("delete_horario2/<str:pk>/",views.deletHorario2,name="delete_horario2"),



#Uploads
    path ("UploadRUC",views.uploadRUC,name="upload_RUC"),



    
    


]
