from django.db import models
from django.contrib import gis
from django.contrib.auth.models import User

class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        abstract = True

class Area(Timestamped):
    '''
    Save Polygons'''
    
    name = models.CharField(max_length=100)
    geom = gis.db.models.GeometryField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=False)
    


    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.name

