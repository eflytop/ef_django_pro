import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Web.settings')

import django
django.setup()

from Net_App.models import Device, Interface
from Scripts.info_getters import ssh_dev_2_get_intfs

def collect_intfs():
    devs = Device.objects.all()
    for dev in devs:
        if (dev.vendor == 'Cisco' and dev.type == 'Router') or (dev.verdor == 'Cisco' and dev.type == 'Switch'):
            device_type = 'cisco_ios'
        elif dev.vendor == 'Cisco' and dev.type == 'Firewall':
            device_type = 'cisco_asa'
        dev_info = {
            'device_type': device_type,
            'host': dev.ip_address,
            'username': dev.username,
            'password': dev.password,
            'port': dev.ssh_port,
            'secret': dev.enable_password,
        }
        # print(dev_info)
        intfs = ssh_dev_2_get_intfs(**dev_info)
        for intf in intfs:
            try:
                # Interface(name=intf['interface'], desc=intf['description'], device=dev).save()
                obj,created = Interface.objects.update_or_create(
                    device=dev, name=intf['interface'],
                    defaults=dict(name=intf['interface'], desc=intf['description'], device=dev)
                    )
                print(obj,created)
                #print('端口：{}保存成功'.format(intf['interface']))
            except Exception as e:
                print('端口{}保存失败，错误信息：{}'.format(intf,str(e)))

if __name__ == '__main__':
    collect_intfs()

