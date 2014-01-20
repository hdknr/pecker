# -*- coding: utf-8 -*-

from optparse import make_option
from datetime import datetime
from urlparse import urlparse
import os

from django.conf import settings

from . import GenericCommand
from ...models import Site,Link,LinkResult
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

#        if True:
#            return 
#
#        for link in result:
#            current = urlparse( link )            
#            parent = urlparse(result.link.url)
#            fragment =  '' if current.fragment =='' else '#'+current.fragment
#             
#            if current.netloc !='' :
#                if current.netloc != result.link.site.host:
#                    continue
#            elif current.path.startswith('..'):
#                link = os.path.dirname(
#                    os.path.dirname( result.link.url )) + '/'+link[2:]
#            elif current.path.startswith('/'):
#                link = "%s://%s%s" % ( parent.scheme, parent.netloc, current.path ) 
#            else:
#                link = os.path.dirname( result.link.url )+ '/' +link[:]
#
#            if fragment:
#                link = link.replace(fragment,'')
#
#            print current.path, link
