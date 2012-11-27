import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_passbook.models import Pass, Registration
from django.shortcuts import get_object_or_404
import django.dispatch


pass_registered = django.dispatch.Signal()
pass_unregistered = django.dispatch.Signal()


@csrf_exempt
def register_pass(request, device_library_id, pass_type_id, serial_number):

    pass_ = get_object_or_404(
        Pass.objects.filter(pass_type_identifier=pass_type_id,
                            serial_number=serial_number))
    if request.META['HTTP_AUTHORIZATION'] != 'ApplePass %s' % pass_.authentication_token:
        return HttpResponse(status=401)
    registration = Registration.objects.filter(device_library_identifier=device_library_id,
                                               pazz=pass_)

    if request.method == 'POST':
        if registration:
            return HttpResponse(status=200)
        body = json.loads(request.body)
        new_registration = Registration(device_library_identifier=device_library_id,
                                        push_token=body['pushToken'],
                                        pazz=pass_)
        new_registration.save()
        pass_registered.send(sender=pass_)
        return HttpResponse(status=201)

    elif request.method == 'DELETE':
        registration.delete()
        pass_unregistered.send(sender=pass_)
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=400)


def latest_version(request, pass_type_id, serial_number):

    pass_ = get_object_or_404(
        Pass.objects.filter(pass_type_identifier=pass_type_id,
                            serial_number=serial_number))
    if request.META['HTTP_AUTHORIZATION'] != 'ApplePass %s' % pass_.authentication_token:
        return HttpResponse(status=401)

    return pass_.data
    