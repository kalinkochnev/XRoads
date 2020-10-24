from testutils.conftest import temp_img
from django.core.files.uploadedfile import SimpleUploadedFile

from XroadsAPI.tests.test_model_club import club_fix
import tempfile
from collections import OrderedDict
import random
import pytest

from XroadsAPI.serializers import *