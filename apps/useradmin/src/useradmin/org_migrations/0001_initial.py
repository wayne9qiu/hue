# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-01-15 19:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import useradmin.models2


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('desktop', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('token', models.CharField(default=None, max_length=128, null=True, verbose_name='Token')),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', useradmin.models2.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HuePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=30)),
                ('action', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('connector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desktop.Connector')),
            ],
            options={
                'verbose_name': 'Connector permission',
                'verbose_name_plural': 'Connector permissions',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LdapGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the organization', max_length=200, unique=True)),
                ('uuid', models.CharField(default=useradmin.models2.uuid_default, max_length=36, unique=True)),
                ('domain', models.CharField(help_text='The domain name of the organization, e.g. gethue.com', max_length=200, unique=True)),
                ('customer_id', models.CharField(default=None, max_length=128, null=True, verbose_name='Customer id')),
                ('is_active', models.BooleanField(default=True)),
                ('is_multi_user', models.BooleanField(default=True)),
            ],
            managers=[
                ('objects', useradmin.models2.OrganizationManager()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useradmin.Organization')),
                ('permissions', models.ManyToManyField(blank=True, to='useradmin.HuePermission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'organization group',
                'verbose_name_plural': 'organization groups',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_directory', models.CharField(max_length=1024, null=True)),
                ('creation_method', models.CharField(default='HUE', max_length=64)),
                ('first_login', models.BooleanField(default=True, help_text='If this is users first login.', verbose_name='First Login')),
                ('last_activity', models.DateTimeField(auto_now=True, db_index=True)),
                ('json_data', models.TextField(default='{}')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ldapgroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='useradmin.OrganizationGroup'),
        ),
        migrations.AddField(
            model_name='huepermission',
            name='groups',
            field=models.ManyToManyField(through='useradmin.GroupPermission', to='useradmin.OrganizationGroup'),
        ),
        migrations.AddField(
            model_name='huepermission',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useradmin.Organization'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useradmin.OrganizationGroup'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='hue_permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useradmin.HuePermission'),
        ),
        migrations.AddField(
            model_name='organizationuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='useradmin.OrganizationGroup', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='organizationuser',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useradmin.Organization'),
        ),
        migrations.AddField(
            model_name='organizationuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationgroup',
            unique_together=set([('name', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='huepermission',
            unique_together=set([('connector', 'action', 'organization')]),
        ),
    ]
