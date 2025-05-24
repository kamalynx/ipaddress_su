import asyncio
import ipaddress

import httpx
import validators
import whois
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, FormView
from ipware import get_client_ip
from markdown import markdown

from . import forms, helpers


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


class WhoisView(FormView):
    template_name = 'tools/whois.html'
    form_class = forms.DomainForm

    def form_valid(self, form):
        domain = form.cleaned_data['domain']
        print(domain)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tools:whois')
