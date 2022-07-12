
from django.db import models
from django.contrib.auth.models import User
from importlib_metadata import email
import uuid

from django.utils import timezone
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = str(instance.pk)
    # ext = filename.split('.')[-1]
    # filename = '{}.{}'.format(instance.pk, ext)

    # return the whole path to the file
    return os.path.join(upload_to, filename)

def generate_uuid():
    return uuid.uuid4().hex


class fileupload(models.Model):
    id = models.CharField(primary_key = True, default=generate_uuid, editable=False, max_length=40)
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length = 254, null=True)
    password = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=500, null=True)
    filepath = models.FileField(upload_to=path_and_rename, null=True)

