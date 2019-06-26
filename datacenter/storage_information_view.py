from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def get_format_time(timedelta):
    return ':'.join(str(timedelta).split(':')[:2])


def storage_information_view(request):
    visitors_not_leaved = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for visitor in visitors_not_leaved:
        duration = get_format_time(timezone.now() - visitor.entered_at)
        visit = {
            "who_entered": visitor.passcard,
            "date": visitor.entered_at,
            "duration": duration,
        }
        non_closed_visits.append(visit)
    
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
