# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Role


class GetUserRole(object):
    def process_request(self, request):
        request.role = None
        request.role_locked = False

        if request.user.is_authenticated():
            try:
                request.role = Role.objects.get(user=request.user)
                request.role_locked = request.role.is_locked

            except Role.DoesNotExist:
                request.role = Role.objects.create(
                    user=request.user,
                    creator=request.user,
                    target='fake',
                    name=unicode(request.user)
                )
