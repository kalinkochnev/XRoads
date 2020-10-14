import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.urls import reverse
from django.core import mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from XroadsAPI.serializers import *

    
    
