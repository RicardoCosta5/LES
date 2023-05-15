from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth.forms import UserCreationForm
import pandas as pd
from datetime import datetime, date
from urllib.parse import urlencode
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import PedidoFilter
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import get_user


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

      # Verifica se a data escolhida é anterior ao dia de hoje
      if datetime.strptime(dia, '%Y-%m-%d').date() < date.today():
         error = 'A data escolhida é anterior ao dia de hoje!'
         return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
      
      if Pedido.objects.filter(assunto=assunto, dia=dia).exists():
            # Se já existir, retorne uma mensagem de erro
            error = 'Já existe um pedido com o mesmo assunto!'
            return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
      for hora_inicio, hora_fim in zip(hora_inicio_list, hora_fim_list):
         try:
            datetime.strptime(hora_inicio, '%H:%M:%S')
            datetime.strptime(hora_fim, '%H:%M:%S')
         except ValueError:
            error = 'Formato de hora inválido!'
            return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
        
      
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
         if PedidoHorario.objects.filter(uc=uc_list[i], dia=dia2[i],hora_inicio=hora_inicio_list[i],hora_fim=hora_fim_list[i],tarefa=tarefa[i]).exists():
            error = 'Pedido de Horário igual!'
            ultimo_pedido = Pedido.objects.last()
            ultimo_pedido.delete()
            return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
         if datetime.strptime(dia2[i], '%Y-%m-%d').date() < date.today():
            error = 'A data escolhida é anterior ao dia de hoje!'
            ultimo_pedido = Pedido.objects.last()
            ultimo_pedido.delete()
            return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
         hora_inicio_list[i] = datetime.strptime(hora_inicio, '%H:%M:%S')
         hora_fim_list[i] = datetime.strptime(hora_fim, '%H:%M:%S')
         if hora_inicio_list[i] >= hora_fim_list[i]:
            error = 'A hora de fim deve ser maior que a hora de início!'
            ultimo_pedido = Pedido.objects.last()
            ultimo_pedido.delete()
            return render(request, 'main/PedidoHorario.html', {"error": error, "nome": name,"UC": UC})
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

        new_Pedido = Pedido(assunto=assunto, desc=descricao, dia=data, tipo = "Outros")
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
   UC = UnidadesCurriculares.objects.all()
   if request.method == "POST":
      salaa= request.POST.getlist('salaa')
      uc = request.POST['unc']
      dia= request.POST['data']
      assunto = request.POST['assunto'] 
      hora_de_inicio = request.POST.getlist('hora_inicio')
      hora_de_fim= request.POST.getlist('hora_fim')
      desc = request.POST['desc']
      descri = request.POST.getlist('descri')

      new_Pedido = Pedido(assunto = assunto, desc = desc, dia = dia, tipo = "Sala")
      new_Pedido.save()

      for i in range(len(uc)):
         new_PedidoSala = PedidoSala(
            sal=salaa[i],
            hora_de_inicio=hora_de_inicio[i],
            hora_de_fim=hora_de_fim[i],
            descri=descri[i],
            uc = uc[i],
            pedido=new_Pedido
         )
         new_PedidoSala.save()
         
   return render(request, template_name="main/PedidoSala.html",context={"Sala": Salas, "Edificio": Edificios, "UC": UC})

