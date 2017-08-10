from api.models import Manager
from django.contrib import admin


class ManagersAdmin(admin.ModelAdmin):
    """ Admin layout for superadmin"""

    def get_queryset(self, request):
        qs = super(ManagersAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return None

""" Register Admin layouts into django"""
admin.site.register(Manager, ManagersAdmin, )
