from nornir_netmiko import netmiko_send_command, netmiko_send_config , netmiko_save_config
from Net_App.models import Log
from django.utils import timezone as datetime
from Net_App.utils.nornir_parse_hosts import get_nornir_obj
import os
import time

def nornir_inventory(devs):
    nr = get_nornir_obj(devs)
    result = nr.run(netmiko_send_command(), command_string=cmd, use_textfsm=True)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    nr_results = []
    for i in result.keys():
        if timeout_errors in (result[i].result):
            log = Log(target=i, action='Show', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
            nr_results.append({
                'ip': i,
                'output_content': f'TCP connection to device failed..'
            })
        elif authen_errors in (result[i].result):
            log = Log(target=i, action='Show', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
            nr_results.append({
                'ip': i,
                'output_content': f'Authentication to device failed...'
            })
        elif other_errors in (result[i].result):
            log = Log(target=i, action='Show', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
            nr_results.append({
                'ip': i,
                'output_content': f'Other_errors to device failed...'
            })
        else:
            log = Log(target=i, action='Show', status='Success', time=datetime.now(),
                      messages=result[i].result)
            log.save()
            nr_results.append({
                'ip': i,
                'output_content': result[i].result
            })
    return nr_results