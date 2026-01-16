from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('viagens', '0024_reserva_embarque_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='status_reserva',
            field=models.CharField(
                choices=[
                    ('AGUARDANDO_PAGAMENTO', 'Aguardando Pagamento'),
                    ('PAGAMENTO_CONFIRMADO', 'Pagamento Confirmado'),
                    ('AGUARDANDO_EMBARQUE', 'Aguardando Embarque'),
                    ('EMBARCADO', 'Embarcado'),
                    ('CANCELADA', 'Cancelada'),
                    ('REEMBOLSADA', 'Reembolsada'),
                ],
                default='AGUARDANDO_PAGAMENTO',
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='tempo_pagamento',
            field=models.DateTimeField(
                blank=True,
                help_text='Data/hora do timeout de pagamento',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='data_embarque',
            field=models.DateTimeField(
                blank=True,
                help_text='Data/hora do embarque confirmado',
                null=True,
            ),
        ),
    ]
