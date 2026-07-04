from datetime import time

from django.core.management.base import BaseCommand

from matching.models import Availability, Mentor

DEMO_MENTORS = [
    {
        'name': 'Kokou AGBOTON',
        'subjects': 'Python, Django, Bases de données',
        'field_of_study': 'Génie Logiciel',
        'mentoring_format': Mentor.FORMAT_LES_DEUX,
        'availabilities': [(time(9, 0), time(12, 0)), (time(14, 0), time(16, 0))],
    },
    {
        'name': 'Aïssatou DIALLO',
        'subjects': 'Mathématiques, Algorithmique, Python',
        'field_of_study': 'Informatique',
        'mentoring_format': Mentor.FORMAT_EN_LIGNE,
        'availabilities': [(time(13, 0), time(15, 0))],
    },
    {
        'name': 'Michée HOUNSOU',
        'subjects': 'Réseaux, Sécurité informatique, Linux',
        'field_of_study': 'Systèmes et Réseaux',
        'mentoring_format': Mentor.FORMAT_PRESENTIEL,
        'availabilities': [(time(16, 0), time(18, 0))],
    },
    {
        'name': 'Fatou SANE',
        'subjects': 'JavaScript, React, HTML/CSS',
        'field_of_study': 'Génie Logiciel',
        'mentoring_format': Mentor.FORMAT_LES_DEUX,
        'availabilities': [(time(10, 0), time(12, 0)), (time(17, 0), time(19, 0))],
    },
    {
        'name': 'Ismaël TOURE',
        'subjects': 'Data Science, Python, Statistiques',
        'field_of_study': 'Intelligence Artificielle',
        'mentoring_format': Mentor.FORMAT_EN_LIGNE,
        'availabilities': [(time(8, 0), time(10, 0))],
    },
]


class Command(BaseCommand):
    help = "Pré-remplit la base de données avec des mentors de démonstration."

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help="Supprime tous les mentors existants avant d'insérer les données de démo.",
        )

    def handle(self, *args, **options):
        if options['flush']:
            deleted, _ = Mentor.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"{deleted} enregistrement(s) supprimé(s)."))

        created_count = 0
        for entry in DEMO_MENTORS:
            mentor, created = Mentor.objects.get_or_create(
                name=entry['name'],
                defaults={
                    'subjects': entry['subjects'],
                    'field_of_study': entry['field_of_study'],
                    'mentoring_format': entry['mentoring_format'],
                },
            )
            if created:
                for start, end in entry['availabilities']:
                    Availability.objects.create(mentor=mentor, start_time=start, end_time=end)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Mentor créé : {mentor.name}"))
            else:
                self.stdout.write(f"Mentor déjà existant, ignoré : {mentor.name}")

        self.stdout.write(self.style.SUCCESS(
            f"Terminé. {created_count} mentor(s) ajouté(s) sur {len(DEMO_MENTORS)} au total."
        ))
