from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
import pandas as pd
import csv  

#with open(r'1-30-s1c5-result-only-items.csv') as f:
#   reader = csv.reader(f,quotechar='""',delimiter = ',',
#                        quoting = csv.QUOTE_ALL,skipinitialspace = True)
#    for row in reader:
#       _, created = FDataFrame.objects.get_or_create(date2str = )
# Create your models here.

@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
@python_2_unicode_compatible       
class FDataFrame(models.Model):
    #date = models.DateField(blank = True,null=True,input_formats ='%m%d%Y')
    date = models.DateField(blank = True,null=True)
    date2str = models.CharField(max_length =10)
    frequentitems = models.CharField(max_length = 50)
    support = models.CharField(max_length =10)
    support_threshold = models.CharField(max_length = 10,null = True)
    confidence_threshold = models.CharField(max_length =10,null = True)
    
    def __str__(self):
        return '%s %s %s %s %s' % (self.date2str,self.frequentitems,self.support,self.support_threshold,self.confidence_threshold)
    #__repr__ = __str__ue
    

@python_2_unicode_compatible        
class ADataFrame(models.Model):
    #date = models.DateField(blank = True,null=True,input_formats ='%m%d%Y')
    date = models.DateField(blank = True,null=True)
    date2str = models.CharField(max_length =10)
    associationrules = models.CharField(max_length =60)
    confidence = models.CharField(max_length =10)
    support_threshold = models.CharField(max_length = 10,null = True)
    confidence_threshold = models.CharField(max_length =10,null=True)
    
    def __str__(self):
        return '%s %s %s %s %s' % (self.date2str,self.associationrules,self.confidence,self.support_threshold,self.confidence_threshold)
        
        
@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length = 10,verbose_name="full name")
    
    def __str__(self):
        return self.name
