from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from .models import *
from django.contrib.auth.forms import UserCreationForm
import pandas as pd



def homepage(request):
   return render(request, template_name="main/inicio.html")

def homepage1(request):
   return render(request, template_name="main/criarUC.html")

def homepage2(request):
   name=Docente.objects.all()
   UC = UnidadesCurriculares.objects.all()
   if request.method == "POST":
      uc_list = request.POST.getlist('unc')
      dia = request.POST['data']
      assunto = request.POST['assunto']
      desc = request.POST['desc']
      descri_list = request.POST.getlist('descri')
      hora_inicio_list = request.POST.getlist('hora_inicio')
      hora_fim_list = request.POST.getlist('hora_fim')
      tarefa = request.POST.getlist('tarefa')
      dia2 =request.POST.getlist('data2')
      if Pedido.objects.filter(assunto=assunto, dia=dia).exists():
            # Se já existir, retorne uma mensagem de erro
            error = 'Já existe um pedido com o mesmo assunto'
            return render(request, 'main/PedidoHorario.html', {'error': error, "nome": name,"UC": UC})
        
      
      new_pedido = Pedido(assunto=assunto,desc=desc,dia=dia, tipo="Horário")
      new_pedido.save()
      
      for i in range(len(uc_list)):
         new_pedido_hor = PedidoHorario(
            uc=uc_list[i],
            hora_inicio=hora_inicio_list[i],
            hora_fim=hora_fim_list[i],
            descri=descri_list[i],
            pedido=new_pedido,
            tarefa=tarefa[i],
            dia=dia2[i]
         )
         new_pedido_hor.save()
  
   return render(request, template_name="main/PedidoHorario.html",context={"nome": name,"UC": UC})


def PeidosOUT(request):
    name = Docente.objects.all()
    if request.method == "POST":
        assunto = request.POST['assunto']
        descricao = request.POST['desc']
        data = request.POST['dia']

        new_PedidoOutros = PedidosOutros(assunto=assunto, descricao=descricao, dia=data)
        new_PedidoOutros.save()

    return render(request, template_name="main/PedidosOutros.html", context={"nome": name})

def UPDATEPeidosOUT(request, pk):
    PedidosOut = PedidosOutros.objects.get(id=pk)
    if request.method == "POST":
        PedidosOut.assunto = request.POST['assunto']
        PedidosOut.descricao = request.POST['desc']
        PedidosOut.dia = request.POST['dia']

        PedidosOut.save()
        return redirect('main:meus')

    return render(request, template_name="main/PedidosOutros.html", context={"assunto": PedidosOut.assunto,"desc": PedidosOut.descricao, "dia":PedidosOut.dia})

def meus(request):
   pedidosoutro = PedidosOutros.objects.all()
   return render(request, template_name="main/bulma_table.html",context={"Pedido":pedidosoutro})


def homepage5(request):
   return render(request, template_name="main/app.html")

def register(request):
   return render(request, template_name="users/criar_utilizador.html")

def deletOutros(request,pk):
   PedidosOut = PedidosOutros.objects.get(id=pk)
   if request.method == "POST":
      PedidosOut.delete()
      return redirect('/meus')
   return render(request, template_name="main/delete.html",context={'item': PedidosOut})


def tableHorario(request):
   pedidoshorario = Pedido.objects.all()
   pedidoshorarios = PedidoHorario.objects.all()
   funciona = Funcionario.objects.all()
   if request.method == 'POST':
      nome = request.POST.get('funcionari')
      funcionario = Funcionario.objects.get(nome=nome)
      pedido_id = request.POST.get('pedido_id') 
      pedido = Pedido.objects.get(id=pedido_id)
      pedido.Funcionario = funcionario
      pedido.atribuido ="Atribuido"
      pedido.save()
  
   return render(request, template_name="main/tableHorario.html",context={"Pedido":pedidoshorario, "item":pedidoshorarios, "funcio":funciona})

def tableHorario2(request, pk):
   try:
        pedido = Pedido.objects.get(id=pk)
        pedidoshorario = PedidoHorario.objects.filter(pedido=pedido)
   except Pedido.DoesNotExist:
        return HttpResponseNotFound('Pedido não encontrado')
   return render(request, template_name="main/tableHorario2.html",context={"Pedido":pedidoshorario})

