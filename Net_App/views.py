from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Device, Log, Inventory
from .forms import UserForm
from django.contrib.auth import authenticate
import hashlib
from tablib import Dataset
from django.http import HttpResponse
from .resources import DeviceResource, InventoryResource
from Net_App.utils.nornir_conn import nornir_conn_cfg, nornir_conn_show, nornir_conn_backupcfg
from Net_App.utils.nornir_inventory import nornir_inventory

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def index(request):
    all_device = Device.objects.all()
    cisco_device = Device.objects.filter(vendor="Cisco")
    forti_device = Device.objects.filter(vendor='Fortinet')
    all_router = Device.objects.filter(type='Router')
    all_switch = Device.objects.filter(type='Switch')
    all_firewall = Device.objects.filter(type='Firewall')
    last_10_event = Log.objects.all().order_by('-id')[:10]
    context = {'all_device': len(all_device),
               'cisco_device': len(cisco_device),
               'forti_device': len(forti_device),
               'all_router': len(all_router),
               'all_switch': len(all_switch),
               'all_firewall': len(all_firewall),
               'last_10_event': last_10_event
               }
    return render(request, 'index.html', context)

def login(request):
    if request.session.get('is_login',None):
        return redirect('index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('index')
            else:
                message = "登录失败"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("index")

def host_mgmt(request):
    if request.method == 'GET':
        all_device = Device.objects.all()
        context = {'all_device': all_device}
        return render(request, 'host_mgmt.html', context)

    elif request.method == 'POST':
        device_id_list = request.POST.getlist('seleted_device_id')
        request.session['seleted_device_id'] = device_id_list
        if 'delHost' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).delete()
            return redirect('host_mgmt')
        if 'exportHost' in request.POST:
            device_resource = DeviceResource()
            dataset = device_resource.export()
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_host.xls"'
            return response
        if 'updateHost' in request.POST:
            return redirect('host_update')
        if 'importHost' in request.POST:
            device_resource = DeviceResource()
            dataset = Dataset()
            new_devices = request.FILES['imported_file']
            imported_data = dataset.load(new_devices.read())
            result = device_resource.import_data(dataset, dry_run=True)  # Test the data import
            if not result.has_errors():
                device_resource.import_data(dataset, dry_run=False)  # Actually import now
                return redirect('host_mgmt')
            else:
                return HttpResponse(f'导入失败，暂时没有进行报错处理，大概率是导入了已经存在的主机:{result.totals}')
    return redirect('host_mgmt')

def host_add(request):
    if request.method == 'POST':
        ip_address = request.POST['ip_address']
        hostname = request.POST['hostname']
        username = request.POST['username']
        password = request.POST['password']
        enable_password = request.POST['enable_password']
        ssh_port = request.POST['ssh_port']
        vendor = request.POST['vendor']
        type = request.POST['type']
        host_obj = Device.objects.filter(ip_address=ip_address).first()
        if not host_obj:
            Device.objects.create(ip_address=ip_address, hostname=hostname,username=username, password=password, enable_password=enable_password, ssh_port=ssh_port,
                              vendor=vendor, type=type)
            return redirect('host_mgmt')
        return HttpResponse('该主机已存在')
    return render(request, 'host_add.html')

def host_update(request):
    device_id_list = request.session['seleted_device_id']
    selected_ip_list = []
    username = request.POST.get('username')
    password = request.POST.get('password')
    enable_password = request.POST.get('enable_password')
    ssh_port = request.POST.get('ssh_port')
    vendor = request.POST.get('vendor')
    type = request.POST.get('type')

    for x in device_id_list:
        dev = get_object_or_404(Device, pk=x)
        ip_address = dev.ip_address
        selected_ip_list.append(ip_address)

    if request.method == 'POST':
        if 'updateUsername' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(username=username)
            return redirect('host_mgmt')
        elif 'updatePassword' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(password=password)
            return redirect('host_mgmt')
        elif 'updateEnable_password' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(enable_password=enable_password)
            return redirect('host_mgmt')
        elif 'updateSsh_port' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(ssh_port=ssh_port)
            return redirect('host_mgmt')
        elif 'updateVendor' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(vendor=vendor)
            return redirect('host_mgmt')
        elif 'updateType' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(type=type)
            return redirect('host_mgmt')
        else:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(username=username, password=password, enable_password=enable_password, ssh_port=ssh_port,
                              vendor=vendor, type=type)
            return redirect('host_mgmt')
    return render(request, 'host_update.html', locals())

