import django_filters
from .models import *
from django_filters import DateFilter, CharFilter
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'  # Formato de data desejado

class PedidoFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='dia', lookup_expr='gte', widget=DateInput())
    end_date = DateFilter(field_name='dia', lookup_expr='lte', widget=DateInput())
    assunto = CharFilter(field_name='assunto', lookup_expr='icontains')
    tipo = CharFilter(field_name='tipo', lookup_expr='icontains')
    status = CharFilter(field_name='status', lookup_expr='icontains')
    atribuido = CharFilter(field_name='atribuido', lookup_expr='icontains')
    class Meta:
        model = Pedido
        fields = '__all__'
        