# Generated by Django 5.2.3 on 2025-07-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0006_employee_password_delete_employeeprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='leave_type',
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='reason',
            field=models.TextField(default='not specified'),
            preserve_default=False,
        ),
    ]
