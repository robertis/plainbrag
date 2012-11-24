from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse
import datetime



def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k,v in values:
        html.append('<tr><td>%s </td></td>%s </td></tr>' %(k,v))

    return HttpResponse('<table>%s</table>' % '\n'.join(html))


