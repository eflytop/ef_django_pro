from import_export import resources
from .models import Device, Inventory
class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory