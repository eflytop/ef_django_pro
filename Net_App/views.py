#from django.views.generic import UpdateView, DetailView
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Device, Log
from .forms import UserForm
from django.contrib.auth import authenticate
import paramiko
import time
from django.utils import timezone as datetime
#from datetime import datetime
import hashlib
from tablib import Dataset
from django.http import HttpResponse
from .resources import DeviceResource

'''
class DeviceUpdateView(UpdateView):
    model = Device
    fields = ['hostname','username','password','enable_password','ssh_port','vendor','type']
    template_name = 'host_edit.html'
    success_url = "/device_list"
'''

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def index(request):
    all_device = Device.objects.all()
    cisco_device = Device.objects.filter(vendor="cisco")
    forti_device = Device.objects.filter(vendor='fortinet')
    all_router = Device.objects.filter(type='router')
    all_switch = Device.objects.filter(type='switch')
    all_firewall = Device.objects.filter(type='firewall')
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

def device_list(request):
    if request.method == 'GET':
        all_device = Device.objects.all()
        context = {'all_device': all_device}
        return render(request, 'device_list.html', context)

    elif request.method == 'POST':
        device_id_list = request.POST.getlist('seleted_device_id')
        request.session['seleted_device_id'] = device_id_list
        if 'delHost' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).delete()
            return redirect('device_list')
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
                return redirect('device_list')
    return redirect('device_list')

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
            return redirect('device_list')
        return HttpResponse('该主机已存在')
    return render(request, 'host_add.html')

def host_update(request):
    # if request.method == 'GET':
    #     return HttpResponse('GET is coming')
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
            return redirect('device_list')
        elif 'updatePassword' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(password=password)
            return redirect('device_list')
        elif 'updateEnable_password' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(enable_password=enable_password)
            return redirect('device_list')
        elif 'updateSsh_port' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(ssh_port=ssh_port)
            return redirect('device_list')
        elif 'updateVendor' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(vendor=vendor)
            return redirect('device_list')
        elif 'updateType' in request.POST:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(type=type)
            return redirect('device_list')
        else:
            for device_id in device_id_list:
                Device.objects.filter(id=device_id).update(username=username, password=password, enable_password=enable_password, ssh_port=ssh_port,
                              vendor=vendor, type=type)
            return redirect('device_list')
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
        Device.objects.filter(id=device_id).update(ip_address=ip_address, hostname=hostname,username=username, password=password, enable_password=enable_password, ssh_port=ssh_port,
                              vendor=vendor, type=type)
        return redirect('device_list')
    return render(request, 'host_edit.html', locals())

def cfg_host(request):
    if request.method == 'GET':
        device_list = Device.objects.all()
        context = {'device_list': device_list,
                   'mode': '设备配置'
                   }
        return render(request, 'cfg_host.html', context)

    elif request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')
        command = request.POST['command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password, look_for_keys=False)
                conn = ssh_client.invoke_shell()
                result.append(f'{dev.ip_address} 上的运行结果：')
                for cmd in command:
                    conn.send(cmd + '\n')
                    time.sleep(1)
                    output = conn.recv(65535).decode('ascii')
                    result.append(output)
                log = Log(target=dev.ip_address, action='Configure', status='Success', time=datetime.now(), messages='No Error')
                log.save()

            except Exception as e:
                result.append(f'{dev.ip_address} 配置失败，请查看日志!')
                log = Log(target=dev.ip_address, action='Configure', status='Error', time=datetime.now(), messages=e)
                log.save()

        result = '\n'.join(result)
        return render(request, 'cfg_verify.html', {'result': result})

def cfg_verify(request):
    return render(request, 'cfg_verify.html', context)

def cfg_backup(request):
    if request.method == 'GET':
        device_list = Device.objects.all()
        context = {'device_list': device_list}
        return render(request, 'cfg_backup.html', context)

    elif request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password,
                                   look_for_keys=False)
                if dev.vendor.lower() == 'cisco':
                    if dev.type.lower() == 'router':
                        conn = ssh_client.invoke_shell()
                        conn.send('terminal length 0\n')
                        conn.send('show run\n')
                        time.sleep(2)
                        output = conn.recv(65535).decode('ascii')
                        now = datetime.now()
                        date = f'{now.month}_{now.day}_{now.year}'
                        f = open(f'C:\\configuration_backup\\{dev.ip_address}_{date}.txt', 'w+')
                        f.write(output)
                        result.append(f'{dev.ip_address} 配置备份成功!')
                    elif dev.type.lower() == 'switch':
                        conn = ssh_client.invoke_shell()
                        conn.send('terminal length 0\n')
                        conn.send('show run\n')
                        time.sleep(2)
                        output = conn.recv(65535).decode('ascii')
                        now = datetime.now()
                        date = f'{now.month}_{now.day}_{now.year}'
                        f = open(f'C:\\configuration_backup\\{dev.ip_address}_{date}.txt', 'w+')
                        f.write(output)
                        result.append(f'{dev.ip_address} 配置备份成功!')
                    elif dev.type.lower() == 'firewall':
                        conn = ssh_client.invoke_shell()
                        conn.send('enable\n')
                        conn.send(f'{dev.enable_password}\n')
                        conn.send('terminal pager 0\n')
                        conn.send('show run\n')
                        time.sleep(10)
                        output = conn.recv(65535).decode('ascii')
                        now = datetime.now()
                        date = f'{now.month}_{now.day}_{now.year}'
                        f = open(f'C:\\configuration_backup\\{dev.ip_address}_{date}.txt', 'w+')
                        f.write(output)
                        result.append(f'{dev.ip_address} 配置备份成功!')
                elif dev.vendor.lower() == 'fortinet':
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal length 0\n')
                    conn.send('show run\n')
                    time.sleep(2)
                    output = conn.recv(65535).decode('ascii')
                    now = datetime.now()
                    date = f'{now.month}_{now.day}_{now.year}'
                    f = open(f'C:\\configuration_backup\\{dev.ip_address}_{date}.txt', 'w+')
                    f.write(output)
                    result.append(f'{dev.ip_address} 配置备份成功!')
                log = Log(target=dev.ip_address, action='CFG Backup', status='Success', time=datetime.now(),
                          messages='No Error')
                log.save()

            except Exception as e:
                log = Log(target=dev.ip_address, action='CFG Backup', status='Error', time=datetime.now(),
                          messages=e)
                log.save()
                result.append(f'{dev.ip_address} 配置备份失败，请查看日志!')

        result = '\n'.join(result)
        return render(request, 'cfg_verify.html', {'result': result})


def cfg_log(request):
    logs = Log.objects.all()
    context = {'logs': logs}
    return render(request, 'cfg_log.html', context)



# CBV
'''
class Index(View):
    def get(self, request):
        return render(request, 'index.html')
    def post(self, request):
        return HttpResponse('Welcome to CBV EFLab via POST')

class Login(View):
    def get(self, request):
        switches = SwitchesModel.objects.all()
        return render(request, "login.html", {'login_info':switches})
    def post(self, request):
        ip = request.POST['ip']
        username = request.POST['username']
        password = request.POST['password']
        SwitchesModel.objects.create(ip=ip,username=username,password=password,logintime=datetime.now(tz=timezone.utc))
        return redirect("/django_app/login")

class LoginDetail(View):
    def get(self, request, id):
        try:
            switch = SwitchesModel.objects.get(id=id)
            return render(request, "logindetail.html", {'switch_detail': switch})
        except SwitchesModel.DoesNotExist:
            return render(request, "404.html")
#            return HttpResponseNotFound()
'''



