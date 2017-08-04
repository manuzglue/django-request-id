# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from . import generate_request_id, local, release_local
from .conf import REQUEST_ID_HEADER
import time

# TODO: Change name to id
def get_request_id(request):
    if hasattr(request, 'request_id'):
        return request.request_id
    elif REQUEST_ID_HEADER:
        return request.META.get(REQUEST_ID_HEADER, '')
    else:
        return generate_request_id()

def get_start_time(request):
    if hasattr(request, 's'):
        return request.s
    else:
        return time.time()

class RequestIdMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request_id = get_request_id(request)
        s = get_start_time(request)
        request.request_id = request_id
        local.request_id = request_id
        local.s = s
        response = self.get_response(request)

        release_local(local)

        return response

    # Compatibility methods for Django <1.10
    def process_request(self, request):
        request_id = get_request_id(request)
        request.request_id = request_id
        local.request_id = request_id

    def process_response(self, request, response):
        release_local(local)
        return response
