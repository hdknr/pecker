import mechanize as M
from models import Site,Run,Link,LinkResult,Case
from django.utils.timezone import now,localtime
from urlparse import urlparse
from requests.packages import chardet

import traceback
import time
import os

class Crawler(object):

    def __init__(self, site, name=None):

        self.site = site
        name = name or str( localtime( now() ) )
        self.run = Run( name=name, site = site )
        self.run.save()

        self.br = M.Browser()
        self.br.set_handle_robots(False)

    def crawl(self,result ,force=False):

        if result.link.available == False or result.status != None:
            if not force:
                return []

        #: get page
        res=self.br.open(result.link.url,timeout=2.0) 
        result.status = res.code  
        result.content_type = res.info()['Content-Type']

        if not result.content_type or result.content_type.find('text/') <0:
            #: PDF ... 
            result.save()
            return []

        result.set_output(res.get_data())

        result.save()

        #: page links
        next_links=result.children()

        #: page has cases
        for c in result.link.case_set.all():
            case_result, case_result_created= LinkResult.objects.get_or_create(
                                                run=self.run,
                                                link=result.link,
                                                case = c
                                            )
            #: TOOD: this implementation expect only 1 depth
            if case_result.status == None:
                if c.form_index >= 0 : 
                    self.br.select_form( nr = c.form_index )
                    for k,v in c.form_params.items(): 
                        self.br[ k ] = v
                    res = self.br.submit()
                    case_result.status = res.code
                    case_result.content_type=res.info()['Content-Type']
                    if result.content_type or result.content_type.find('text/') >=0:
                        case_result.set_output(res.get_data() )
                    case_result.save()

            self.br.open(result.link.url,timeout=2.0,)           #: access original page

        return next_links

    def start(self,url=None,parent=None,follow=True ,force=False):
        #: parent : parent Link instance
        self.br.clear_history()
        time.sleep(0.01 )        
        url = url or self.site.start_url

        result =None
        try:
            result = self.run.provide_result( url, parent )      
            if result == None:
                return 
            next_links = self.crawl( result,force=force)
        except:
            if result:
                result.errors = traceback.format_exc()
                result.save()
            return

        if not follow:
            return 

        for path in next_links:
            self.start(  path ,result.link)
