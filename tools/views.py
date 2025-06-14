import validators
import netaddr
import whois
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView
from django.utils import timezone
from ipware import get_client_ip

from tools import forms, helpers, models


class HomePage(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        """Add client ip to context data."""

        client_ip = get_client_ip(self.request)[0]
        kwargs['ipaddress'] = client_ip

        return super(HomePage, self).get_context_data(**kwargs)


def nslookup_view(request, domain: str = None):
    context = {}

    if request.method == 'POST':
        form = forms.DomainForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data.get('domain')
            return redirect('tools:nslookup_with_domain', str(domain))
    else:
        form = forms.DomainForm()

    if domain is not None:
        form = forms.DomainForm({'domain': domain})

        if not validators.domain(domain):
            raise Http404('Домен некорректен')

        result = helpers.nslookup(domain)
        context['domain'] = domain
        context['ipsv4'] = result[0]
        context['ipsv6'] = result[1]

        domain_model, created = models.DomainLog.objects.get_or_create(
            name=domain, view_type='nslookup'
        )
        domain_model.timestamp = timezone.now()
        domain_model.save()

    context['form'] = form
    context['log'] = models.DomainLog.objects.filter(
        view_type='nslookup'
    ).all()[:10]
    return render(request, 'tools/checkip.html', context=context)


def ipinfo_view(request):
    if request.method == 'POST':
        form = forms.IPForm(request.POST)

        if form.is_valid():
            ip = netaddr.IPAddress(form.cleaned_data.get('ipaddress'))

            if any(
                [
                    ip.is_ipv4_private_use(),
                    ip.is_reserved(),
                    ip.is_loopback(),
                ]
            ):
                ip = get_client_ip(request)[0]  # works only on prod :)

            return redirect('tools:ipinfo_with_ip', str(ip))
    else:
        form = forms.IPForm()

    context = {'form': form, 'log': models.IPLog.objects.all()[:10]}
    return render(request, 'tools/ipinfo.html', context=context)


def ipinfo_with_ip(request, ip: str = None):
    if request.method == 'POST':
        form = forms.IPForm(request.POST)

        if form.is_valid():
            ip = form.cleaned_data.get('ipaddress')
    else:
        form = forms.IPForm({'ipaddress': ip})

    ip_model, created = models.IPLog.objects.get_or_create(address=ip)
    ip_model.timestamp = timezone.now()
    ip_model.save()

    context = {
        'result': helpers.get_ip_info(ip),
        'form': form,
        'ip': ip,
        'log': models.IPLog.objects.all()[:10],
    }
    return render(request, 'tools/ipinfo.html', context=context)


def ipcalc_view(request):
    context = {}

    if request.method == 'POST':
        form = forms.IPv4CalcForm(request.POST)

        if form.is_valid():
            ipaddress = form.cleaned_data['ipaddress']
            cidr = form.cleaned_data['netmask']
            context['result'] = netaddr.IPNetwork(f'{ipaddress}/{cidr}')
    else:
        form = forms.IPv4CalcForm()

    context['form'] = form

    return render(request, 'tools/ipcalc.html', context=context)


def whois_view(request):
    if request.method == 'POST':
        form = forms.DomainForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data.get('domain')

            return redirect('tools:whois_with_domain', domain)
    else:
        form = forms.DomainForm()

    context = {'form': form, 'log': models.DomainLog.objects.all()[:10]}
    return render(request, 'tools/whois.html', context=context)


def whois_with_domain(request, domain: str = None):
    if request.method == 'POST':
        form = forms.DomainForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data.get('domain')
            return redirect('tools:whois_with_domain', domain)
    else:
        form = forms.DomainForm({'domain': domain})


    try:
        whois_data = whois.whois(domain).text
    except whois.parser.PywhoisError as err:
        raise Http404(err)

    ip_model, created = models.DomainLog.objects.get_or_create(name=domain)
    ip_model.timestamp = timezone.now()
    ip_model.save()

    context = {
        'result': whois_data,
        'form': form,
        'domain': domain,
        'log': models.DomainLog.objects.all()[:10],
    }
    return render(request, 'tools/whois.html', context=context)
