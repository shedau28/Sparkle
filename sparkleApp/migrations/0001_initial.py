# Generated by Django 4.1.1 on 2022-09-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Master",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=30)),
                ("password", models.CharField(max_length=30)),
                ("f_name", models.CharField(max_length=20)),
                ("location", models.CharField(max_length=30)),
                (
                    "profile_pic",
                    models.ImageField(
                        default="blank_profile_picture.png", upload_to="profile_images"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("service_name", models.CharField(max_length=100)),
                ("desc", models.CharField(max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("service_price", models.IntegerField(default=0)),
            ],
        ),
    ]
