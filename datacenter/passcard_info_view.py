import datetime
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def get_duration(visit):
    if visit.leaved_at is None:
        return timezone.now() - visit.entered_at

    return visit.leaved_at - visit.entered_at

def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)

    return duration > datetime.timedelta(minutes=minutes)


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    serialized_passcard_visits = []

    for visit in passcard_visits:
        passcard_visit = {
            "entered_at": visit.entered_at,
            "duration": get_duration(visit),
            "is_strange": is_visit_long(visit)
        }

        serialized_passcard_visits.append(passcard_visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": serialized_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
