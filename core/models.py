import hashlib
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=120,unique=True)
    active=models.BooleanField(default=True)
    class Meta: ordering=("name",)
    def __str__(self): return self.name

class Subcategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="subcategories")
    name=models.CharField(max_length=120)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=("category__name","name")
        constraints=[models.UniqueConstraint(fields=("category","name"),name="unique_subcategory")]
    def __str__(self): return f"{self.category} · {self.name}"

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        OPEN="OPEN","Aberto"
        IN_PROGRESS="IN_PROGRESS","Em andamento"
        FORWARDED="FORWARDED","Encaminhado"
        RESOLVED="RESOLVED","Resolvido"
        CANCELLED="CANCELLED","Cancelado"
    class Channel(models.TextChoices):
        IN_PERSON="IN_PERSON","Presencial"
        EMAIL="EMAIL","Email"
        PHONE="PHONE","Telefone"
        CHAT="CHAT","Chat"
        OTHER="OTHER","Outro"
    request_date=models.DateField()
    requester_type=models.CharField(max_length=80,blank=True)
    requester_reference=models.CharField(max_length=100,blank=True,db_index=True)
    requester_name=models.CharField(max_length=180)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name="requests")
    subcategory=models.ForeignKey(Subcategory,on_delete=models.PROTECT,related_name="requests",null=True,blank=True)
    subject=models.CharField(max_length=240)
    resolution=models.TextField(blank=True)
    channel=models.CharField(max_length=20,choices=Channel.choices,default=Channel.IN_PERSON)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    notes=models.TextField(blank=True)
    handled_by=models.CharField(max_length=160)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name="created_service_requests")
    import_key=models.CharField(max_length=64,unique=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=("-request_date","-id")
    def __str__(self): return f"{self.request_date} · {self.requester_name} · {self.subject}"
    @staticmethod
    def build_import_key(values):
        normalized="|".join(str(v or "").strip().lower() for v in values)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

class ImportBatch(models.Model):
    filename=models.CharField(max_length=255)
    dry_run=models.BooleanField(default=True)
    created_count=models.PositiveIntegerField(default=0)
    skipped_count=models.PositiveIntegerField(default=0)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
