from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from django import http
from django import shortcuts


def home(request):
    return shortcuts.render(request, 'devsite/home.html', {
        'user': request.user,
    })

def logout(request):
    auth.logout(request)
    messages.success(request, u"Logout successful.")
    return http.HttpResponseRedirect(reverse('home'))