def updateHorario(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido_horario = PedidoHorario.objects.filter(pedido=pk).first()
    UC = UnidadesCurriculares.objects.all()
    if request.method == "POST":
        pedido.dia = request.POST['data']
        pedido.assunto = request.POST['assunto']
        pedido.desc = request.POST['desc']
        pedido.save()
        return redirect('main:tableHorario')
    return render(request, template_name="main/PedidoHorario2.html", context={
        "assunto": pedido.assunto,
        "desc": pedido.desc,
        "dia": pedido.dia,
      
    })

def uploadRUC(request):
    if request.method == 'POST':
        if not request.FILES:
            error = 'Selecione um arquivo para fazer o upload'
            return render(request=request, template_name='main/IMPORTCSV.html', context={'error': error})
        if not request.FILES['file'].name.endswith('.xlsx'):
            error = 'O arquivo deve estar no formato .xlsx'
            return render(request=request, template_name='main/IMPORTCSV.html', context={'error': error})
        excel_file = request.FILES['file']
        excel_data = pd.ExcelFile(excel_file)
        sheetx = pd.read_excel(excel_data, sheet_name=0)
        testes = sheetx[['Ano letivo', 'Docente', 'Regência', 'Tipo', 'Horas']] 

        for index, row in testes.iterrows():
            AnoLetivo = row['Ano letivo']
            Docente = row['Docente']
            Regencia = row['Regência']
            Tipo = row['Tipo']
            Horas = row['Horas']
            #Codigo = row['Codigo']
            #Desc = row['Descrição']

            
            novAUC = UnidadesCurriculares(AnoLetivo=AnoLetivo,Docentes=Docente,Regência=Regencia,Tipo=Tipo,Horas=Horas)
            novAUC.save()
            succes = 'Importado para a base de dados'
        return render(request=request, template_name='main/IMPORTCSV.html', context={"succes": succes})
    return render(request=request, template_name='main/IMPORTCSV.html')



def updateHorario2(request, pk):
    pedido_horario = PedidoHorario.objects.get(id=pk)
    UC = UnidadesCurriculares.objects.all()
    if request.method == "POST":
        pedido_horario.hora_fim = request.POST['hora_inicio']
        pedido_horario.hora_inicio = request.POST['hora_fim']
        pedido_horario.descri = request.POST['descri']
        pedido_horario.uc = request.POST['unc']
        pedido_horario.save()
        return redirect(reverse('main:tableHorario2', kwargs={'pk': pedido_horario.pedido.id}))
    return render(request, template_name="main/PedidoHorario3.html", context={"UC" : UC,
        "hora_fim": pedido_horario.hora_fim,
        "hora_inicio": pedido_horario.hora_inicio,
        "unc": pedido_horario.uc,
        "descri": pedido_horario.descri,
      
    })

def deletHorario(request,pk):
   PedidosHor = Pedido.objects.get(id=pk)
   if request.method == "POST":
      PedidosHor.delete()
      return redirect('/tableHorario')
   return render(request, template_name="main/deleteH.html",context={'item': PedidosHor})

def deletHorario2(request,pk):
   PedidosHor = PedidoHorario.objects.get(id=pk)
   if request.method == "POST":
      PedidosHor.delete()
      return redirect(reverse('main:tableHorario2', kwargs={'pk': PedidosHor.pedido.id}))
   return render(request, template_name="main/deleteH2.html",context={'item': PedidosHor})

def UnidadeCurricular(request):
   UC = UnidadesCurriculares.objects.all()
   if request.method == "POST":
      num_requests = int(request.POST.get('num_requests', 0))
      date = request.POST['data']
      assunto = request.POST['assunto']
      desc = request.POST['desc']
      new_Pedido = Pedido(assunto=assunto,desc=desc,dia=date)
      new_Pedido.save()
      pedido_id = new_Pedido.id
      pedido = Pedido.objects.get(id=pedido_id)
      for i in range(num_requests):
         uc = request.POST.get(f'unc_{i}')
         tarefa = request.POST.get(f'tarefa_{i}')
         descri = request.POST.get(f'descri_{i}')

         new_PedidoUC = PedidoUC(uc=uc,tarefa=tarefa,descri=descri,pedido=pedido)
         new_PedidoUC.save() # save the new_PedidoUC object to the database
   return render(request, template_name="main/PedidoUC.html",context={"UC": UC})

def tableUC(request):
   pedidosUC = PedidoUC.objects.all()
   return render(request, template_name="main/tableUC.html",context={"Pedido":pedidosUC})

def updateUC(request, pk):
    pedido_UC = PedidoUC.objects.get(id=pk)
    UC = UnidadesCurriculares.objects.all()
    if request.method == "POST":
      pedido_UC.uc= request.POST['unc']
      pedido_UC.dia = request.POST['data']
      pedido_UC.assunto = request.POST['assunto']
      pedido_UC.desc = request.POST['desc']
      pedido_UC.save()
      
      return redirect('main:tableUC')
    return render(request, template_name="main/PedidoUC.html", context={"unc": pedido_UC.uc, "desc": pedido_UC.desc, "dia" : pedido_UC.dia, "assunto" : pedido_UC.assunto, "UC" : UC})

def deletUC(request,pk):
   PedidosUC = PedidoUC.objects.get(id=pk)
   if request.method == "POST":
      PedidosUC.delete()
      return redirect('/tableUC')
   return render(request, template_name="main/deleteUC.html",context={'item': PedidosUC})


def PedidoSalas(request):
   Salas = Sala.objects.all()
   Edificios = Edificio.objects.all()
   if request.method == "POST":
      salaa= request.POST['salaa']
      edifi= request.POST['edifi']
      dia= request.POST['dia']
      assunto = request.POST['assunto'] 
      hora_de_inicio = request.POST['hora_inicio']
      hora_de_fim= request.POST['hora_fim']
      desc = request.POST['desc']

      new_PedidoSala = PedidoSala(edi=edifi, sal=salaa, dia = dia,
                                 hora_de_inicio = hora_de_inicio, hora_de_fim = hora_de_fim, desc=desc,assunto=assunto)
      new_PedidoSala.save()
   return render(request, template_name="main/PedidoSala.html",context={"Sala": Salas, "Edificio": Edificios})

def tableSala(request):
   pedidosSala = PedidoSala.objects.all()
   return render(request, template_name="main/tableSala.html",context={"Pedido":pedidosSala})

def updateSala(request, pk):
    pedido_Sala = PedidoSala.objects.get(id=pk)
    Salas = Sala.objects.all()
    Edificios = Edificio.objects.all()
    if request.method == "POST":
      pedido_Sala.sal= request.POST['salaa']
      pedido_Sala.edi = request.POST['edifi']
      pedido_Sala.dia = request.POST['dia']
      pedido_Sala.assunto = request.POST['assunto']
      pedido_Sala.hora_de_inicio = request.POST['hora_inicio']
      pedido_Sala.hora_de_fim = request.POST['hora_fim']
      pedido_Sala.desc = request.POST['desc']
      pedido_Sala.save()
   
      
      return redirect('main:tableSala')
    return render(request, template_name="main/PedidoSala.html", context={"Edificio": Edificios, "Sala" : Salas ,"salaa": pedido_Sala.sal, "edifi": pedido_Sala.edi,
                                                                           "dia" : pedido_Sala.dia, "desc" : pedido_Sala.desc, "hora_inicio" : pedido_Sala.hora_de_inicio, "hora_fim" : pedido_Sala.hora_de_fim, "assunto" : pedido_Sala.assunto})

def deletSala(request,pk):
   PedidosSala = PedidoSala.objects.get(id=pk)
   if request.method == "POST":
      PedidosSala.delete()
      return redirect('/tableSala')
   return render(request, template_name="main/deleteS.html",context={'item': PedidosSala})


def tableEstatisticaPedido(request):
   
   num_pedidos = Pedido.objects.all().count()
   # Obter o número de pedidos com o status "Em Análise"
   num_pedidos_em_analise = Pedido.objects.filter(status='Em Análise').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Em Análise')
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()

   # Obter o número de pedidos com o status "Concluido"
   num_pedidos_em_analise = Pedido.objects.filter(status='Concluído').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Concluido')
   estatistica_pedido_em_analise.NmrPedido = num_pedidos_em_analise
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()

   # Obter o número de pedidos com o status "Rejeitado"
   num_pedidos_em_analise = Pedido.objects.filter(status='Rejeitado').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Rejeitado')
   estatistica_pedido_em_analise.NmrPedido = num_pedidos_em_analise
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()

   # Obter o número de pedidos com o status "Novo"
   num_pedidos_em_analise = Pedido.objects.filter(status='Novo').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Novo')
   estatistica_pedido_em_analise.NmrPedido = num_pedidos_em_analise
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()

   # Obter o número de pedidos com o status "Em processamento"
   num_pedidos_em_analise = Pedido.objects.filter(status='Em processamento').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Em processamento')
   estatistica_pedido_em_analise.NmrPedido = num_pedidos_em_analise
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()

   # Obter o número de pedidos com o status "Em espera"
   num_pedidos_em_analise = Pedido.objects.filter(status='Em espera').count()
   estatistica_pedido_em_analise = EstatisticaPedido.objects.get(Status='Em espera')
   estatistica_pedido_em_analise.NmrPedido = num_pedidos_em_analise
   porcentagem_analise = (num_pedidos_em_analise / num_pedidos) * 100
   texto_formatado = '{:.1f}%'.format(porcentagem_analise)
   estatistica_pedido_em_analise.percetagem =texto_formatado
   estatistica_pedido_em_analise.save()


   

   pedidosSala = EstatisticaPedido.objects.all()
   return render(request, template_name="main/tableEstatisticaPedidos.html",context={"Pedido":pedidosSala})