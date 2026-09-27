from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_PATH_NAMES = {"login"}


class SimplePasswordMiddleware:
    """
    Protège tout le site avec un mot de passe unique (pas de compte utilisateur).
    Une fois le bon mot de passe saisi, la session reste ouverte.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/static/") or request.path.startswith("/admin/"):
            return self.get_response(request)

        login_url = reverse("login")
        if request.path == login_url or request.session.get("authenticated"):
            return self.get_response(request)

        return redirect(login_url)
