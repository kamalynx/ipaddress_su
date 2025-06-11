from django.db import models
from uuid6 import uuid7


class BaseLogModel(models.Model):
    id = models.UUIDField(default=uuid7, editable=False, primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-timestamp',)
        indexes = [models.Index(fields=('timestamp',))]


class IPLog(BaseLogModel):
    address = models.GenericIPAddressField(
        verbose_name='IP адрес', unpack_ipv4=True
    )

    class Meta(BaseLogModel.Meta):
        verbose_name = 'Журнал IP'
        indexes = BaseLogModel.Meta.indexes + [
            models.Index(fields=('address',))
        ]

    def __str__(self):
        return str(self.address)


class DomainLog(BaseLogModel):
    class ViewType(models.TextChoices):
        WHOIS = 'whois', 'Whois'
        NSLOOKUP = 'nslookup', 'ns lookup'

    name = models.CharField(max_length=255, verbose_name='домен')
    view_type = models.CharField(
        max_length=16,
        choices=ViewType,
        verbose_name='тип представления',
        null=True,
    )

    class Meta(BaseLogModel.Meta):
        verbose_name = 'Журнал доменов'
        indexes = BaseLogModel.Meta.indexes + [
            models.Index(fields=('name', 'view_type'))
        ]

    def __str__(self):
        return str(self.name)
