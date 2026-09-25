import csv
from datetime import date
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count,Q
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.views.decorators.http import require_POST
from .forms import ServiceRequestForm
from .models import Category,ServiceRequest
from .services import export_xlsx,import_history

class ServiceFlowLoginView(LoginView):
    template_name="login.html"
    redirect_authenticated_user=True

def filtered_requests(request):
    qs=ServiceRequest.objects.select_related("category","subcategory","created_by")
    q=(request.GET.get("q") or "").strip()
    if q: qs=qs.filter(Q(requester_name__icontains=q)|Q(requester_reference__icontains=q)|Q(subject__icontains=q)|Q(resolution__icontains=q))
    for key,field in [("status","status"),("channel","channel"),("category","category_id"),("handled_by","handled_by")]:
        value=(request.GET.get(key) or "").strip()
        if value: qs=qs.filter(**{field:value})
    start=request.GET.get("start"); end=request.GET.get("end")
    if start: qs=qs.filter(request_date__gte=start)
    if end: qs=qs.filter(request_date__lte=end)
    return qs

@login_required
def dashboard(request):
    qs=filtered_requests(request)
    totals={"total":qs.count(),"open":qs.exclude(status__in=["RESOLVED","CANCELLED"]).count(),"resolved":qs.filter(status="RESOLVED").count()}
    by_category=list(qs.values("category__name").annotate(total=Count("id")).order_by("-total")[:8])
    return render(request,"dashboard.html",{"requests":qs[:100],"totals":totals,"by_category":by_category,"categories":Category.objects.filter(active=True)})

@login_required
def create_request(request):
    form=ServiceRequestForm(request.POST or None,initial={"request_date":date.today(),"handled_by":request.user.get_full_name() or request.user.username})
    if request.method=="POST" and form.is_valid():
        obj=form.save(commit=False); obj.created_by=request.user; obj.save(); messages.success(request,"Request recorded."); return redirect("dashboard")
    return render(request,"request_form.html",{"form":form})

@login_required
def export_csv(request):
    qs=filtered_requests(request)
    response=HttpResponse(content_type="text/csv; charset=utf-8"); response["Content-Disposition"]='attachment; filename="serviceflow.csv"'
    w=csv.writer(response); w.writerow(["date","reference","requester","category","subject","resolution","channel","status","handled_by"])
    for r in qs.select_related("category"): w.writerow([r.request_date,r.requester_reference,r.requester_name,r.category.name,r.subject,r.resolution,r.get_channel_display(),r.get_status_display(),r.handled_by])
    return response

@login_required
def export_excel(request):
    out=export_xlsx(filtered_requests(request))
    response=HttpResponse(out.getvalue(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"]='attachment; filename="serviceflow.xlsx"'; return response

@login_required
def import_history_view(request):
    result=None
    if request.method=="POST":
        file=request.FILES.get("file"); dry_run=request.POST.get("dry_run")=="1"
        if not file or not file.name.lower().endswith(".xlsx"): messages.error(request,"Upload an .xlsx file.")
        else:
            try: result=import_history(file,request.user,dry_run=dry_run)
            except Exception: messages.error(request,"Import failed. Verify the spreadsheet format.")
    return render(request,"import_history.html",{"result":result})

@require_POST
@login_required
def logout_view(request):
    logout(request); return redirect("login")
