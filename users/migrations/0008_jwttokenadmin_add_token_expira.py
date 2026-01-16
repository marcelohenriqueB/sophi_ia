# Generated manually to add token and expiration fields to JwtTokenAdmin
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_jwt_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwttokenadmin',
            name='token',
            field=models.TextField(unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jwttokenadmin',
            name='expira_em',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
