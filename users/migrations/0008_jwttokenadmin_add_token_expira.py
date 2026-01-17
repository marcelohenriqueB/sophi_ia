# No-op migration to resolve duplicate column conflict.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_jwt_token'),
    ]

    operations = []
