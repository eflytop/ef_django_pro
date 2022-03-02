from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=255, help_text="设备IP地址",)
    hostname = models.CharField(max_length=255, null=True, blank=True, help_text="设备主机名，选填")
    username = models.CharField(max_length=255, help_text="登录用户名")
    password = models.CharField(max_length=255, help_text="登录密码")
    enable_password = models.CharField(max_length=255, null=True, blank=True, help_text="enable密码，选填")
    ssh_port = models.IntegerField(default=22, help_text="SSH登录端口号，默认为22")

    VENDOR_CHOICES = (
        ('Cisco', '思科'),
        ('Fortinet', '飞塔'),
    )
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)

    TYPE_CHOICES = (
        ('Router', '路由器'),
        ('Switch', '交换机'),
        ('Firewall', '防火墙'),
    )
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.id}. {self.ip_address}"

class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)
