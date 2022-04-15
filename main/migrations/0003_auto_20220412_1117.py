# Generated by Django 3.0.8 on 2022-04-12 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.doctor'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bill')),
            ],
        ),
    ]