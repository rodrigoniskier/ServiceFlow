from django.urls import path
from .views import ServiceFlowLoginView,create_request,dashboard,export_csv,export_excel,import_history_view,logout_view
urlpatterns=[path("login/",ServiceFlowLoginView.as_view(),name="login"),path("logout/",logout_view,name="logout"),path("",dashboard,name="dashboard"),path("requests/new/",create_request,name="create_request"),path("export/csv/",export_csv,name="export_csv"),path("export/xlsx/",export_excel,name="export_excel"),path("import/",import_history_view,name="import_history")]
