# -*- coding: utf-8 -*-

from optparse import make_option
from datetime import datetime

from django.conf import settings

from . import GenericCommand
from ...models import Site,Link
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

    def handle_site(self,id,run,*args,**options):
        ''' crawl site --id=1 '''
        if not id:
            print 'python manage.py crawl site --id={{ Site.id }} '
            return 

        site = Site.objects.get(id=id)
        c=Crawler( site,name=run)
        c.start(force=True)

    def handle_url(self,id,*args,**options):
        if not id:
            print 'python manage.py crawl url --id={{ Link.id }} '
            return 

        link= Link.objects.get(id=id)
        c=Crawler( link.site )
        c.start( link.site.start_url ,follow=False) #:authentication
        c.start( link.url ,follow=False)
        
