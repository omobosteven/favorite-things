from django.urls import path
from audit_log import views

urlpatterns = [
    path('', views.AuditLogList.as_view(), name='audit_log'),
]
