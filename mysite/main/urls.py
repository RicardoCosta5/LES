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
from .views import consultar_utilizadores

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
    path('mensagem/<int:id>', views.mensagem,name='mensagem'),
    path("login", views.login_action, name="login"),
    path("register/<int:id>", views.register, name="register"),
    path("escolher", views.escolher, name="escolher"),
    path("logout", views.logout_action, name="logout"),
    path('consultarutilizadores', consultar_utilizadores.as_view(), name='consultar-utilizadores'),
    path('validarutilizador/<int:id>', views.validar_utilizador,name='validar-utilizador'),
    path('rejeitarutilizador/<int:id>', views.rejeitar_utilizador,name='rejeitar-utilizador'),
    path('validar/<str:nome>/<int:id>', views.enviar_email_validar,name='validar'),
    path('rejeitar/<str:nome>/<int:id>', views.enviar_email_rejeitar,name='rejeitar'),
    path('alterarutilizadoradmin/<int:id>', views.alterar_utilizador_admin,name='alterar-utilizador-admin'),
    path('apagarutilizador/<int:id>', views.apagar_utilizador,name='apagar-utilizador'),
    path('mudarperfilescolha/<int:id>', views.mudar_perfil_escolha_admin,name='mudar-perfil-escolha-admin'),
#Tabelas
    path ("tablePedidos", views.tablePedidos, name="tablePedidos"),
    path ("tablePedidos2/<str:pk>/", views.tablePedidos2, name="tablePedidos2"),
    path ("tableEstatisticaPedido", views.tableEstatisticaPedido, name="tableEstatisticaPedido"),
    path('concluirregisto/<int:id>', views.concluir_registo,name='concluir-registo'),
    path('ajax/load-departamentos/', views.load_departamentos, name='ajax_load_departamentos'),
    path('ajax/load-cursos/', views.load_cursos, name='ajax_load_cursos'),
    path('validarpedido/<str:nome>/<int:id>/<int:pedidoid>', views.enviar_email_validarpedido,name='validarpedido'),
    path('rejeitarpedido/<str:nome>/<int:id>/<int:pedidoid>', views.enviar_email_rejeitarpedido,name='rejeitarpedido'),
    path('validarp/<int:id>/<int:pedidoid>', views.validar_p,name='validarp'),
    path('rejeitarp/<int:id>/<int:pedidoid>', views.rejeitar_p,name='rejeitarp'),



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


    path("export", views.export, name = "export"),
    path("exportHorarios", views.exportHorarios, name = "exportHorarios"),
    path("exportOutros", views.exportOutros, name="exportOutros"),
    path("exportSalas", views.exportSalas, name="exportSalas"),
    


]
