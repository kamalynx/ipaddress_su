import asyncio
import ipaddress

import httpx
import validators
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
    form = forms.WhoisForm()
    context["form"] = form

    if request.method == "POST":
        form = forms.WhoisForm(request.POST)
        context["form"] = form

        if form.is_valid():
            domain = form.cleaned_data.get("domain")
            return redirect("tools:nslookup_with_domain", str(domain))

    if domain is not None:
        form = forms.WhoisForm({'domain': domain})

        if not validators.domain(domain):
            raise Http404("Домен некорректен")

        result = asyncio.run(helpers.a_do_nslookup(domain))
        context["domain"] = domain
        context["ipsv4"] = result[0]
        context["ipsv6"] = result[1]
    return render(request, "tools/checkip.html", context=context)


class WhoisView(FormView):
    template_name = 'tools/whois.html'
    form_class = forms.WhoisForm

    def form_valid(self, form):
        print(form.cleaned_data['domain'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tools:whois')


def whois(request, input_ipaddress: str = None):
    context = {}
    form = forms.WhoisForm()
    context["form"] = form

    if request.method == "POST":
        form = forms.WhoisForm(request.POST)
        context["form"] = form

        if form.is_valid():
            input_ipaddress = form.cleaned_data.get("ipaddress")
            return redirect("tools:whois_with_ip", str(input_ipaddress))

    if input_ipaddress is not None:
        try:
            ipaddress.ip_address(input_ipaddress)
        except ValueError as err:
            raise Http404(err)

        form = forms.WhoisForm({'ipaddress': input_ipaddress})

        context["ipaddress"] = input_ipaddress
        context["whois"] = httpx.get(
            f"https://freeipapi.com/api/json/{input_ipaddress}"
        ).json()

    return render(request, "tools/whois.html", context=context)


def whois_domain(request, domain_name: str = None):
    context = {}
    form = forms.DomainForm()
    context["form"] = form

    if request.method == "POST":
        form = forms.DomainForm(request.POST)
        context["form"] = form

        if form.is_valid():
            domain_name = form.cleaned_data.get("domain")
            return redirect("tools:whois_with_domain", str(domain_name))

    if domain_name is not None:

        form = forms.DomainForm({'domain': domain_name})

        context["domain"] = domain_name
        context["whois"] = domain_name

    return render(request, 'tools/whois_domain.html', context=context)
