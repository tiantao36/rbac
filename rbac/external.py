#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rbac.settings")
    import django
    django.setup()

    from app01 import models

    obj = models.Permission.objects.all()
    print(obj)