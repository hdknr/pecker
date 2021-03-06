# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField
from datetime import timedelta
from hashlib import md5
from requests.packages import chardet

from bs4 import BeautifulSoup as Soup
from urlparse import urlparse,urljoin
import os
import re
import ast

class Site(models.Model):
    name= models.CharField( max_length=20,unique=True )
    host =  models.CharField( max_length=30, null=True,blank=True,)
    scheme =  models.CharField( max_length=5, default='https' )
    start_url = models.CharField( max_length=300,null=True,blank=True, )
    ignore_regex=  models.TextField( null=True,blank=True,default=None ) 

    class Meta:
        verbose_name = _(u'Site') 
        verbose_name_plural = _(u'Sites') 

    def __unicode__(self):
        return self.name

    def delete_all_links(self):
        self.link_set.all().delete()

    def regexs(self):
        ret = getattr(self,'_regex',None)
        if ret != None:
            return ret
 
        if not self.ignore_regex:
            return []
        setattr(self,'_regex',[ re.compile( ast.literal_eval(restr),re.IGNORECASE) 
                for restr in self.ignore_regex.split('\n') if restr])
        return self._regex
    
    def ignore_url(self,url):

        for r in self.regexs():
            if r.search(url) :
                return True

        return False

class Run(models.Model):
    site = models.ForeignKey(Site)
    name= models.CharField( max_length=20,unique=True )

    class Meta:
        verbose_name = _(u'Run') 
        verbose_name_plural = _(u'Runs') 

    def __unicode__(self):
        return self.name

    def provide_result(self,url,parent=None):
        link,link_created = Link.objects.get_or_create(
                            site = self.site,
                            url  = url )

        if link_created and parent:
            link.parent = parent
            link.save()

        if self.site.ignore_url(url):
            return None

        result,result_created = LinkResult.objects.get_or_create(
                                    run = self,
                                    link = link,
                                    case = None
                                )
        return result
 

class Link(models.Model):
    site = models.ForeignKey(Site)
    parent= models.ForeignKey('self',default=None,null=True,blank=True,on_delete=models.SET_NULL)
    url_hash = models.CharField( max_length=50,db_index=True,unique=True,blank=True )
    url = models.CharField( max_length=300,)
    available  = models.BooleanField( default=True ) 

    class Meta:
        verbose_name = _(u'Link') 
        verbose_name_plural = _(u'Links') 

    def __unicode__(self):
        return self.url

    def save(self,*args,**kwargs):
        self.url_hash = md5( self.url).hexdigest()
        super(Link,self).save(*args,**kwargs )

class Case(models.Model):
    link = models.ForeignKey(Link)
    form_index = models.IntegerField()  
    ''' Form Index :  -1 : GET with query_params, >=0 : POST with form_params(&query_params) '''
    form_params = JSONField(null=True,blank=True,)
    query_params = JSONField(null=True,blank=True,)

    class Meta:
        verbose_name = _(u'Case') 
        verbose_name_plural = _(u'Cases') 

    def __unicode__(self):
        return  self.link and self.link.__unicode__() or 'unspecified'
   

class LinkResult(models.Model):
    run = models.ForeignKey(Run)
    link = models.ForeignKey(Link) 
    case =  models.ForeignKey(Case,null=True,default=None,blank=True,) 
    status =  models.CharField( max_length=3,null=True,blank=True, )
    content_type =  models.CharField( max_length=20,null=True,blank=True, )
    output = models.TextField( null=True,blank=True,default=None ) 
    errors =  models.TextField( null=True,blank=True,default=None ) 
    created_at = models.DateTimeField(_(u'Created Time'),auto_now_add=True)

    class Meta:
        verbose_name = _(u'LinkResult') 
        verbose_name_plural = _(u'LinkResults') 

    def set_output(self,text,charset=None):
        #: TODO: MUST do nothing on unicode python 2.7
        if not charset: 
            charset = chardet.detect(text)['encoding']
        self.output = text.decode(charset)

    def soup(self):
        return Soup(self.output) 

    def children(self): 
        _links = [ ln['href'] for ln in  Soup(self.output).select('a') 
                if ln.has_attr('href') and not ln['href'].startswith('#') and not ln['href']=='' ]

        result_links =[]
        for link in _links:
            current = urlparse( link )    
            parent = urlparse( self.link.url)
            fragment =  '' if current.fragment =='' else '#'+current.fragment
            query = '' if current.query == '' else '?' + current.query

            if current.netloc !='' :
                if current.netloc != self.link.site.host:
                    continue

            link = urljoin( parent.path, current.path).replace('../','')
    
            if fragment:
                link = current.path.replace(fragment,'')
            
            if link != '' and link[0] != '/':             
                link = '/' + link

            result_links.append( "%s://%s%s%s" % ( parent.scheme, parent.netloc,link,query) )

        return result_links
