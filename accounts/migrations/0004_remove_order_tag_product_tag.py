# Generated by Django 4.1.3 on 2022-11-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_tag_order_customer_order_product_order_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(max_length=200, null=True, to='accounts.tag'),
        ),
    ]