### Update dos Pedidos ###
def updateHorario(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido_horario = PedidoHorario.objects.filter(pedido=pk).all()
    UC = UnidadesCurriculares.objects.all()
    if request.method == "POST":
        pedido.dia = request.POST['data']
        dias = pedido.dia
        pedido.assunto = request.POST['assunto']
        pedido.desc = request.POST['desc']

        if datetime.strptime(dias, '%Y-%m-%d').date() < date.today():
         error = 'A data escolhida é anterior ao dia de hoje!'
         return render(request, 'main/PedidoHorario2.html', {"error": error,"assunto": pedido.assunto,
        "desc": pedido.desc,
        "dia": pedido.dia,
        "pedido_horario":pedido_horario,
        "UC": UC,})
      
        if Pedido.objects.filter(Q(assunto=pedido.assunto, dia=pedido.dia) & ~Q(id=pk)).exists():
            # Se já existir, retorne uma mensagem de erro
            error = 'Já existe um pedido com o mesmo assunto!'
            return render(request, 'main/PedidoHorario2.html', {"error": error,"assunto": pedido.assunto,
        "desc": pedido.desc,
        "dia": pedido.dia,
        "pedido_horario":pedido_horario,
        "UC": UC,})
      
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
            
            try:
                  datetime.strptime(pedido_horario.hora_inicio, '%H:%M:%S')
                  datetime.strptime(pedido_horario.hora_fim, '%H:%M:%S')
            except ValueError:
                  error = 'Formato de hora inválido!'
                  return render(request, 'main/PedidoHorario2.html', {"error": error,"assunto": pedido.assunto,
            "desc": pedido.desc,
            "dia": pedido.dia,
            "pedido_horario":pedido_horario,
            "UC": UC,})
            pedido_horario.save()
        
        redirect_url = reverse('main:tablePedidos')
        params = urlencode({'success': 'Enviado para a base de dados'})
        redirect_url = f"{redirect_url}?{params}"
        return HttpResponseRedirect(redirect_url)
    return render(request, template_name="main/PedidoHorario2.html", context={
        "assunto": pedido.assunto,
        "desc": pedido.desc,
        "dia": pedido.dia,
        "pedido_horario":pedido_horario,
        "UC": UC,
    })


def UPDATEPeidosOUT(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido_outros = PedidosOutros.objects.filter(pedido=pk).all()
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
    pedido_Sala = Pedido.objects.get(id=pk)
    Salas = Sala.objects.all()
    if request.method == "POST":
      pedido_Sala.dia = request.POST['data']
      pedido_Sala.assunto = request.POST['assunto']
      pedido_Sala.desc = request.POST['desc']
      pedido_Sala.save()
  
      return redirect('main:tableSala')
    return render(request, template_name="main/PedidoSala.html", context={
        "assunto": pedido_Sala.assunto,
        "desc": pedido_Sala.desc,
        "dia": pedido_Sala.dia,     
    })  


### Apagar Pedidos ISTO SO JA APAGA TODOS OS TIPOS DO PEDIDO ###
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
   myFilter = PedidoFilter(request.GET,queryset=pedidoshorario)
   pedidoshorario = myFilter.qs
   paginator = Paginator(pedidoshorario, 10)  # Define a quantidade de itens por página
   page_number = request.GET.get('page')  # Obtém o número da página da solicitação
   page_obj = paginator.get_page(page_number)
   success = request.GET.get('success')
   

   if request.method == 'POST':
      pedido_id = request.POST.get('pedido_id') 
      pedido = Pedido.objects.get(id=pedido_id)
      
      if request.POST.get('desassociar'):
         pedido.Funcionario = None
         pedido.atribuido = "Não Atribuido"
         pedido.save()
         return redirect(f'{reverse("main:tablePedidos")}?page={page_obj.number}&success=Funcionario desassociado!')
      else:
         nome = request.POST.get('funcionari')
         funcionario = Funcionario.objects.get(nome=nome)
         pedido.Funcionario = funcionario
         pedido.atribuido = "Atribuido"
         pedido.save()
         return redirect(f'{reverse("main:tablePedidos")}?page={page_obj.number}&success=Funcionario Atribuido!')
      
      
  
   return render(request, template_name="main/tableHorario.html",context={"Pedido":page_obj, "item":pedidoshorarios, "funcio":funciona,'success': success, 'myFilter':myFilter})


### Tabela Pedidos veie###
def tablePedidos2(request,pk):
   try:
    pedido = Pedido.objects.get(id=pk)
    if PedidoHorario.objects.filter(pedido=pedido).exists():
        pedidoshorario = PedidoHorario.objects.filter(pedido=pedido)
        return render(request, template_name="main/tableHorario2.html", context={"outros": pedidoshorario,"pedido":pedido})
    elif PedidosOutros.objects.filter(pedido=pedido).exists():
        pedidosoutros = PedidosOutros.objects.filter(pedido=pedido)
        return render(request, template_name="main/tableHorario2.html", context={"Pedido": pedidosoutros,"pedido":pedido})
    elif PedidoSala.objects.filter(pedido=pedido).exists():
        pedidossala = PedidoSala.objects.filter(pedido=pedido)
        return render(request, template_name="main/tableHorario2.html", context={"Pedido": pedidossala,"pedido":pedido})
    elif PedidoUC.objects.filter(pedido=pedido).exists():
        pedidosuc = PedidoUC.objects.filter(pedido=pedido)
        return render(request, template_name="main/tableHorario2.html", context={"Pedido": pedidosuc, "pedido":pedido})
    
   except Pedido.DoesNotExist:
      return HttpResponseNotFound('Pedido não encontrado')
      
   pedidoshorario = PedidoHorario.objects.filter(pedido=pedido)
   return render(request, template_name="main/tableHorario2.html",context={"Pedido":pedidoshorario,"pedido":pedido})


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

def uploadSALAS(request):
    if request.method == 'POST':
        if not request.FILES:
            error = 'Selecione um arquivo para fazer o upload'
            return render(request=request, template_name='main/upload_SALAS.html', context={'error': error})
        if not request.FILES['file'].name.endswith('.xlsx'):
            error = 'O arquivo deve estar no formato .xlsx'
            return render(request=request, template_name='main/upload_SALAS.html', context={'error': error})
        excel_file = request.FILES['file']
        excel_data = pd.ExcelFile(excel_file)
        sheetx = pd.read_excel(excel_data, sheet_name=0)
        testes = sheetx[['Nome Instituição', 'Desc. Edifício', 'Desc. Sala', 'Des. Categoria', 'Id. tipo sala', 'Lotação presencial sala']] 

        for index, row in testes.iterrows():
            NomeInstituição = row['Nome Instituição']
            DescEdifício = row['Desc. Edifício']
            DescSala = row['Desc. Sala']
            DesCategoria = row['Des. Categoria']
            IdTipoSala = row['Id. tipo sala']
            LotaçãoPresencialSala = row['Lotação presencial sala']

            novAUC = Sala(NomeInstituição=NomeInstituição, DescEdifício=DescEdifício, DescSala=DescSala, DesCategoria=DesCategoria, IdTipoSala=IdTipoSala, LotaçãoPresencialSala=LotaçãoPresencialSala)
            novAUC.save()
        return redirect('main:Upload_Salas')
    return render(request=request, template_name='main/Upload_Salas.html')


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



#Login e Register
def login(request):
    ''' Fazer login na plataforma do dia aberto e gestão de acessos à plataforma '''
    if request.user.is_authenticated: 
        return redirect("main:home")   
    else:
        u=""
    msg=False
    error=""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=="" or password=="":
                msg=True
                error="Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                utilizador = Utilizador.objects.get(id=user.id)
                if utilizador.valido=="False": 
                    msg=True
                    error="O seu registo ainda não foi validado"
                elif utilizador.valido=="Rejeitado":
                    msg=True
                    error="O seu registo não é válido"
                else:
                    login(request, user)
                    return redirect('main:home')
            else:
                msg=True
                error="O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})


def escolher(request):
    ''' Escolher tipo de perfil para criar um utilizador '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "Funcionário").exists():
            u = "Funcionário"
        elif user.groups.filter(name = "Docente").exists():
            u = "Docente" 
        else:
            u=""     
    else:
        u=""
    utilizadores = ["Funcionário","Docente", "Administrador"]
    return render(request=request, template_name='main/escolher_perfil.html', context={"utilizadores": utilizadores,'u': u})


def register(request, id):
    ''' Criar um novo utilizador que poderá ter de ser validado dependendo do seu tipo '''
    if request.user.is_authenticated:
        user = get_user(request)
        if user.groups.filter(name="Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name="Docente").exists():
            u = "Docente"
        elif user.groups.filter(name="Funcionário").exists():
            u = "Funcionario"
        else:
            u = ""
    else:
        u = ""
    msg = False
    if request.method == "POST":
        tipo = id
        if tipo == 1:
            form = FuncionarioRegisterForm(request.POST)
            perfil = "Funcionario"
            my_group, _ = Group.objects.get_or_create(name='Funcionário')
        elif tipo == 2:
            form = DocenteRegisterForm(request.POST)
            perfil = "Docente"
            my_group, _ = Group.objects.get_or_create(name='Docente')
        elif tipo == 3:
            form = AdministradorRegisterForm(request.POST)
            perfil = "Administrador"
            my_group, _ = Group.objects.get_or_create(name='Administrador')
        else:
            return redirect("utilizadores:escolher-perfil")

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            user.groups.add(my_group)

            if tipo == 1:
                user.valido = True
                user.save()
                p = 1
            else:
                user.valido = False
                recipient_id = user.id
                user.save()
                p = 0
                views.enviar_notificacao_automatica(request, "validarRegistosPendentes", recipient_id)
            if request.user.is_authenticated:
                user = get_user(request)
                if user.groups.filter(name="Administrador").exists():
                    return redirect("main:concluir-registo", 2)
            else:
                return redirect("main:concluir-registo", p)
        else:
            msg = True
            tipo = id
            return render(request=request,
                          template_name="main/criar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u, 'registo': tipo, 'msg': msg})
    else:
        tipo = id
        if tipo == 1:
            form = FuncionarioRegisterForm()
            perfil = "Funcionário"
        elif tipo == 2:
            form = DocenteRegisterForm()
            perfil = "Docente"
        elif tipo == 3:
            form = AdministradorRegisterForm()
            perfil = "Administrador"
        else:
            return redirect("main:escolher-perfil")
    return render(request=request,
                  template_name="main/criar_utilizador.html",
                  context={"form": form, 'perfil': perfil, 'u': u, 'registo': tipo, 'msg': msg})


def concluir_registo(request,id):
    ''' Página que é mostrada ao utilizador quando faz um registo na plataforma '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Docente").exists():
            u = "Docente"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "Funcionário").exists():
            u = "Funcionário"
        else:
            u=""   
    else:
        u=""
    if id == 1:
        participante="True"
    elif id == 0:
        participante="False"
    elif id == 2:
        participante="Admin"   
    return render(request=request,
                  template_name="main/concluir_registo.html",
                  context={'participante': participante, 'u': u})
