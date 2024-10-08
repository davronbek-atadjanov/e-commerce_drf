# Generated by Django 5.1 on 2024-08-09 10:36

import accounts.utility
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,13}$')], verbose_name='Phone number')),
                ('apartment', models.CharField(max_length=120, verbose_name='Apartment')),
                ('street', models.TextField(verbose_name='Street')),
                ('pin_code', models.CharField(max_length=60, verbose_name='Pin code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user address',
                'verbose_name_plural': 'user addresses',
            },
        ),
        migrations.CreateModel(
            name='VerificationOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(validators=[accounts.utility.check_otp_code], verbose_name='Verification Code')),
                ('type', models.CharField(choices=[('register', 'register'), ('reset_password', 'reset password')], max_length=20, verbose_name='Verification Type')),
                ('expires_in', models.DateTimeField(verbose_name='expires in ')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_otp', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification OTP',
                'verbose_name_plural': 'Verification OTPs',
                'ordering': ['-expires_in'],
            },
        ),
    ]
