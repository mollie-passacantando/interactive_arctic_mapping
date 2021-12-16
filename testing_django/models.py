from django.db import models
from django.contrib.postgres.fields import ArrayField


class DataModel(models.Model):
    # Put your fields here
    TrackID = models.CharField(max_length=100, blank=True,null=True)
    lats = ArrayField(ArrayField(models.DecimalField(max_digits=40,decimal_places=30),null=True))
    lons = ArrayField(ArrayField(models.DecimalField(max_digits=40,decimal_places=30),null=True))
    heights = ArrayField(ArrayField(models.DecimalField(max_digits=40,decimal_places=30),null=True),null=True)
    dist_along_track = ArrayField(ArrayField(models.DecimalField(max_digits=40,decimal_places=30)),null=True)
    # segment_length = ArrayField(ArrayField(models.IntegerField(),null=True))
        
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.TrackID
