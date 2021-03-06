from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from rest_framework import viewsets
from .utils import handle_uploaded_file
from .models import ML_Model, SP_Model, Sample, Image
from .choices import RIPENESS_LABELS
from frutopy import serializers
import time
from io import BytesIO


class ML_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows machine learning models to be viewed or edited.
    """
    queryset = ML_Model.objects.all().order_by('-id')
    serializer_class = serializers.ML_ModelSerializer


class SP_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows signal processing models to be viewed, edited, or deleted.
    """
    queryset = SP_Model.objects.all().order_by('-id')
    serializer_class = serializers.SP_ModelSerializer


class SampleListView(View):
    """
    Allows user to check and modify labels and validate the sample for further training.
    """
    template_name = 'samples_list.html'

    def get(self, request):
        samples = Sample.objects.all()

        return render(request, self.template_name, context={'samples': samples})

    def post(self, request):
        samples = Sample.objects.all()
        validated = request.POST.getlist('validation')
        for s in samples:
            if s.label != RIPENESS_LABELS[str(request.POST[str(s.pk)]).lower()]:
                s.label = RIPENESS_LABELS[str(request.POST[str(s.pk)]).lower()]
                s.label_is_right = True
            elif str(s.pk) in validated:
                s.label_is_right = True
            elif str(s.pk) not in validated and s.label_is_right == True:
                s.label_is_right = False
            s.save()
        messages.success(request, 'Success! The database has been updated successfully.')
        return render(request, self.template_name, context={'samples': samples})


class ImageListView(View):
    """
    Allows user to check and modify labels and validate the sample for further training.
    """
    template_name = 'images_list.html'

    def get(self, request):
        image = Image.objects.all()

        return render(request, self.template_name, context={'image': image})

    def post(self, request):
        image = Image.objects.all()
        validated = request.POST.getlist('validation')
        for i in image:
            if i.label != RIPENESS_LABELS[str(request.POST[str(i.pk)]).lower()]:
                i.label = RIPENESS_LABELS[str(request.POST[str(i.pk)]).lower()]
                i.label_is_right = True
            elif str(i.pk) in validated:
                i.label_is_right = True
            elif str(i.pk) not in validated and i.label_is_right == True:
                i.label_is_right = False
            i.save()
        messages.success(request, 'Success! The database has been updated successfully.')
        return render(request, self.template_name, context={'images': images})


def upload_file(request):
    """
    Handles requests for file upload.
    """
    if request.method == 'POST':
        if (handle_uploaded_file(request.FILES['file'])):
            return HttpResponseRedirect('/success')
        return HttpResponseRedirect('/')
    return render(request, 'file_upload.html')


def handle_uploaded_image(image):
    a = str(int(time.time()))
    b = settings.IMG_TMP_PATH + a + '.jpg'
    with open(b) as fd:
        string = BytesIO()
        for chunk in image.chunks:
            fd.write(chunk)
        string.seek(0)
    # a = image_name (no ext)
    # b = image_path (con ext)
    conn = psycopg2.connect(settings.DB_PARAMS_CONNECT)
    cur = conn.cursor()
    table_name = 'frutopy_image'
    cur.execute("BEGIN;")
    cur.execute(
        """INSERT INTO %s (path, label) VALUES (%s, %d);"""
        % (table_name, b, 0))
    cur.execute("COMMIT;")


def upload_image(request):
    if request.method == 'POST':
        handle_uploaded_image(request.FILES['file'])
        return HttpResponseRedirect('/success')
    return render(request, 'image_upload.html')


def about(request):
    return render(request, 'about.html')


def success(request):
    """
    Redirects to Success page on successful file upload.
    """
    return render(request, 'success.html')

def home(request):
    """
    Home page.
    """
    return render(request, 'index.html')
