from django.db import models


class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    role_choices = ((1, '超级管理员'), (2, '站点管理员'))
    role = models.SmallIntegerField(verbose_name='角色', choices=role_choices, default=1)
    status_choices = ((1, '启用'), (2, '冻结'))
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.username


class SiteCategory(models.Model):
    icon = models.CharField(verbose_name='图标', max_length=64, null=True, blank=True)
    title = models.CharField(verbose_name='分类名称', max_length=64, unique=True)
    sort = models.IntegerField(verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title


class Site(models.Model):
    title = models.CharField(verbose_name='站点名称', max_length=64)
    url = models.URLField(verbose_name='站点链接')
    description = models.TextField(verbose_name='站点描述', max_length=128)
    category = models.ForeignKey(
        verbose_name='站点分类',
        to=SiteCategory,
        to_field='id',
        null=True,
        blank=True,
        related_name='sites',
        on_delete=models.SET_NULL,
        default=1
    )
    sort = models.IntegerField(verbose_name='排序')
    is_active = models.BooleanField(verbose_name='状态', default=True)
    logo = models.FileField(verbose_name='LOGO', max_length=128, null=True, blank=True, default='logo.png')
    tips = models.TextField(verbose_name='提示', max_length=128, null=True, blank=True)
    maintainer = models.ForeignKey(
        verbose_name='管理员',
        to='User',
        to_field='id',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title


class ContactCategory(models.Model):
    title = models.CharField(verbose_name='分类名称', max_length=64, unique=True)
    sort = models.IntegerField(verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title


class Contact(models.Model):
    TYPE_CHOICES = (
        (0, '无'),
        (1, '手机号码'),
        (2, '企业微信'),
        (3, '企业邮箱'),
    )
    person = models.CharField(verbose_name='联系人', max_length=64)
    description = models.CharField(verbose_name='职能描述', max_length=256)
    location = models.CharField(verbose_name='所属位置', max_length=256)
    contact_type = models.SmallIntegerField(verbose_name='联系类型', choices=TYPE_CHOICES, default=0)
    contact_key = models.CharField(verbose_name='联系方式', max_length=128, null=True, blank=True)
    category = models.ForeignKey(verbose_name='职能分类', to=ContactCategory, to_field='id', on_delete=models.CASCADE,
                                 related_name='contacts', default=1)
    sort = models.IntegerField(verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")


class Notification(models.Model):
    title = models.CharField(verbose_name='通知标题', max_length=128)
    content = models.TextField(verbose_name='通知内容', max_length=256)
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    is_active = models.BooleanField(verbose_name='状态', default=True)
    TYPE_CHOICES = (
        (0, 'info'),
        (1, 'success'),
        (2, 'warning'),
        (3, 'error'),
    )
    type = models.SmallIntegerField(verbose_name='通知类型', choices=TYPE_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
