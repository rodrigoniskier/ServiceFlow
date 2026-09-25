from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model=ServiceRequest
        fields=["request_date","requester_type","requester_reference","requester_name","category","subcategory","subject","resolution","channel","status","notes","handled_by"]
        labels={"request_date":"Data", "requester_type":"Tipo de solicitante", "requester_reference":"Referência", "requester_name":"Nome fictício do solicitante", "category":"Categoria", "subcategory":"Subcategoria", "subject":"Assunto", "resolution":"Resolução", "channel":"Canal", "status":"Status", "notes":"Observações", "handled_by":"Responsável"}
        widgets={"request_date":forms.DateInput(attrs={"type":"date"}),"resolution":forms.Textarea(attrs={"rows":3}),"notes":forms.Textarea(attrs={"rows":2})}

    def clean(self):
        data=super().clean()
        sub=data.get("subcategory")
        if sub and sub.category_id != getattr(data.get("category"),"id",None):
            self.add_error("subcategory","Escolha uma subcategoria vinculada à categoria selecionada.")
        return data
