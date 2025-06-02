from django.db import models
from uuid6 import uuid7


class IPLog(models.Model):
    id = models.UUIDField(default=uuid7, editable=False, primary_key=True)
    address = models.GenericIPAddressField(verbose_name='IP адрес', unpack_ipv4=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.address)

    class Meta:
        ordering = ['-updated_at', '-created_at']
        verbose_name = 'Журнал IP'
