import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Web.settings')

import django
django.setup()

from nornir_netmiko.tasks import netmiko_send_command
from Net_App.models import Device, Interface

show_intf_cmd_maping = {
    'cisco_ios':'show interface',
    'cisco_asa':'show interface',
}

def update_intfs_task(task, save=True):
    device_type = task.host.platform
    device_obj = Device.objects.get(ip_address=task.host.hostname)

    cmd = show_intf_cmd_maping.get(device_type)
    if not cmd:
        raise Exception('暂不支持该设备')

    intfs = task.run(netmiko_send_command, command_string=cmd, use_textfsm=True).result
    if save:
        for intf in intfs:
            try:
                obj,created = Interface.objects.update_or_create(
                    name=intf['interface'],device=device_obj,
                    defaults=dict(name=intf['interface'],
                                  desc=intf['description'],
                                  device=device_obj),
                                )
                print(obj,created)
            except Exception as e:
                print('端口{}保存失败，错误信息：{}'.format(intf,str(e)))
    return intfs
    print(device_obj)

if __name__ == '__main__':
    update_intfs_task()
