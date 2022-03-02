from import_export import resources
from .models import Device
class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device