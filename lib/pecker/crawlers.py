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

    def crawl(self,url,force=False):
        link,link_created = Link.objects.get_or_create(
                            site = self.site,
                            url  = url )
        
        result,result_created = LinkResult.objects.get_or_create(
                                    run = self.run,
                                    link = link,
                                    case = None 
                                )      
        if link.available == False or result.status != None:
            if not force:
                return []

        #: get page
        res=self.br.open(url,timeout=2.0) 
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
        for c in link.case_set.all():
            case_result, case_result_created= LinkResult.objects.get_or_create(
                                                run=self.run,
                                                link=link,
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
                    case_result.set_output(res.get_data() )
                    case_result.save()

            self.br.open(url,timeout=2.0,)           #: access original page

        return next_links

    def start(self,url=None,follow=True ,force=False):
        self.br.clear_history()
        time.sleep(0.01 )        
        try:
            url = url or self.site.start_url
            next_links = self.crawl( url ,force=force)
        except:
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print "@@@@ errror",url
            print traceback.format_exc()
            return

        if not follow:
            return 

        for path in next_links:
            self.start(  path   )
