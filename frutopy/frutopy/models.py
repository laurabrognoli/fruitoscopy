from django.db import models
from django.contrib.postgres.fields import ArrayField
from .choices import RIPENESS_CHOICES
from .local_settings import BASE_IMG_DIR


# Machine Learning models
class ML_Model(models.Model):

    vals = models.TextField()

    def __string__(self):
        return self.path


# Signal Processing algorithms
class SP_Model(models.Model):

    vals = models.TextField()

    def __string__(self):
        return self.path


# Samples
class Sample(models.Model):

    spectrum = ArrayField(models.FloatField())
    fruit = models.IntegerField()
    label = models.SmallIntegerField(choices=RIPENESS_CHOICES)
    gps = models.TextField(null=True)
    tmstp = models.DateTimeField(null=True) # Timestamp
    image_path = models.FilePathField(BASE_IMG_DIR, null=True) # I'm not expecting the pickers to take a pic of every sample they scan, hence default=None
    label_is_right = models.NullBooleanField(default=False)
    ml_model = models.ForeignKey(ML_Model, on_delete=models.PROTECT)
    sp_model = models.ForeignKey(SP_Model, on_delete=models.PROTECT)

    def __string__(self):
        return self.pk

    class Meta:
        ordering = ['-tmstp']


# Images
class Image(models.Model):
    path = models.FilePathField(BASE_IMG_DIR)
    label = models.SmallIntegerField(choices=RIPENESS_CHOICES)
    label_is_right = models.NullBooleanField(default=False)
    tmstp = models.DateTimeField(auto_now_add=True, blank=True, editable=False)