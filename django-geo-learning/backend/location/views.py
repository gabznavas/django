from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from .models import Location
import json

from django.contrib.gis.geos import Point


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


@login_required
def save_location(request: HttpRequest):
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Validate the data
        if not all([latitude, longitude]):
            return JsonResponse({
                'status': 'error',
                'message': 'Incomplete location data'
            }, status=400)

        # save user location
        Location.objects.update_or_create(
            user=request.user,
            defaults={
                'point': Point(
                    float(longitude),
                    float(latitude),
                ),
            }
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Location saved successfully'
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
