import os
from datetime import timedelta

## Celery Settings
# Broker settings. (default: RabbitMQ)
BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@localhost:5672//")

# Using the database to store task state and results. (default: SQLite)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "database")
CELERY_RESULT_DBURI = os.getenv("CELERY_RESULT_DBURI", "sqlite:///mydatabase.db")

# List of modules to import when celery starts.
#CELERY_IMPORTS = ("myapp.tasks", )

#CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}
CELERY_TASK_SERIALIZER = os.getenv("CELERY_TASK_SERIALIZER", "pickle")

## APNS Configurations
APNS_CA_CERT_FILE       = "./entrust_2048_ca.cer"
APNS_CERT_FILE          = "./mycert.pem"
APNS_KEY_FILE           = "./mykey.pem"
APNS_PUSH_GATEWAY_URL   = "gateway.sandbox.push.apple.com:2195"
APNS_FEEDBACK_GATEWAY_URL    = "feedback.sandbox.push.apple.com:2196"

## GCM Configurations 
GCM_CA_CERT_FILE        = "./Equifax_Secure_Certificate_Authority.pem"
GCM_API_KEY             = "gcmapikey"
GCM_PUSH_GATEWAY_URL    = "https://android.googleapis.com/gcm/send"

## Scheduled Task Settings for APNS feedback
CELERYBEAT_SCHEDULE = {
    'collect_feedback': {
        'task': 'pushagent.tasks.add',
        'schedule': timedelta(seconds=60*60),
        'args': (1, 2)
    }
}

CELERY_TIMEZONE = 'UTC'

## Keep Unregistered devices information
UDEVICE_STORE = "csv"
UDEVICE_STORE_FILE ="./unregistered_devices.csv"
