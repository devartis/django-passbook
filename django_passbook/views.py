import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from django_passbook.models import Pass, Registration, Log
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Max
import django.dispatch


pass_registered = django.dispatch.Signal()
pass_unregistered = django.dispatch.Signal()


# Getting the Serial Numbers for Passes Associated with a Device
def registrations(request, device_library_id, pass_type_id):

    passes = Pass.objects.filter(registration__device_library_identifier=device_library_id,
                                 pass_type_identifier=pass_type_id)
    if passes.count() == 0:
        return HttpResponse(status=404)

    if 'passesUpdatedSince' in request.GET:
        passes = passes.filter(updated_at__gt=request.GET['passesUpdatedSince'])

    if passes:
        last_updated = passes.aggregate(Max('updated_at'))['updated_at__max']
        serial_numbers = [p.serial_number for p in passes.filter(updated_at=last_updated).all()]
        response_data = {'lastUpdated': last_updated.strftime("%Y-%m-%d"), 'serialNumbers': serial_numbers}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        return HttpResponse(status=204)


# Registering a Device to Receive Push Notifications for a Pass
# Unregistering a Device
@csrf_exempt
def register_pass(request, device_library_id, pass_type_id, serial_number):

    pazz = get_object_or_404(
        Pass.objects.filter(pass_type_identifier=pass_type_id,
                            serial_number=serial_number))
    if request.META['HTTP_AUTHORIZATION'] != 'ApplePass %s' % pass_.authentication_token:
        return HttpResponse(status=401)
    registration = Registration.objects.filter(device_library_identifier=device_library_id,
                                               pazz=pazz)

    if request.method == 'POST':
        if registration:
            return HttpResponse(status=200)
        body = json.loads(request.body)
        new_registration = Registration(device_library_identifier=device_library_id,
                                        push_token=body['pushToken'],
                                        pazz=pazz)
        new_registration.save()
        pass_registered.send(sender=pazz)
        return HttpResponse(status=201)

    elif request.method == 'DELETE':
        registration.delete()
        pass_unregistered.send(sender=pazz)
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=400)


def latest_pass(request, pass_type_id, serial_number):
    return Pass.objects.get(pass_type_identifier=pass_type_id,
                               serial_number=serial_number).updated_at


# Getting the Latest Version of a Pass
@condition(last_modified_func=latest_pass)
def latest_version(request, pass_type_id, serial_number):

    pass_ = get_object_or_404(
        Pass.objects.filter(pass_type_identifier=pass_type_id,
                            serial_number=serial_number))
    if request.META['HTTP_AUTHORIZATION'] != 'ApplePass %s' % pass_.authentication_token:
        return HttpResponse(status=401)

    response = HttpResponse(pass_.data.read(),
                            content_type='application/vnd.apple.pkpass')
    response['Content-Disposition'] = 'attachment; filename=pass.pkpass'
    return response    


# Errors logging
@csrf_exempt
def log(request):

    b = json.loads(request.body)
    for m in b['logs']:
        Log(message=m).save()
    return HttpResponse(status=200)
