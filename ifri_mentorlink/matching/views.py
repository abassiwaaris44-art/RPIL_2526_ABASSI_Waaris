from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .matching_utils import find_matches
from .models import Mentor


def index(request):
    """Page unique : formulaire de recherche + zone de résultats (remplie en JS)."""
    return render(request, 'matching/index.html')


def search_mentors(request):
    """
    Endpoint JSON appelé en AJAX par le frontend.

    Paramètres GET attendus :
      - subjects : matières/compétences recherchées, séparées par des virgules (obligatoire)
      - time     : heure souhaitée au format HH:MM (obligatoire)
      - filiere  : filière du mentoré (optionnel)
    """
    subjects_raw = request.GET.get('subjects', '').strip()
    time_raw = request.GET.get('time', '').strip()
    filiere_raw = request.GET.get('filiere', '').strip()

    if not subjects_raw:
        return JsonResponse(
            {'error': "Veuillez indiquer au moins une matière ou compétence recherchée."},
            status=400,
        )

    if not time_raw:
        return JsonResponse(
            {'error': "Veuillez indiquer une heure souhaitée."},
            status=400,
        )

    try:
        requested_time = datetime.strptime(time_raw, '%H:%M').time()
    except ValueError:
        return JsonResponse(
            {'error': "Format d'heure invalide. Utilisez le format HH:MM (ex : 14:30)."},
            status=400,
        )

    mentors = Mentor.objects.prefetch_related('availabilities').all()
    matches = find_matches(mentors, subjects_raw, requested_time, filiere_raw)

    return JsonResponse({
        'count': len(matches),
        'results': matches,
    })
