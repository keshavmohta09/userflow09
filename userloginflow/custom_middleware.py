from django.contrib.auth.middleware import AuthenticationMiddleware , get_user
from django.utils.functional import SimpleLazyObject
import jwt
from django.conf import settings
from authentication.models import User


class CustomAuthentication(AuthenticationMiddleware):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        token = request.session.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token,algorithms=["RS256","HS256"],options={"verify_signature":True}, key=settings.SECRET_KEY)
            except:
                pass
            try:
                request.user = User.objects.get(pk=payload['id'])
                return
            except User.DoesNotExist:
                pass
        request.user = SimpleLazyObject(lambda: get_user(request))
        
        
