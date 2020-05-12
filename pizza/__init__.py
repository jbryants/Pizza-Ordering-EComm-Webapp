# import celery to make sure it is loaded when Django starts
from .celery import app as celery_app

