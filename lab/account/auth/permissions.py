# -*- coding: utf-8 -*- 
from django.db import models

PERMISSIONS = [
    (m.get_ar_name() , [
                    'list_%s' % m.__name__.lower(),
                    'add_%s' % m.__name__.lower(),
                    'change_%s' % m.__name__.lower(),
                    'delete_%s' % m.__name__.lower()])
               
    for m in models.get_models(include_auto_created=False) if
         not str(m.__module__).startswith('django') and not
         str(m.__module__).startswith('common')]