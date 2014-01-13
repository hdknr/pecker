# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField
from datetime import timedelta
from hashlib import md5

class Site(models.Model):
    name= models.CharField( max_length=20,unique=True )
    host =  models.CharField( max_length=15, null=True,blank=True,)
    start_url = models.CharField( max_length=300,null=True,blank=True, )

    class Meta:
        verbose_name = _(u'Site') 
        verbose_name_plural = _(u'Sites') 

    def __unicode__(self):
        return self.name

class Run(models.Model):
    site = models.ForeignKey(Site)
    name= models.CharField( max_length=20,unique=True )

    class Meta:
        verbose_name = _(u'Run') 
        verbose_name_plural = _(u'Runs') 

class Link(models.Model):
    site = models.ForeignKey(Site)
    url_hash = models.CharField( max_length=50,db_index=True,unique=True,blank=True )
    url = models.CharField( max_length=300,)

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
    form_params = JSONField()
    query_params = JSONField()

    class Meta:
        verbose_name = _(u'Case') 
        verbose_name_plural = _(u'Cases') 
   

class LinkResult(models.Model):
    run = models.ForeignKey(Run)
    link = models.ForeignKey(Link) 
    case =  models.ForeignKey(Case,null=True,default=None,blank=True,) 
    status =  models.CharField( max_length=3,null=True,blank=True, )
    output = models.TextField( null=True,blank=True ) 

    class Meta:
        verbose_name = _(u'LinkResult') 
        verbose_name_plural = _(u'LinkResults') 
