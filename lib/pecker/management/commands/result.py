# -*- coding: utf-8 -*-

from optparse import make_option
from datetime import datetime
from urlparse import urlparse
import os

from django.conf import settings

from . import GenericCommand
from ...models import Site,Link,LinkResult,Run
from ...crawlers import Crawler

class Command(GenericCommand):
    ''' crawl
    '''

    option_list = GenericCommand.option_list + ( 
        make_option('--run',
            action='store',
            dest='run',
            default=None,
            help=u'run name'),
        )   

    def handle_list_links(self,result_id,run,*args,**options):
        ''' reuslt list_links 1 '''
        if not id:
            print 'python manage.py result list_link {{ LinkResult.id }} '
            return 

        result = LinkResult.objects.get(id=result_id)
        for link in result.children():
            print link

    def handle_list_anchors(self,result_id,run,*args,**options):
        ''' reuslt list_anchors 1 '''
        if not id:
            print 'python manage.py result list_anchors {{ LinkResult.id }} '
            return 

        result = LinkResult.objects.get(id=result_id)
        for link in result.soup().select('a'):
            print link.get('href','')

    def handle_list_forms(self,run,*args,**options):
        run = Run.objects.get(name=run) 
        print "Results",run.linkresult_set.exclude(output = None).count()
        for result in run.linkresult_set.exclude(output = None):
            forms = result.soup().select('form')
            if len(forms) > 0:
                print result.link.url, len(forms)

    def handle_list_exts(self,run,*args,**options):
        run = Run.objects.get(name=run) 
        
        out={} 
        for result in run.linkresult_set.all():
            u = urlparse( result.link.url )
            ext = os.path.splitext(u.path)[1] 
            out[ext] = out.get(ext,0) + 1

        print out
