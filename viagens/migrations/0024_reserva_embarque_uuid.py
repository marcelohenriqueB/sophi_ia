from django.db import migrations, models
import uuid


def generate_uuids(apps, schema_editor):
    Reserva = apps.get_model('viagens', 'Reserva')
    for reserva in Reserva.objects.all():
        reserva.embarque_uuid = uuid.uuid4()
        reserva.save(update_fields=['embarque_uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('viagens', '0023_remove_rota_suites'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='embarque_uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generate_uuids, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='reserva',
            name='embarque_uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
