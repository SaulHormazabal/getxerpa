# Generated by Django 5.0 on 2023-12-29 05:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enrichment", "0002_category_created_at_category_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="keyword",
            name="weight",
            field=models.IntegerField(default=1),
        ),
    ]
