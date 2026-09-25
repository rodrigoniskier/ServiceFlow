from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model=ServiceRequest
        fields=["request_date","requester_type","requester_reference","requester_name","category","subcategory","subject","resolution","channel","status","notes","handled_by"]
        widgets={"request_date":forms.DateInput(attrs={"type":"date"}),"resolution":forms.Textarea(attrs={"rows":3}),"notes":forms.Textarea(attrs={"rows":2})}
