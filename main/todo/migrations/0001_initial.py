# Generated by Django 2.2 on 2019-04-25 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('taskdate', models.DateTimeField()),
                ('complete', models.BooleanField(default=False)),
                ('expire', models.BooleanField(default=False)),
                ('started', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Todo',
                'ordering': ('taskdate',),
            },
        ),
    ]
