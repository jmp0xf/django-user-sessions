# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

from ipware.ip import get_ip

class SessionMiddleware(SessionMiddleware):
    """
    Middleware that provides ip and user_agent to the session store.
    """
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = self.SessionStore(
            ip=get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            session_key=session_key
        )
