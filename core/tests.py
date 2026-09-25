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

from django.conf import settings
from django.core.management import call_command
from django.test import override_settings

@override_settings(PORTFOLIO_DEMO=True)
class PortfolioDemoTests(TestCase):
    def setUp(self):
        call_command("seed_demo",verbosity=0)
    def test_seed_is_idempotent_and_has_no_privileged_account(self):
        from django.contrib.auth.models import User
        before=User.objects.count()
        call_command("seed_demo",verbosity=0)
        self.assertEqual(User.objects.count(),before)
        self.assertFalse(User.objects.filter(is_staff=True).exists())
        self.assertFalse(User.objects.filter(is_superuser=True).exists())
    def test_demo_entry_and_admin_boundary(self):
        name=settings.DEMO_ACCOUNTS[0][0]
        self.assertEqual(self.client.post("/demo/enter/",{"account":name}).status_code,302)
        self.assertEqual(self.client.get("/").status_code,200)
        self.assertEqual(self.client.get("/admin/").status_code,403)
        self.assertEqual(self.client.post("/demo/enter/",{"account":"admin"}).status_code,404)
    def test_demo_login_requires_csrf(self):
        from django.test import Client
        client=Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/demo/enter/",{"account":settings.DEMO_ACCOUNTS[0][0]}).status_code,403)

    def test_malformed_filters_and_blocked_import(self):
        self.client.post("/demo/enter/",{"account":"agent.demo"})
        for path in ("/?category=invalid", "/?start=invalid"):
            self.assertEqual(self.client.get(path).status_code,200)
        self.assertEqual(self.client.get("/import/").status_code,403)
    def test_export_neutralizes_formula_input(self):
        from core.services import safe_cell
        self.assertEqual(safe_cell("=1+2"),"'=1+2")
