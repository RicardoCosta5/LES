from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from .models import *
from django.contrib.auth.forms import UserCreationForm
import pandas as pd
from datetime import datetime

### Pagina Inicial ###
def homepage(request):
   return render(request, template_name="main/inicio.html")

### App ###
def homepage5(request):
   return render(request, template_name="main/app.html")

### Registo ###
def register(request):
   return render(request, template_name="users/criar_utilizador.html")

### Criação de Pedidos ###
def PedidoHorarios(request):
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
      for hora_inicio, hora_fim in zip(hora_inicio_list, hora_fim_list):
         try:
            datetime.strptime(hora_inicio, '%H:%M:%S')
            datetime.strptime(hora_fim, '%H:%M:%S')
         except ValueError:
            error = 'Formato de hora inválido'
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
      
      succes = 'Enviado para a base de dados'
      return render(request, template_name="main/PedidoHorario.html",context={"nome": name,"UC": UC,"succes": succes})
  
   return render(request, template_name="main/PedidoHorario.html",context={"nome": name,"UC": UC})


def PedidosOUT(request):
    name = Docente.objects.all()
    if request.method == "POST":
        assunto = request.POST['assunto']
        descricao = request.POST['desc']
        data = request.POST['dia']
        arquivo = request.FILES.getlist('resume')

        new_Pedido = Pedido(assunto=assunto, desc=descricao, dia=data, tipo = "outros")
        new_Pedido.save()

        for i in range(len(arquivo)):
           new_pedido_outros = PedidosOutros(
           arquivo = arquivo[i],
           pedido = new_Pedido   
           )
           new_pedido_outros.save()

    return render(request, template_name="main/PedidosOutros.html", context={"nome": name})


def PedidoUnidadeCurricular(request):
      UC = UnidadesCurriculares.objects.all()
      if request.method == "POST":
         date = request.POST['data']
         assunto = request.POST['assunto']
         desc = request.POST['desc']

         uc_list = request.POST.getlist('unc')
         tarefa = request.POST.getlist('tarefa')
         regente = request.POST.getlist('regente')
         descri = request.POST.getlist('descri')

         new_Pedido = Pedido(assunto=assunto,desc=desc,dia=date,tipo="Unidade Curricular")
         new_Pedido.save()

         
         for i in range(len(uc_list)):
            new_PedidoUC = PedidoUC(
               uc=uc_list[i],
               tarefa=tarefa[i],
               regente=regente[i],
               descri=descri[i], 
               pedido = new_Pedido
            )
            new_PedidoUC.save()
      return render(request, template_name="main/PedidoUC.html",context={"UC": UC})


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


