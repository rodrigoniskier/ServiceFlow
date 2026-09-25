from datetime import date,timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand,CommandError
from django.db import transaction
from core.models import Category,Subcategory,ServiceRequest

class Command(BaseCommand):
    help='Populate a dedicated demo database with 56 synthetic service requests.'
    @transaction.atomic
    def handle(self,*args,**kwargs):
        if not settings.PORTFOLIO_DEMO: raise CommandError('PORTFOLIO_DEMO=1 is required.')
        agent,_=User.objects.get_or_create(username='agent.demo',defaults={'first_name':'Mariana','last_name':'Costa','email':'mariana@example.invalid'})
        agent.is_staff=False;agent.is_superuser=False;agent.set_unusable_password();agent.save()
        categories=[('Documentos','Emissão','Solicitação de declaração de participação'),('Sistemas e acessos','Portal','Orientação para acesso ao portal'),('Agendamentos','Reunião','Agendamento de orientação individual'),('Atendimento acadêmico','Inscrição','Acompanhamento de inscrição em oficina'),('Infraestrutura','Equipamentos','Verificação de equipamento na sala de apoio'),('Comunicação','Comunicados','Atualização do informativo da equipe'),('Processos administrativos','Cadastro','Conferência de cadastro de participante')]
        names=['Lucas Almeida','Rafael Oliveira','Ana Martins','Camila Rocha','Felipe Souza','Juliana Freitas','Pedro Nunes','Clara Mendes','Gabriel Lima','Luiza Barros','Daniel Ribeiro','Helena Duarte']
        for i in range(56):
            title,sub,subject=categories[i%7]
            category,_=Category.objects.get_or_create(name=title)
            subcategory,_=Subcategory.objects.get_or_create(category=category,name=sub)
            status=['RESOLVED','OPEN','RESOLVED','IN_PROGRESS','RESOLVED','FORWARDED','RESOLVED','CANCELLED'][i%8]
            ServiceRequest.objects.get_or_create(requester_reference=f'SF-2026-{1001+i}',defaults={'request_date':date(2026,9,25)-timedelta(days=(i*3)%42),'requester_type':'Participante','requester_name':names[i%len(names)],'category':category,'subcategory':subcategory,'subject':subject,'resolution':'Orientação encaminhada e confirmação registrada.' if status=='RESOLVED' else '', 'channel':['EMAIL','CHAT','IN_PERSON','PHONE'][i%4],'status':status,'notes':'Registro fictício para demonstração.','handled_by':['Mariana Costa','Bruno Carvalho','Beatriz Andrade','Daniel Ribeiro'][i%4],'created_by':agent})
        self.stdout.write(self.style.SUCCESS('56 synthetic requests ready.'))
