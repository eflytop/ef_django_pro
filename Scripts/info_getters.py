from netmiko import Netmiko,ConnectHandler

show_intf_cmd_maping = {
    'cisco_ios':'show interface',
}

def ssh_dev_2_get_intfs(device_type, host, username, password, secret='', port=22):
    dev_info = {
        'device_type': device_type,
        'host': host,
        'username': username,
        'password': password,
        'port': 22,
        'secret': secret,
    }

    cmd = show_intf_cmd_maping.get(device_type)
    if not cmd:
        raise Exception('暂不支持该设备')

    with ConnectHandler(**dev_info) as net_conn:
        intfs = net_conn.send_command(cmd, use_textfsm=True)
        print(intfs)
        return intfs

if __name__ == '__main__':
    dev_info = {
        'device_type': 'cisco_ios',
        'host': '10.245.29.4',
        'username': 'shihua.chen',
        'password': 'shihua.chen0208',
        'port': 22,
        'secret': '',
    }
    ssh_dev_2_get_intfs(**dev_info)