from nornir_netmiko import netmiko_send_command, netmiko_send_config , netmiko_save_config
from Net_App.models import Log
from django.utils import timezone as datetime
from Net_App.utils.nornir_parse_hosts import get_nornir_obj
import os
import time

def nornir_conn_savecfg(devs):
    nr = get_nornir_obj(devs)
    result = nr.run(netmiko_save_config)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    nr_results = []
    for i in result.keys():
        ip = nr.inventory.hosts[i].hostname
        if timeout_errors in (result[i].result):
            log = Log(target=ip, action='Savecfg', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'TCP connection to device failed..'
            })
        elif authen_errors in (result[i].result):
            log = Log(target=ip, action='Savecfg', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Authentication to device failed...'
            })
        elif other_errors in (result[i].result):
            log = Log(target=ip, action='Savecfg', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Other_errors to device failed...'
            })
        else:
            log = Log(target=ip, action='Savecfg', status='Success', time=datetime.now(),
                      messages=result[i].result)
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'running configuration is saved'
            })
    return nr_results

def nornir_conn_cfg(devs, cmds):
    nr = get_nornir_obj(devs)
    result = nr.run(netmiko_send_config, config_commands=cmds, enable=True)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    nr_results = []
    for i in result.keys():
        ip = nr.inventory.hosts[i].hostname
        if timeout_errors in (result[i].result):
            log = Log(target=ip, action='Config', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'TCP connection to device failed..'
            })
        elif authen_errors in (result[i].result):
            log = Log(target=ip, action='Config', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Authentication to device failed...'
            })
        elif other_errors in (result[i].result):
            log = Log(target=ip, action='Config', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Other_errors to device failed...'
            })
        else:
            log = Log(target=ip, action='Config', status='Success', time=datetime.now(),
                      messages=result[i].result)
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': result[i].result
            })
    return nr_results

def nornir_conn_show(devs, cmds):
    nr = get_nornir_obj(devs)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    nr_results = []
    for cmd in cmds:
        result = nr.run(netmiko_send_command, command_string=cmd, enable=True)
        for i in result.keys():
            ip = nr.inventory.hosts[i].hostname
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
    return nr_results

def nornir_conn_backupcfg(devs,cmd):
    nr = get_nornir_obj(devs)
    result = nr.run(netmiko_send_command, command_string=cmd, enable=True)
    timeout_errors = 'netmiko.ssh_exception.NetmikoTimeoutException'
    authen_errors = 'netmiko.ssh_exception.NetmikoAuthenticationException'
    other_errors = 'Traceback'
    cfg_path_date = time.strftime("%Y-%m-%d", time.localtime())
    file_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    cfg_path = f'Cfg_files/' + cfg_path_date
    verify_path = os.path.exists(cfg_path)
    nr_results = []

    if not verify_path:
        os.makedirs(cfg_path)

    for i in result.keys():
        ip = nr.inventory.hosts[i].hostname
        if timeout_errors in (result[i].result):
            log = Log(target=ip, action='Backup', status='Error', time=datetime.now(),
                      messages='TCP connection to device failed..')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'TCP connection to device failed..'
            })
        elif authen_errors in (result[i].result):
            log = Log(target=ip, action='Backup', status='Error', time=datetime.now(),
                      messages='Authentication to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Authentication to device failed...'
            })
        elif other_errors in (result[i].result):
            log = Log(target=ip, action='Backup', status='Error', time=datetime.now(),
                      messages='Other_errors to device failed...')
            log.save()
            nr_results.append({
                'ip': ip,
                'output_content': f'Other_errors to device failed...'
            })
        else:
            log = Log(target=ip, action='Backup', status='Success', time=datetime.now(),
                      messages='备份成功！')
            log.save()
            cfg_filename = f'{cfg_path}/{i}_{file_time}.txt'
            with open(cfg_filename, "w", encoding='utf-8') as cfg_out:
                cfg_out.write(result[i].result)
            nr_results.append({
                'ip': ip,
                'output_content': f'配置备份成功！'
            })
    return nr_results

if __name__ == '__main__':
    ...
