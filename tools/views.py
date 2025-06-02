import asyncio

import httpx
import validators
import whois
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView
from ipware import get_client_ip
from tools import forms, helpers


class HomePage(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        """Add client ip to context data."""

        client_ip = get_client_ip(self.request)[0]
        kwargs['ipaddress'] = client_ip

        return super(HomePage, self).get_context_data(**kwargs)


def nslookup(request, domain: str = None):
    context = {}

    if request.method == "POST":
        form = forms.DomainForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data.get("domain")
            return redirect("tools:nslookup_with_domain", str(domain))
    else:
        form = forms.DomainForm()

    if domain is not None:
        form = forms.DomainForm({'domain': domain})

        if not validators.domain(domain):
            raise Http404("Домен некорректен")

        result = asyncio.run(helpers.a_do_nslookup(domain))
        context["domain"] = domain
        context["ipsv4"] = result[0]
        context["ipsv6"] = result[1]
    context['form'] = form
    return render(request, "tools/checkip.html", context=context)


def whois_view(request, domain: str = None):
    context = {}

    if request.method == "POST":
        form = forms.DomainForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data.get("domain")
            return redirect("tools:whois_with_domain", str(domain))
    else:
        form = forms.DomainForm()

    if domain is not None:
        form = forms.DomainForm({'domain': domain})

        if not validators.domain(domain):
            raise Http404("Домен некорректен")

        result = whois.whois(domain)
        context['result'] = result

    context['form'] = form
    return render(request, "tools/whois.html", context=context)


def ipinfo_view(request, ip: str = None):
    context = {}

    if request.method == "POST":
        form = forms.IPForm(request.POST)

        if form.is_valid():
            ip = form.cleaned_data.get("ipaddress")
            return redirect("tools:ipinfo_with_ip", str(ip))
    else:
        form = forms.IPForm()

    if ip is not None:
        form = forms.IPForm({'ipaddress': ip})

        params = {
            'lang': 'ru',
            'fields': ','.join((
                'status',
                'message',
                'country',
                'countryCode',
                'regionName',
                'city',
                'lat',
                'lon',
                'timezone',
                'isp',
                'org',
                'as',
                'reverse',
                'mobile',
                'proxy',
                'query',
            )),
        }

        with httpx.Client() as client:
            result = client.get(f'http://ip-api.com/json/{ip}', params=params)

        context['result'] = result.json()

    context['form'] = form
    context['ip'] = ip
    return render(request, "tools/ipinfo.html", context=context)
