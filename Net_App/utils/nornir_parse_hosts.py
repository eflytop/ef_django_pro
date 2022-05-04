from nornir import InitNornir

def get_nornir_obj(devs):
    devs_data = []

    for dev in devs:
        devs_data.append(
            {
                'name': dev['ip'],
                'hostname': dev['ip'],
                'platform': dev['platform'],
                'port': dev['port'],
                'username': dev['username'],
                'password': dev['password'],
                'netmiko_secret': dev['secret'],
                'netmiko_conn_timeout': 100,
            }
        )
    runner = {
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    }
    inventory = {
        "plugin": "FlatDataInventory",
        "options": {
            "data": devs_data,
        },
    }
    nr = InitNornir(runner=runner, inventory=inventory)
    return nr

if __name__ == '__main__':
    get_nornir_obj()