### Update dos Pedidos ###
def updateHorario(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido_horario = PedidoHorario.objects.filter(pedido=pk).all()
    UC = UnidadesCurriculares.objects.all()
    if request.method == "POST":
        pedido.dia = request.POST['data']
        pedido.assunto = request.POST['assunto']
        pedido.desc = request.POST['desc']
        pedido.save()

        uc_list = request.POST.getlist('unc')
        descri_list = request.POST.getlist('descri')
        hora_inicio_list = request.POST.getlist('hora_inicio')
        hora_fim_list = request.POST.getlist('hora_fim')
        tarefa = request.POST.getlist('tarefa')
        dia2 =request.POST.getlist('data2')
        # Combine as listas em uma lista de tuplas
        updates = zip(pedido_horario, uc_list, descri_list, hora_inicio_list, hora_fim_list, tarefa, dia2)

        # Atualize os objetos PedidoHorario
        for pedido_horario, uc, descri, hora_inicio, hora_fim, tarefa, dia2 in updates:
            pedido_horario.uc = uc
            pedido_horario.descri = descri
            pedido_horario.hora_inicio = hora_inicio
            pedido_horario.hora_fim = hora_fim
            pedido_horario.tarefa = tarefa
            pedido_horario.dia = dia2
            pedido_horario.save()

        return redirect('main:tablePedidos')
    return render(request, template_name="main/PedidoHorario2.html", context={
        "assunto": pedido.assunto,
        "desc": pedido.desc,
        "dia": pedido.dia,
        "pedido_horario":pedido_horario,
        "UC": UC,
    })


def UPDATEPeidosOUT(request, pk):
    pedido = Pedido.objects.get(id=pk)
    if request.method == "POST":
        pedido.assunto = request.POST['assunto']
        pedido.desc = request.POST['desc']
        pedido.dia = request.POST['data']
        pedido.save()
        return redirect('main:meus')

    return render(request, template_name="main/PedidosOutros2.html", context={"assunto": pedido.assunto,"desc": pedido.desc, "dia":pedido.dia})


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


### Apagar Pedidos ###
def deletHorario(request,pk):
   PedidosHor = Pedido.objects.get(id=pk)
   if request.method == "POST":
      PedidosHor.delete()
      return redirect('/tablePedidos')
   return render(request, template_name="main/deleteH.html",context={'item': PedidosHor})



### Tabela Pedidos###
def tablePedidos(request):
   pedidoshorario = Pedido.objects.all()
   pedidoshorarios = PedidoHorario.objects.all()
   funciona = Funcionario.objects.all()
   
   if request.method == 'POST':
      pedido_id = request.POST.get('pedido_id') 
      pedido = Pedido.objects.get(id=pedido_id)
      
      if request.POST.get('desassociar'):
         pedido.Funcionario = None
         pedido.atribuido = "Não Atribuido"
      else:
         nome = request.POST.get('funcionari')
         funcionario = Funcionario.objects.get(nome=nome)
         pedido.Funcionario = funcionario
         pedido.atribuido = "Atribuido"
      
      pedido.save()
  
   return render(request, template_name="main/tableHorario.html",context={"Pedido":pedidoshorario, "item":pedidoshorarios, "funcio":funciona})


### Criar Ano Letivo ###
def AnoLetivoAdd(request):
   UC = UnidadesCurriculares.objects.all()
   if request.method == "POST":
      anoletivo = request.POST['anoletivo']
      datainicio = request.POST['datainicio']
      datafinal = request.POST['datafinal']
      new_ano = AnoLetivo(
         anoletivo = anoletivo,
         datainicio = datainicio,
         datafinal = datafinal
      )
      new_ano.save()
   return render(request, template_name="main/PedidoAL.html",context={"UC": UC})


### Update Ano Letivo ###
def updateAL(request, pk):
    pedido = AnoLetivo.objects.get(id=pk)
    if request.method == "POST":
        pedido.anoletivo = request.POST['anoletivo']
        pedido.datainicio = request.POST['datainicio']
        pedido.datafinal = request.POST['datafinal']
        pedido.save()
        return redirect('main:tableAL')
    return render(request, template_name="main/PedidoAL2.html", context={
        "anoletivo": pedido.anoletivo,
        "datainicio": pedido.datainicio,
        "datafinal": pedido.datafinal,
      
    })


### Apagar Ano Letivo ###
def deletAL(request,pk):
   PedidosAL = AnoLetivo.objects.get(id=pk)
   if request.method == "POST":
      PedidosAL.delete()
      return redirect('/tableAL')
   return render(request, template_name="main/deleteAL.html",context={'item': PedidosAL})


### Tabela Ano Letivo ###
def tableAL(request):
   pedidosAL = AnoLetivo.objects.all()
   return render(request, template_name="main/tableAL.html",context={"AnoLetivo":pedidosAL})



### Importações ###
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


def uploadDSD(request):
    if request.method == 'POST':
        if not request.FILES:
            error = 'Selecione um arquivo para fazer o upload'
            return render(request=request, template_name='main/upload_DSD.html', context={'error': error})
        if not request.FILES['file'].name.endswith('.xls'):
            error = 'O arquivo deve estar no formato .xls'
            return render(request=request, template_name='main/upload_DSD.html', context={'error': error})
        excel_file = request.FILES['file']
        excel_data = pd.ExcelFile(excel_file)
        sheetx = pd.read_excel(excel_data, sheet_name=0)
        testes = sheetx[['Período', 'Cód. disciplina', 'Disciplina', 'Inst. discip.', 'Inst. disciplina', 'Depart. disciplina', 'Turma', 'Código curso', 'Curso',
                         'Cód. Docente', 'Docente', 'Função docente', 'Inst. docente', 'Depart. docente', 'Horas semanais', 'Horas período', 'Factor', 
                         'Horas serviço', 'Data início', 'Data fim', 'Nome Docente', 'Agrupamento']] 

        for index, row in testes.iterrows():
            Periodo = row['Período']
            codDisci = row['Cód. disciplina']
            disciplina = row['Disciplina']
            instituic = row['Inst. discip.']
            instituto = row['Inst. disciplina']
            departamento = row['Depart. disciplina']
            turma = row['Turma']
            codCurso = row['Código curso']
            curso = row['Curso']
            codDocente = row['Cód. Docente']
            docente = row['Docente']
            funcDocente = row['Função docente']
            instDocente = row['Inst. docente']
            departDocente = row['Depart. docente']
            horasSem = row['Horas semanais']
            horasPeri = row['Horas período']
            factor = row['Factor']
            horasServ = row['Horas serviço']
            Datainicial = row['Data início']
            DataFim = row['Data fim']
            Nome = row['Nome Docente']
            Agrupamento = row['Agrupamento']
            novAUC = DSD(Periodo = Periodo, codDisci =  codDisci, disciplina = disciplina, instituic = instituic, instituto = instituto, departamento = departamento,
                         turma = turma, codCurso = codCurso, curso = curso, codDocente = codDocente, docente = docente, funcDocente = funcDocente, instDocente = instDocente,
                         horasSem = horasSem, horasPeri = horasPeri, factor = factor, Datainicial = Datainicial, DataFim = DataFim, Nome = Nome, Agrupamento = Agrupamento)
            novAUC.save()
        success = 'Dados do DSD importados com sucesso'
        return render(request=request, template_name='main/upload_DSD.html', context={'success': success})
    return render(request=request, template_name='main/upload_DSD.html')



def uploadDocente(request):
    if request.method == 'POST':
        if not request.FILES:
            error = 'Selecione um arquivo para fazer o upload'
            return render(request=request, template_name='main/Upload_Docentes.html', context={'error': error})
        if not request.FILES['file'].name.endswith('.xls'):
            error = 'O arquivo deve estar no formato .xls'
            return render(request=request, template_name='main/Upload_Docentes.html', context={'error': error})
        excel_file = request.FILES['file']
        excel_data = pd.ExcelFile(excel_file)
        sheetx = pd.read_excel(excel_data, sheet_name=0)
        testes = sheetx[['Código', 'Docente', 'Ativo', 'Nome', 'Indivíduo', 'Data de nascimento', 'Sexo', 'Tipo de identificação', 'Identificação', 'Data de emissão da identificação', 'Nacionalidade', 'Arquivo', 'Data de validade da identificação', 'NIF', 'País fiscal', 'Digito verificação', '&nbsp;']] 

        for index, row in testes.iterrows():
            codigo = row['Código']
            docente = row['Docente']
            ativo = row['Ativo']
            nome = row['Nome']
            individuo = row['Indivíduo']
            data_nascimento = row['Data de nascimento']
            sexo = row['Sexo']
            tipo_identificacao = row['Tipo de identificação']
            identificacao = row['Identificação']
            data_emissao_identificacao = row['Data de emissão da identificação']
            nacionalidade = row['Nacionalidade']
            arquivo = row['Arquivo']
            data_validade_identificacao = row['Data de validade da identificação']
            nif = row['NIF']
            pais_fiscal = row['País fiscal']
            digito_verificacao = row['Digito verificação']
            nbsp = row['&nbsp;']

            novoDocente = Docente(codigo=codigo, docente=docente, ativo=ativo, nome=nome, individuo=individuo, data_nascimento=data_nascimento, sexo=sexo, tipo_identificacao=tipo_identificacao, identificacao=identificacao, data_emissao_identificacao=data_emissao_identificacao, nacionalidade=nacionalidade, arquivo=arquivo, data_validade_identificacao=data_validade_identificacao, nif=nif, pais_fiscal=pais_fiscal, digito_verificacao=digito_verificacao, nbsp=nbsp)
            novoDocente.save()
            succes = 'Importado para a base de dados'
        return render(request=request, template_name='main/Upload_Docentes.html', context={"succes": succes})
    return render(request=request, template_name='main/Upload_Docentes.html')


### Estatisticas ###
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



### Coisa na minha opiniao nao são necessarias ###
def meus(request):
   pedidosoutro = PedidosOutros.objects.all()
   return render(request, template_name="main/bulma_table.html",context={"Pedido":pedidosoutro})


def deletOutros(request,pk):
   PedidosOut = PedidosOutros.objects.get(id=pk)
   if request.method == "POST":
      PedidosOut.delete()
      return redirect('/meus')
   return render(request, template_name="main/delete.html",context={'item': PedidosOut})


def tableHorario2(request, pk):
   try:
        pedido = Pedido.objects.get(id=pk)
        pedidoshorario = PedidoHorario.objects.filter(pedido=pedido)
   except Pedido.DoesNotExist:
        return HttpResponseNotFound('Pedido não encontrado')
   return render(request, template_name="main/tableHorario2.html",context={"Pedido":pedidoshorario})


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


def deletHorario2(request,pk):
   PedidosHor = PedidoHorario.objects.get(id=pk)
   if request.method == "POST":
      PedidosHor.delete()
      return redirect(reverse('main:tableHorario2', kwargs={'pk': PedidosHor.pedido.id}))
   return render(request, template_name="main/deleteH2.html",context={'item': PedidosHor})


def tableUC(request):
   pedidosUC = PedidoUC.objects.all()
   return render(request, template_name="main/tableUC.html",context={"Pedido":pedidosUC})


def deletUC(request,pk):
   PedidosUC = PedidoUC.objects.get(id=pk)
   if request.method == "POST":
      PedidosUC.delete()
      return redirect('/tableUC')
   return render(request, template_name="main/deleteUC.html",context={'item': PedidosUC})


def tableSala(request):
   pedidosSala = PedidoSala.objects.all()
   return render(request, template_name="main/tableSala.html",context={"Pedido":pedidosSala})


def deletSala(request,pk):
   PedidosSala = PedidoSala.objects.get(id=pk)
   if request.method == "POST":
      PedidosSala.delete()
      return redirect('/tableSala')
   return render(request, template_name="main/deleteS.html",context={'item': PedidosSala})
