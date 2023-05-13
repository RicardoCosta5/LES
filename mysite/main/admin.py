from django.contrib import admin
from .models import *

admin.site.register(Docente)
admin.site.register(Funcionario)
admin.site.register(Horario)
admin.site.register(Outros)
admin.site.register(Pedido)
admin.site.register(PedidoHorario)
admin.site.register(PedidoSala)
admin.site.register(PedidosOutros)
admin.site.register(PedidoUC)
admin.site.register(Sala)
admin.site.register(Edificio)
admin.site.register(UnidadesCurriculares)
admin.site.register(EstatisticaPedido)

