from django.contrib import admin

from tools import models


@admin.register(models.IPLog)
class IPLogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DomainLog)
class DomainLogAdmin(admin.ModelAdmin):
    pass
