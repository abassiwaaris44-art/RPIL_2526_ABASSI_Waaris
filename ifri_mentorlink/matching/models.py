from django.db import models


class Mentor(models.Model):
    """Un mentor disponible dans l'annuaire IFRI_MentorLink."""

    FORMAT_PRESENTIEL = 'presentiel'
    FORMAT_EN_LIGNE = 'en_ligne'
    FORMAT_LES_DEUX = 'les_deux'

    FORMAT_CHOICES = [
        (FORMAT_PRESENTIEL, 'Présentiel'),
        (FORMAT_EN_LIGNE, 'En ligne'),
        (FORMAT_LES_DEUX, 'Présentiel et en ligne'),
    ]

    name = models.CharField('Nom du mentor', max_length=150)
    subjects = models.CharField(
        'Matières / compétences proposées',
        max_length=300,
        help_text="Liste de matières séparées par des virgules, ex : Python, Django, Bases de données",
    )
    field_of_study = models.CharField('Filière / niveau d\u2019études', max_length=150)
    mentoring_format = models.CharField(
        'Format de mentorat', max_length=20, choices=FORMAT_CHOICES, default=FORMAT_LES_DEUX
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

    def __str__(self):
        return self.name

    def get_subjects_list(self):
        """Retourne la liste des matières du mentor, nettoyées (sans espaces superflus)."""
        return [s.strip() for s in self.subjects.split(',') if s.strip()]


class Availability(models.Model):
    """Un créneau horaire de disponibilité pour un mentor."""

    mentor = models.ForeignKey(Mentor, related_name='availabilities', on_delete=models.CASCADE)
    start_time = models.TimeField('Heure de début')
    end_time = models.TimeField('Heure de fin')

    class Meta:
        ordering = ['start_time']
        verbose_name = 'Disponibilité'
        verbose_name_plural = 'Disponibilités'

    def __str__(self):
        return f"{self.mentor.name} : {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
