from rest_framework import serializers
from frutopy import models


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sample
        fields = '__all__'


class ML_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ML_Model
        fields = '__all__'

class SP_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SP_Model
        fields = '__all__'

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'