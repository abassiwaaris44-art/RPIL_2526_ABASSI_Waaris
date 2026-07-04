"""
Algorithme de matching mentoré <-> mentors pour IFRI_MentorLink.

Critères :
1. Compatibilité des compétences / matières : au moins une matière en commun
   (comparaison insensible à la casse et aux espaces superflus).
2. Compatibilité horaire : l'heure souhaitée par le mentoré doit tomber
   dans un créneau du mentor, avec une tolérance de +/- 1 heure.
3. Filière (optionnelle) : n'est pas un critère éliminatoire, mais bonifie
   le score de compatibilité si elle correspond à celle du mentor.

Le score final est une note simple sur 100, combinant :
   - jusqu'à 60 points pour la proportion de matières en commun,
   - jusqu'à 30 points pour la qualité de la correspondance horaire
     (30 si l'heure tombe exactement dans un créneau, 20 si elle ne
     rentre que grâce à la tolérance de +/-1h),
   - jusqu'à 10 points bonus si la filière indiquée correspond à celle du mentor.
"""

from datetime import datetime, timedelta

TOLERANCE_MINUTES = 60  # tolérance horaire : +/- 1 heure


def parse_subjects(raw):
    """Transforme une chaîne 'Python, Django ; Réseaux' en liste normalisée."""
    if not raw:
        return []
    normalized = raw.replace(';', ',')
    return [s.strip().lower() for s in normalized.split(',') if s.strip()]


def _to_datetime(t):
    """Combine un objet time avec une date arbitraire, pour pouvoir soustraire/additionner."""
    return datetime.combine(datetime(2000, 1, 1), t)


def time_matches_slot(desired_time, start_time, end_time, tolerance_minutes=TOLERANCE_MINUTES):
    """
    Retourne (matched, exact) où :
      - matched = True si desired_time tombe dans [start-tol, end+tol]
      - exact   = True si desired_time tombe dans [start, end] (sans tolérance)
    """
    d = _to_datetime(desired_time)
    s = _to_datetime(start_time)
    e = _to_datetime(end_time)

    exact = s <= d <= e

    tol = timedelta(minutes=tolerance_minutes)
    matched = (s - tol) <= d <= (e + tol)

    return matched, exact


def compute_score(nb_requested_subjects, nb_common_subjects, time_matched, exact_slot,
                   filiere_requested, mentor_filiere):
    """Calcule un score de compatibilité simple sur 100."""
    subject_ratio = (nb_common_subjects / nb_requested_subjects) if nb_requested_subjects else 0
    subject_score = subject_ratio * 60

    time_score = 0
    if time_matched:
        time_score = 30 if exact_slot else 20

    filiere_score = 0
    if filiere_requested and mentor_filiere:
        if filiere_requested.strip().lower() == mentor_filiere.strip().lower():
            filiere_score = 10

    total = subject_score + time_score + filiere_score
    return round(min(total, 100), 1)


def find_matches(mentors_queryset, requested_subjects_raw, requested_time, filiere_raw=None):
    """
    Parcourt les mentors et retourne la liste des mentors compatibles,
    triés par score de compatibilité décroissant.

    mentors_queryset : QuerySet de Mentor (avec availabilities préchargées idéalement)
    requested_subjects_raw : chaîne brute saisie par le mentoré (ex: "Python, Réseaux")
    requested_time : objet datetime.time souhaité par le mentoré
    filiere_raw : chaîne optionnelle indiquée par le mentoré
    """
    requested_subjects = parse_subjects(requested_subjects_raw)
    results = []

    for mentor in mentors_queryset:
        mentor_subjects = mentor.get_subjects_list()

        # 1. Compétences en commun (comparaison insensible à la casse)
        common_subjects = [
            subject for subject in mentor_subjects
            if subject.lower() in requested_subjects
        ]
        if not common_subjects:
            continue  # pas de matière en commun -> pas de match

        # 2. Compatibilité horaire (avec tolérance +/-1h)
        time_matched = False
        exact_slot = False
        matched_availabilities = []

        for availability in mentor.availabilities.all():
            slot_matched, slot_exact = time_matches_slot(
                requested_time, availability.start_time, availability.end_time
            )
            if slot_matched:
                time_matched = True
                exact_slot = exact_slot or slot_exact
                matched_availabilities.append(availability)

        if not time_matched:
            continue  # aucun créneau compatible -> pas de match

        score = compute_score(
            nb_requested_subjects=len(requested_subjects),
            nb_common_subjects=len(common_subjects),
            time_matched=time_matched,
            exact_slot=exact_slot,
            filiere_requested=filiere_raw,
            mentor_filiere=mentor.field_of_study,
        )

        results.append({
            'id': mentor.id,
            'name': mentor.name,
            'common_subjects': common_subjects,
            'all_subjects': mentor_subjects,
            'field_of_study': mentor.field_of_study,
            'mentoring_format': mentor.get_mentoring_format_display(),
            'availabilities': [
                f"{a.start_time.strftime('%H:%M')} - {a.end_time.strftime('%H:%M')}"
                for a in mentor.availabilities.all()
            ],
            'exact_time_match': exact_slot,
            'score': score,
        })

    results.sort(key=lambda r: r['score'], reverse=True)
    return results
