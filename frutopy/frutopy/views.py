from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from .settings import APP_PATH
from .utils import handle_uploaded_file
from .models import ML_Model, SP_Model, Sample, ReducedSample, Image
from .choices import RIPENESS_LABELS
from frutopy import serializers as frutopy_serializers
import time
import json
from io import BytesIO


class ML_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows machine learning models to be viewed or edited.
    """
    queryset = ML_Model.objects.all().order_by('-id')
    serializer_class = frutopy_serializers.ML_ModelSerializer


class SP_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows signal processing models to be viewed, edited, or deleted.
    """
    queryset = SP_Model.objects.all().order_by('-id')
    serializer_class = frutopy_serializers.SP_ModelSerializer


class SampleListView(View):
    """
    Allows user to check and modify labels and validate the sample for further training.
    """

    def get(self, request):
        samples = ReducedSample.objects.all()
        return HttpResponse(serializers.serialize('json', samples),
                            content_type='application/json')

    def post(self, request):
        modified_sample = json.loads(request.read().decode("utf-8"))
        sample = Sample.objects.get(pk=modified_sample['pk'])
        if 'validated' in modified_sample:
            sample.label_is_right = modified_sample['validated']
        if 'label' in modified_sample:
            sample.label = modified_sample['label']
        print(sample.label)
        sample.save()
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')


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
    response = {'success': False}
    if request.method == 'POST':
        if handle_uploaded_file(request.FILES['file']):
            response['success'] = True
        return HttpResponse(json.dumps(response), content_type='application/json')


def handle_uploaded_image(image):
    a = str(int(time.time()))
    b = settings.IMG_TMP_PATH + a + '.jpg'
    with open(b) as fd:
        string = BytesIO()
        for chunk in image.chunks:
            fd.write(chunk)
        string.seek(0)
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

@ensure_csrf_cookie
def home(request):
    """
    Home page.
    """
    return redirect(APP_PATH)