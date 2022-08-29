# Generated by Django 4.0.3 on 2022-08-19 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_paymentitem_date_created_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentitem',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.payment'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.product'),
        ),
    ]
