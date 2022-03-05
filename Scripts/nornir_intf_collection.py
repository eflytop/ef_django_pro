import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Web.settings')

import django
django.setup()

from nornir_utils.plugins.functions import print_result
from Scripts.nornir_parse_hosts import get_nornir_obj
from Scripts.nornir_intf_getter import update_intfs_task

def collect_intfs():
    nr = get_nornir_obj()
    result = nr.run(update_intfs_task)
    print_result(result)

if __name__ == '__main__':
    collect_intfs()

