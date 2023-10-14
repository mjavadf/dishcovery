# Generated by Django 4.2.4 on 2023-08-21 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0005_profile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "ordering": ["user__first_name", "user__last_name"],
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]