# 该脚本是将Web表弟里面的主机信息转换成nornir可识别的hosts.yaml文件
# 通过pip install nornir-table-inventory安装对应模块

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Web.settings')

import django
django.setup()

from nornir import InitNornir
from Net_App.models import Device

def get_nornir_obj():
    devs = Device.objects.all()
    devs_data = []
    for dev in devs:
        if (dev.vendor == 'Cisco' and dev.type == 'Router') or (dev.verdor == 'Cisco' and dev.type == 'Switch'):
            device_type = 'cisco_ios'
        elif dev.vendor == 'Cisco' and dev.type == 'Firewall':
            device_type = 'cisco_asa'
        devs_data.append(
            {
                'name': dev.hostname,
                'hostname': dev.ip_address,
                'platform': device_type,
                'port': dev.ssh_port,
                'username': dev.username,
                'password': dev.password,
                'netmiko_secret': dev.enable_password,
            }
        )
        #与nornir host.yaml文件参数对应
    runner = {
        'plugin':'threaded',
        'options':{
            'num_workers':5  #运行并行数
        },
    }
    inventory = {
        'plugin':'FlatDataInventory',
        "options":{
            'data':devs_data,
        },
    }

    nr = InitNornir(runner=runner,inventory=inventory)
    return nr
    # for n, h in nr.inventory.hosts.items():
    #     print(h.hostname)

if __name__ == '__main__':
    get_nornir_obj()

