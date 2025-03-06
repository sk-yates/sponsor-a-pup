from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puppy',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Pupdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField(max_length=300)),
                ('picture_url', models.ImageField(max_length=400, upload_to='')),
                ('media_url', models.CharField(max_length=400)),
                ('date', models.DateField(verbose_name='Pupdate date')),
                ('pup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.puppy')),
            ],
        ),
    ]