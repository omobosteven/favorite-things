from rest_framework import serializers
from core.models import AuditLog


class AuditLogSerializers(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = ('audit_log_id', 'log', 'created_at', 'user')
