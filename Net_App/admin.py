from django.contrib import admin
from .models import Device, Log, Interface, Inventory
from import_export.admin import ImportExportModelAdmin

# 使用Django的TabularInline, 可以解决这个问题, 在父表里对子表进行编辑:
class InventoryInline(admin.TabularInline):
    # Inventory 必须是models.py中的模型名称,大小写必须要匹配.这个模型为子表,以便可以被父表编辑
    model = Inventory
    # 默认显示条目的数量
    extra = 1

@admin.register(Device)

class DeviceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ip_address',  'username', 'vendor', 'type')
    search_fields = ('ip_address', 'username', 'vendor', 'type')  #搜索框及搜索字段
    list_filter = ['vendor','type'] #右侧边快速筛选
    inlines = [InventoryInline, ]  # Inline把ScoreInline关联进来,让父表管理配置页面能同时编辑子表.

@admin.register(Log)

class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'time', 'messages')
    search_fields = ('target',  'messages')
    ordering = ['time', '-target'] #排序

@admin.register(Inventory)

class Inventory(ImportExportModelAdmin):
    list_display = ('id', 'device', 'sn', 'model')
    list_filter = ['device']  # 右侧边快速筛选

@admin.register(Interface)

class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'name', 'desc')
    list_filter = ['device']  # 右侧边快速筛选


