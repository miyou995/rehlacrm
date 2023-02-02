# Generated by Django 4.1.5 on 2023-02-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_lead_responsable"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lead",
            name="passport",
        ),
        migrations.AddField(
            model_name="contact",
            name="passport",
            field=models.FileField(blank=True, null=True, upload_to="images/passport"),
        ),
    ]