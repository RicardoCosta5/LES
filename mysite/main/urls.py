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

    
    path ("outros", views.PedidosOUT, name="outros"),
    path ("update_outros/<str:pk>/",views.UPDATEPeidosOUT,name="update_outros"),
    path ("delete_outros/<str:pk>/",views.deletOutros,name="delete_outros"),

    path("Sala", views.PedidoSalas,name="Sala"),
    path ("update_Sala/<str:pk>/",views.updateSala,name="update_Sala"),
    path ("delete_Sala/<str:pk>/",views.deletSala,name="delete_Sala"),


#Login e register

    path("login", views.login, name="login"),
    path("register/<int:id>", views.register, name="register"),
    path("escolher", views.escolher, name="escolher"),

#Tabelas
    path ("tablePedidos", views.tablePedidos, name="tablePedidos"),
    path ("tablePedidos2/<str:pk>/", views.tablePedidos2, name="tablePedidos2"),
    path ("tableEstatisticaPedido", views.tableEstatisticaPedido, name="tableEstatisticaPedido"),


   



#Uploads
    path ("UploadRUC",views.uploadRUC,name="upload_RUC"),
    path("upload_DSD", views.uploadDSD, name="upload_DSD"),
    path('Upload_Docentes', views.uploadDocente, name='Upload_Docentes'),
    path("Upload_Salas", views.uploadSALAS, name="Upload_Salas"),

#Ano letivo
    path("AnoLetivo", views.AnoLetivoAdd, name="AnoLetivo"),
    path ("tableAL", views.tableAL, name="tableAL"),
    path ("delete_AL/<str:pk>/",views.deletAL,name="delete_AL"),
    path ("update_AL/<str:pk>/",views.updateAL,name="update_AL"),    



    
    


]
