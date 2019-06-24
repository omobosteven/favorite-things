from django.urls import reverse
from rest_framework import status
from .base import BaseViewTest


class AuditLogTest(BaseViewTest):

    def test_audit_log_list(self):
        """
        Ensure user gets audit logs
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('audit_log'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