def host_edit(request):
    device_id = request.GET.get('device_id')
    device = Device.objects.filter(id=device_id).first()
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        hostname = request.POST.get('hostname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        enable_password = request.POST.get('enable_password')
        ssh_port = request.POST.get('ssh_port')
        vendor = request.POST.get('vendor')
        type = request.POST.get('type')
        Device.objects.filter(id=device_id).update(ip_address=ip_address,hostname=hostname, username=username, password=password, enable_password=enable_password, ssh_port=ssh_port,
                              vendor=vendor, type=type)
        return redirect('host_mgmt')
    return render(request, 'host_edit.html', locals())

def cfg_host(request):
    if request.method == 'GET':
        all_device = Device.objects.all()
        context = {'all_device': all_device,
                   'mode': '设备配置'
                   }
        return render(request, 'cfg_host.html', context)

    elif request.method == 'POST':
        selected_device_id = request.POST.getlist('device')
        cmds = request.POST['command']
        devs = []

        for x in selected_device_id:
            dev = get_object_or_404(Device, pk=x)
            if (dev.vendor == 'Cisco' and dev.type == 'Router') or (dev.vendor == 'Cisco' and dev.type == 'Switch'):
                device_type = 'cisco_ios'
            elif dev.vendor == 'Cisco' and dev.type == 'Firewall':
                device_type = 'cisco_asa'
            elif dev.vendor == 'Fortinet' :
                device_type = 'fortinet'
            devs.append(
                {
                    'name': dev.hostname,
                    'ip': dev.ip_address,
                    'username': dev.username,
                    'password': dev.password,
                    'port': dev.ssh_port,
                    'platform': device_type,
                    'secret':dev.enable_password
                }
            )

        if 'cfgHost' in request.POST:
            # return HttpResponse('zzzz is coming')
            outputs = nornir_conn_cfg(devs, cmds=cmds.splitlines())
#            return render(request, 'cfg_verify.html', {'outputs': outputs})
        elif 'showHost' in request.POST:
            outputs = nornir_conn_show(devs, cmds=cmds.splitlines())
#            return render(request, 'cfg_verify.html', {'outputs': outputs})
        elif 'backupHost' in request.POST:
            if device_type == 'cisco_ios':
                cmd = 'sh run'
            elif device_type == 'cisco_asa':
                cmd = 'sh run'
            elif device_type == 'fortinet':
                cmd = 'show full-configuration'
            outputs = nornir_conn_backupcfg(devs, cmd)
#            return render(request, 'cfg_verify.html', {'outputs': outputs})
        elif 'inventoryHost' in request.POST:
            if device_type == 'cisco_ios':
                cmd = 'sh ver'
            elif device_type == 'cisco_asa':
                cmd = 'sh ver'
            elif device_type == 'fortinet':
                cmd = 'get system status'
            outputs = nornir_inventory(devs,cmd)
    return render(request, 'cfg_verify.html', {'outputs': outputs})

def cfg_verify(request):
    return render(request, 'cfg_verify.html', context)

def cfg_log(request):
    logs = Log.objects.all()
    context = {'logs': logs}
    return render(request, 'cfg_log.html', context)

def show_version(request):
    if request.method == 'GET':
        all_device = Inventory.objects.all()
        context = {'all_device': all_device}
        return render(request, 'show_version.html', context)
    elif request.method == 'POST':
        info_resource = InventoryResource()
        dataset = info_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="exported_host_info.xls"'
        return response
