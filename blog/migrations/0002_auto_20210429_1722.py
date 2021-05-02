# Generated by Django 3.2 on 2021-04-29 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='main_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=300)),
                ('slugurl', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='main_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.main_category'),
            preserve_default=False,
        ),
    ]