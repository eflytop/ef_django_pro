from django.contrib import admin
from .models import Device, Log, Interface
from import_export.admin import ImportExportModelAdmin

@admin.register(Device)

class DeviceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ip_address', 'hostname', 'username', 'vendor', 'type')
    search_fields = ('ip_address', 'hostname', 'username', 'vendor', 'type')  #搜索框及搜索字段
    list_filter = ['vendor','type'] #右侧边快速筛选

@admin.register(Log)

class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'time', 'messages')
    search_fields = ('target',  'messages')
    ordering = ['time', '-target'] #排序

@admin.register(Interface)

class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'name', 'desc')
    list_filter = ['device']  # 右侧边快速筛选