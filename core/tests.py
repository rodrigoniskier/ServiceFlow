from io import BytesIO
from openpyxl import Workbook
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Category,ServiceRequest
from .services import import_history

class ServiceFlowTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user("agent",password="long-password-123")
        self.category=Category.objects.create(name="General")
    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code,302)
    def test_create_request_sets_authenticated_creator(self):
        self.client.force_login(self.user)
        response=self.client.post(reverse("create_request"),{"request_date":"2026-01-01","requester_type":"Client","requester_reference":"D-1","requester_name":"Demo","category":self.category.id,"subject":"Test","resolution":"","channel":"EMAIL","status":"OPEN","notes":"","handled_by":"Agent"})
        self.assertEqual(response.status_code,302)
        self.assertEqual(ServiceRequest.objects.get().created_by,self.user)
    def test_import_is_idempotent(self):
        wb=Workbook(); ws=wb.active; ws.append(["date","reference","name","subject","resolution","handled_by"]); ws.append(["2026-01-01","ABC","Demo","Question","Solved","Agent"])
        bio=BytesIO(); wb.save(bio); bio.seek(0); bio.name="history.xlsx"
        import_history(bio,self.user,dry_run=False)
        bio.seek(0); import_history(bio,self.user,dry_run=False)
        self.assertEqual(ServiceRequest.objects.count(),1)
