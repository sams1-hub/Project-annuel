from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from datetime import date
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from django_cassandra_engine.models import DjangoCassandraModel, columns

class MyModel(Model):
    my_primary_key = columns.UUID(primary_key=True, default=uuid.uuid4)
    # Rest of your model fields


class Alert(Model):
    home_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    date = columns.Date()
    time = columns.Time()
    message = columns.Text()

   

    class Meta:
        db_table = 'test.CDB'   # Specify the desired table name without the 'test.' prefix
        get_pk_field = 'home_id'  # Specify the primary key field to use in queries

    __keyspace__ = 'test'  # Specify the desired keyspace name
    __primary_keys__ = ('home_id', 'time')  # Define a composite primary key


