# Generated by Django 4.0.3 on 2022-08-19 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_paymentitem_payment_alter_payment_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentitem', to='core.product'),
        ),
    ]