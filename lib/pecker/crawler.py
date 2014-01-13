import mechanize as M
from models import Site,Run

class Crawler(object):

    def __init__(self, site):
        self.site = site
        self.run = Run( name="name", site = site )
        self.run.save()

        self.crawled={}

        self.br = M.Browser()
        self.br.set_handle_robots(False)

        self.login()

    def url(self,path='/'):
        return "https://%s%s" %( self.host, path )

    def get(self,url):
        if not self.crawled.has_key(url):
            res=self.br.open(url) 
            self.crawled[ url ] = res.code
            headers = res.info()
            print "@@@@ ",url,">",res.code
            if headers['Content-Type'].find('text/') <0:
                return False
            return True
        return False

    def login(self):
        self.br.open( self.site.auth_url )
        self.br.select_form(nr=0 )      # TODO: First Form
        self.br[ 'username']= site.auth_user        # TODO:
        self.br[ 'password']= site.auth_password    # TODO:
        res = self.br.submit()

        self.crawled[ url ] = res.code          #:TODO

    def crawl(self,url=None):
        if url != None and not self.get( url ):
            return

        #: given path
        paths= [ link.url for link in self.br.links()
                    if link.url.startswith('/') ]
        
        # TODO: absolute url 

        for path in paths:
            self.crawl( self.url( path )  )
