from datetime import date,timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from core.models import Category,ServiceRequest

class Command(BaseCommand):
    help="Create synthetic demo data"
    def handle(self,*args,**kwargs):
        admin,_=User.objects.get_or_create(username="admin",defaults={"is_staff":True,"is_superuser":True,"email":"admin@example.com"})
        admin.set_password("Demo-Admin-12345"); admin.save()
        agent,_=User.objects.get_or_create(username="agent.demo",defaults={"first_name":"Demo","last_name":"Agent","email":"agent@example.com"})
        agent.set_password("Demo-Agent-12345"); agent.save()
        cats=[]
        for name in ["Documents","Access & systems","Scheduling","Student support","Infrastructure"]:
            cats.append(Category.objects.get_or_create(name=name)[0])
        if not ServiceRequest.objects.exists():
            for i in range(12):
                ServiceRequest.objects.create(request_date=date.today()-timedelta(days=i*3),requester_type="Client",requester_reference=f"DEMO-{1000+i}",requester_name=f"Demo Requester {i+1}",category=cats[i%len(cats)],subject=f"Synthetic service request {i+1}",resolution="Resolved with demo guidance." if i%3==0 else "",channel=["EMAIL","IN_PERSON","CHAT"][i%3],status="RESOLVED" if i%3==0 else "OPEN",handled_by="Demo Agent",created_by=agent)
        self.stdout.write(self.style.SUCCESS("Synthetic demo data ready."))
