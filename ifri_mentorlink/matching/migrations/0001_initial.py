from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom du mentor')),
                ('subjects', models.CharField(
                    help_text='Liste de matières séparées par des virgules, ex : Python, Django, Bases de données',
                    max_length=300,
                    verbose_name='Matières / compétences proposées',
                )),
                ('field_of_study', models.CharField(max_length=150, verbose_name='Filière / niveau d\u2019études')),
                ('mentoring_format', models.CharField(
                    choices=[
                        ('presentiel', 'Présentiel'),
                        ('en_ligne', 'En ligne'),
                        ('les_deux', 'Présentiel et en ligne'),
                    ],
                    default='les_deux',
                    max_length=20,
                    verbose_name='Format de mentorat',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Mentor',
                'verbose_name_plural': 'Mentors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='Heure de début')),
                ('end_time', models.TimeField(verbose_name='Heure de fin')),
                ('mentor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='availabilities',
                    to='matching.mentor',
                )),
            ],
            options={
                'verbose_name': 'Disponibilité',
                'verbose_name_plural': 'Disponibilités',
                'ordering': ['start_time'],
            },
        ),
    ]
