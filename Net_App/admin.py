from django.contrib import admin
from .models import Device, Log
from import_export.admin import ImportExportModelAdmin

@admin.register(Device)

class DeviceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ip_address', 'hostname', 'username', 'vendor', 'type')

@admin.register(Log)

class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'time', 'messages')