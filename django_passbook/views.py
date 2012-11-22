import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_passbook.models import Registration


@csrf_exempt
def register_pass(request, device_library_id, pass_type_id, serial_number):
    if request.method != 'POST':
        return HttpResponse(status=400)

    if request.META['HTTP_AUTHORIZATION'] != 'ApplePass ' + 'HOLAHOLAHOLAHOLA':
        return HttpResponse(status=401)

    registration = Registration.objects.filter(device_library_identifier=device_library_id,
                                               pass_type_identifier=pass_type_id,
                                               serial_number=serial_number)
    if registration:
        return HttpResponse(status=200)

    body = json.loads(request.body)
    new_registration = Registration(device_library_identifier=device_library_id,
                                    pass_type_identifier=pass_type_id,
                                    serial_number=serial_number,
                                    push_token=body['pushToken'])
    new_registration.save()

    return HttpResponse(status=201)
