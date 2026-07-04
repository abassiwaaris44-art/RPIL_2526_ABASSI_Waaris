#!/usr/bin/env python
"""Utilitaire en ligne de commande de Django pour IFRI_MentorLink."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifri_mentorlink.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez qu'il est installé et "
            "disponible dans votre environnement virtuel (voir requirements.txt)."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
