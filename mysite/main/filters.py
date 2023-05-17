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
        

get_valido_choices = [
    ('True', 'Confirmado'),
    ('False', 'Por confirmar'),
    ('Rejeitado', 'Rejeitado'),
]


def filter_nome(queryset, name, value):
    for term in value.split():
        queryset = queryset.filter(Q(first_name__icontains=term)
                                   | Q(last_name__icontains=term))
    return queryset


class UtilizadoresFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(method=filter_nome)
    valido = django_filters.MultipleChoiceFilter(choices=get_valido_choices)

    class Meta:
        model = Utilizador
        fields = '__all__'
