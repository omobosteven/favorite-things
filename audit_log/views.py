from rest_framework import generics
from .serializers import AuditLogSerializers
from rest_framework.permissions import IsAuthenticated
from core.authentication import CookieAuthentication
from core.models import AuditLog


class AuditLogList(generics.ListAPIView):
    serializer_class = AuditLogSerializers
    authentication_classes = (CookieAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = AuditLog.objects.filter(user=self.request.user)
        return queryset
