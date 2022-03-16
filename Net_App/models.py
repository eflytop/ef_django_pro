from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=255, verbose_name="设备IP", help_text="设备IP地址", unique=True)
    hostname = models.CharField(max_length=255, verbose_name="主机名", null=True, blank=True, help_text="设备主机名，选填")
    username = models.CharField(max_length=255, verbose_name="用户名", help_text="登录用户名")
    password = models.CharField(max_length=255, verbose_name="密码", help_text="登录密码")
    enable_password = models.CharField(max_length=255, verbose_name="enable密码",null=True, blank=True, help_text="enable密码，选填")
    ssh_port = models.IntegerField(default=22, verbose_name="端口号", help_text="SSH登录端口号，默认为22")

    VENDOR_CHOICES = (
        ('Cisco', '思科'),
        ('Fortinet', '飞塔'),
    )
    vendor = models.CharField(max_length=255, verbose_name="厂商", choices=VENDOR_CHOICES)

    TYPE_CHOICES = (
        ('Router', '路由器'),
        ('Switch', '交换机'),
        ('Firewall', '防火墙'),
    )
    type = models.CharField(max_length=255, verbose_name="类型", choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.id}:{self.ip_address}"

class Inventory(models.Model):
    sn = models.CharField(max_length=255, null=True, blank=True, verbose_name="序列号", unique=True)
    uptime = models.CharField(max_length=255, null=True, blank=True, verbose_name="运行时间")
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name="型号")
    os_version = models.CharField(max_length=255, null=True, blank=True, verbose_name="软件版本")
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name="系统镜像")
    device = models.ForeignKey('Device', verbose_name='设备', related_name='device_info', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sn', 'device')

    def __str__(self):
        return '{}_{}'.format(self.device, self.sn)

class Interface(models.Model):
    name = models.CharField(max_length=255, verbose_name="端口名")
    desc = models.CharField(max_length=255, verbose_name="端口描述")
    device = models.ForeignKey('Device', verbose_name='设备', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'device')

    def __str__(self):
        return '{}_{}'.format(self.device, self.name)


class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)
