from nornir_netmiko import netmiko_send_command
from Net_App.models import Device, Log, Inventory
from Net_App.utils.nornir_parse_hosts import get_nornir_obj
from django.utils import timezone as datetime

def nornir_inventory(devs,cmd):
    nr = get_nornir_obj(devs)
    result = nr.run(netmiko_send_command, command_string=cmd,enable=True, use_textfsm=True)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    nr_results = []

    for i in result.keys():
        ip = nr.inventory.hosts[i].hostname
        dev = Device.objects.get(ip_address=ip)
        device_type  = nr.inventory.hosts[i].platform
        if timeout_errors in (result[i].result):
            log = Log(target=ip, action='Show', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'TCP connection to device failed..'
            })
        elif authen_errors in (result[i].result):
            log = Log(target=ip, action='Show', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Authentication to device failed...'
            })
        elif other_errors in (result[i].result):
            log = Log(target=ip, action='Show', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Other_errors to device failed...'
            })
        else:
            log = Log(target=ip, action='Show', status='Success', time=datetime.now(),
                      messages=result[i].result)
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': result[i].result
            })

            if device_type == 'cisco_ios':
                Inventory.objects.update_or_create(device=dev,
                                                   defaults=dict(sn=result[i].result[0]['serial'][0],
                                                           model=result[i].result[0]['hardware'][0],
                                                           uptime=result[i].result[0]['uptime'],
                                                           image=result[i].result[0]['running_image'],
                                                           os_version=result[i].result[0]['version']))
                Device.objects.filter(ip_address=ip).update(hostname=result[i].result[0]['hostname'])
            elif device_type == 'cisco_asa':
                Inventory.objects.update_or_create(device=dev,
                                               defaults=dict(sn=result[i].result[0]['serial'][0],
                                                       model=result[i].result[0]['hardware'],
                                                       uptime=result[i].result[0]['uptime'],
                                                       image=result[i].result[0]['image'],
                                                       os_version=result[i].result[0]['version']))
                Device.objects.filter(ip_address=ip).update(hostname=result[i].result[0]['hostname'])
            elif device_type == 'fortinet':
                Inventory.objects.update_or_create(device=dev,
                                                   defaults=dict(sn=result[i].result[0]['serial_number'],
                                                           model=result[i].result[0]['version'],))
                Device.objects.filter(ip_address=ip).update(hostname=result[i].result[0]['hostname'],)
                # print(device_type)
                # print(i)
                # print(result[i].result[0])
                # print(result[i].result[0]['serial_number'])

    return nr_results



if __name__ == '__main__':

    devs = [{
        'name': 'R-29.6',
        'ip': '10.245.29.6',
        'username': 'sdddn',
        'password': 'shddddd',
        'port': '22',
        'platform': 'cisco_ios',
        'secret': ''
    },
        {
            'name': 'R-29.4',
            'ip': '10.245.29.4',
            'username': 'sdddn',
            'password': 'shihuddd310',
            'port': '22',
            'platform': 'cisco_ios',
            'secret': ''
        },
    ]

    cmd='show ver'

    nornir_inventory(devs, cmd)