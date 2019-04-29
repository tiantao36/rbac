from django.db import models

# Create your models here.
'''
用户
角色

用户角色

权限
角色权限

权限组权限【管理权限方便找权限】
'''
# class Group(models.Model):
#     """
#     权限组
#     """
#     title = models.CharField(max_length=32)
#     parent = models.ForeignKey(to="Group",related_name='xx',null=True,blank=True)
#     is_group = models.BooleanField(verbose_name='是否是组')
#     class Meta:
#         verbose_name_plural = "权限组表"
#     def __str__(self):
#         return self.title

class Basepermission(models.Model):
    '''
    基础权限表
    '''
    title=models.CharField(verbose_name="基础访问权限名",max_length=32)
    url = models.CharField(verbose_name="含正则的URL", max_length=128)
    deny_userinfo=models.ForeignKey(verbose_name="拒绝用户",to="UserInfo",null=True,blank=True)
    class Meta:
        verbose_name_plural = "基础权限"   #admin中显示表明
    def __str__(self):
        return self.title   ##admin中显示对象名

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='菜单访问权限名',max_length=32)
    url = models.CharField(verbose_name="含正则的URL",max_length=128)
    is_menu = models.BooleanField(verbose_name="是否是菜单")
    parent = models.ForeignKey(to="Permission", related_name='pparent', null=True, blank=True)
    imgurl=models.CharField(verbose_name="菜单图标",max_length=128,null=True,blank=True)
    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    roles = models.ManyToManyField(verbose_name='具有的角色',to="Role",blank=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self): #可以在admin中显示对象的名字
        return self.username


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(verbose_name='角色名称',max_length=32)
    permissions = models.ManyToManyField(verbose_name="具有的权限",to='Permission',blank=True,related_name='rpermissions')
    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.title