from __future__ import unicode_literals

import logging


class LogPostData(object):
    def process_request(self, request):
        if request.POST:
            log = logging.getLogger('post')
            data = {k: v for k, v in request.POST.items() if 'pass' not in k and k != 'csrfmiddlewaretoken'}
            log.info(
                '%s (user %s): %r',
                request.META.get('PATH_INFO', '-'),
                request.user.is_authenticated() and request.user.id or 'anon',
                data,
            )
