import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_passbook.models import Pass, Registration
from django.shortcuts import get_object_or_404


@csrf_exempt
def register_pass(request, device_library_id, pass_type_id, serial_number):

    pass_ = get_object_or_404(Pass.objects.filter(pass_type_identifier=pass_type_id,
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
        return HttpResponse(status=201)

    elif request.method == 'DELETE':
        registration.delete()
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=400)

    # @pass = Passbook::Pass.where(pass_type_identifier: params[:pass_type_identifier], serial_number: params[:serial_number]).first
    # head :not_found and return if @pass.nil?
    # head :unauthorized and return if request.env['HTTP_AUTHORIZATION'] != "ApplePass #{@pass.authentication_token}"
    # @registration = @pass.registrations.where(device_library_identifier: params[:device_library_identifier]).first_or_initialize
    # @registration.push_token = params[:pushToken]
    # status = @registration.new_record? ? :created : :ok
    # @registration.save
    # head status
