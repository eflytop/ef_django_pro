import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Web.settings')

import django
django.setup()

from nornir_netmiko import netmiko_send_command
from Net_App.models import Device,Log
from Net_App.utils.nornir_parse_hosts import get_nornir_obj
from django.utils import timezone as datetime

devs = [{
    'name': '10.16.72.9',
    'ip': '10.16.72.9',
    'username': 'pixadmin',
    'password': 'fox+=1688',
    'port': '22',
    'platform': 'fortinet',
    'secret': ''
}, ]

def nornir_ios_show_version(devs):
    nr = get_nornir_obj(devs)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    result = nr.run(netmiko_send_command, command_string='show version', use_textfsm=True)

    for i in result.keys():
        if timeout_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
        elif authen_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
        elif other_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
        else:
            log = Log(target=i, action='Inventory', status='Success', time=datetime.now(),
                      messages='更新成功')
            log.save()
            Device.objects.filter(ip_address=i).update(sn=result[i].result[0]['serial'][0],
                                                       hostname=result[i].result[0]['hostname'],
                                                       model=result[i].result[0]['hardware'][0],
                                                       uptime=result[i].result[0]['uptime'],
                                                       image=result[i].result[0]['running_image'],
                                                       os_version=result[i].result[0]['version'])
            # print_result(results)
            # print(i)
            # print(result[i].result[0]['serial'][0])
            # print(result[i].result[0]['hostname'])
            # print(result[i].result[0]['uptime'])
            # print(result[i].result[0]['hardware'][0])
            # print(result[i].result[0]['running_image'])
            # print(result[i].result[0]['version'])
            # {'version': '16.12.4', 'rommon': '16.12(2r)', 'hostname': 'ISR4331-CQ-A21-29.13',
            #  'uptime': '38 weeks, 2 days, 8 hours, 25 minutes', 'uptime_years': '', 'uptime_weeks': '38',
            #  'uptime_days': '2', 'uptime_hours': '8', 'uptime_minutes': '25', 'reload_reason': 'PowerOn',
            #  'running_image': 'isr4300-universalk9.16.12.04.SPA.bin', 'hardware': ['ISR4331/K9'], 'serial': ['FDO2350M4CH'],
            #  'config_register': '0x2102', 'mac': [], 'restarted': ''}

def nornir_asa_show_version(devs):
    nr = get_nornir_obj(devs)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    result = nr.run(netmiko_send_command, command_string='show version', use_textfsm=True)

    for i in result.keys():
        if timeout_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
        elif authen_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
        elif other_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
        else:
            log = Log(target=i, action='Inventory', status='Success', time=datetime.now(),
                      messages='更新成功')
            log.save()
            Device.objects.filter(ip_address=i).update(sn=result[i].result[0]['serial'][0],
                                                       hostname=result[i].result[0]['hostname'],
                                                       model=result[i].result[0]['hardware'],
                                                       uptime=result[i].result[0]['uptime'],
                                                       image=result[i].result[0]['image'],
                                                       os_version=result[i].result[0]['version'])

def nornir_fg_show_version(devs):
    nr = get_nornir_obj(devs)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    result = nr.run(netmiko_send_command, command_string='get system status', use_textfsm=True)

    for i in result.keys():
        if timeout_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
        elif authen_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
        elif other_errors in (result[i].result):
            log = Log(target=i, action='Inventory', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
        else:
            log = Log(target=i, action='Inventory', status='Success', time=datetime.now(),
                      messages='更新成功')
            log.save()
            Device.objects.filter(ip_address=i).update(sn=result[i].result[0]['serial_number'],
                                                       hostname=result[i].result[0]['hostname'],
                                                       model=result[i].result[0]['version'],
                                                       image=result[i].result[0]['version'],
                                                       os_version=result[i].result[0]['version'])
            # print(i)
            # print(result[i].result[0])
            # print(result[i].result[0]['serial_number'])
            # print(result[i].result[0]['hostname'])
            # print(result[i].result[0]['version'])
            # {'hostname': 'JDM-CUP-FG-100E-72_9', 'version': 'FortiGate-100E v6.2.5,build1142,200819 (GA)',
            #  'signature': '', 'virus_db': '1.00000(2018-04-09 18:07)', 'extended_db': '1.00000(2018-04-09 18:07)',
            #  'extreme_db': '', 'ips_db': '6.00741(2015-12-01 02:30)', 'ips_etdb': '0.00000(2001-01-01 00:00)',
            #  'app_db': '6.00741(2015-12-01 02:30)', 'industrial_db': '6.00741(2015-12-01 02:30)',
            #  'serial_number': 'FG100ETK20006953', 'ips_malicious_url_database': '2.00849(2020-12-05 14:37)',
            #  'botnet_db': '1.00000(2012-05-28 22:51)', 'bios_version': '05000008', 'system_part_number': 'P18827-04',
            #  'log_hard_disk': 'Not', 'private_encryption': '', 'operation_mode': 'NAT',
            #  'current_virtual_domain': 'root', 'max_number_of_virtual_domains': '10',
            #  'virtual_domains_status': '1 in NAT mode, 0 in TP mode', 'virtual_domain_configuration': 'disable',
            #  'fips_cc_mode': 'disable', 'current_ha_mode': 'standalone', 'cluster_uptime': '',
            #  'cluster_state_change_time': '', 'branch_point': '1142', 'release_version_information': 'GA',
            #  'fortios_x86_64': '', 'system_time': 'Mon Mar 14 00:13:35 2022'}

if __name__ == '__main__':

    nornir_fg_show_version(devs)