import requests

import urllib.parse as urlparse
import logging
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout
from portal.forms import SignupForm, LoginForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from portal.models import Controller, Device
from tests import constants
# Create your views here.

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class CaptivePortalDispatcher(View):
    def get(self, request):
        print(request.get)
        return redirect('/portal/signup/')


class RegisterTmp(View):
    def get(self, request):
        return render(request, 'login.html')


logger = logging.getLogger(__name__)


class PortalSignup(View):
    def get(self, request):
        print(request.session['template_name'])
        request_well_formed = False
        request_well_formed = RequestAnalyser.coovachilli_signup(request)
        if request_well_formed:
            controller = Controller.objects.filter(uuid=request.session['controller_id'])
            if controller:
                controller = controller[0]
                Device.objects.register_device(mac=request.session['mac'],
                                               user_agent=request.META['HTTP_USER_AGENT'])
                request.session['controller_id'] = request.session['controller_id']
                request.session['controller_model_name'] = \
                    constants.ControllersTypes.choices[controller.controller_model - 1][1]
                request.session['controllers_types'] = constants.ControllersTypes.choices
                request.session['controller_ip'] = request.session['controller_ip']
                request.session['redirect_url'] = controller.redirect_url
                request.session['template_name'] = 'sign_up'
                print(request.session['template_name'])
                form = SignupForm()
                return render(request, 'sign_up.html',{'form': form})
            else:
                logger.warning('No controller was found for uuid: %s', request.session['controller'])
                form = SignupForm()
                return render(request, 'sign_up.html', {'form': form})
        else:
            logger.error('No controller or mac was included on controller query params')
            form = SignupForm()
            return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        print('post')
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # radius_auth = requests.post('http://192.168.1.41:8002',
            #                             {'auth_user': username, 'auth_pass': raw_password, 'accept': 'Continue'})
            if user is not None:
                return HttpResponse(200)
        else:
            #print(request.session)
            return render(request, 'sign_up.html', {'form': form})


class RequestAnalyser():
    def coovachilli_login(request):
        if 'controller_id' in request.GET and 'mac' in request.GET:
            return True
        else:
            return False

    def coovachilli_signup(request):
        if 'controller_id' in request.session and 'mac' in request.session:
            return True
        else:
            return False

    def coovachilli_has_session(request):
        if 'template_name' in request.session:
            return True
        else:
            return False

    def coovachilli_from_openwrt(request): #coova can be from openwrt or from normal coova on a sistem
        if 'loginurl' in request.GET:
            return False
        else:
            return True


class PortalLogin(View):
    def get(self, request):
        request_well_formed = False
        request_has_session = False
        coova_from_openwrt = False

        coova_from_openwrt = RequestAnalyser.coovachilli_from_openwrt(request)

        if coova_from_openwrt:
            query_params = request.GET
        else:
            parsed = urlparse.urlparse(request.GET['loginurl'])
            query_params = urlparse.parse_qs(parsed.query)

        request_has_session = RequestAnalyser.coovachilli_has_session(request)

        if request_has_session:
            form = LoginForm()
            del request.session['template_name']
            request.session['template_name'] = 'login'
            return render(request, 'login.html', {'form': form, })

        request_well_formed = RequestAnalyser.coovachilli_login(request)

        if request_well_formed:
            controller = Controller.objects.filter(uuid=query_params['controller_id'])
            if controller:
                controller = controller[0]
                Device.objects.register_device(mac=query_params['mac'],
                                               user_agent=request.META['HTTP_USER_AGENT'])

                request.session['controller_id'] = query_params['controller_id']
                request.session['controller_model_name'] = \
                    constants.ControllersTypes.choices[controller.controller_model - 1][1]
                request.session['controllers_types'] = constants.ControllersTypes.choices
                request.session['mac'] = query_params['mac']
                request.session['controller_ip'] = query_params['uamip']
                request.session['redirect_url'] = controller.redirect_url
                request.session['template_name'] = 'login'
                print(request.session['controller_ip'])
                form = LoginForm()
                return render(request, 'login.html', {'form': form,})
            else:
                logger.warning('No controller was found for uuid: %s', query_params['controller_id'])
                form = LoginForm()
                return render(request, 'login.html', {'form': form})
        else:
            logger.error('No controller or MAC was included on login request query params')
            form = LoginForm()
            return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        print('post boy')
        print(form)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('auth_user')
            raw_password = form.cleaned_data.get('auth_pass')
            user = authenticate(request, username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend)')
            print(user)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponse(200)

            else:
                return HttpResponse("O usuário não existe ou a senha está incorreta.", status=404)
        else:
            return redirect('http://g1.globo.com')

    def home(self, request):
        return render(request, 'home.html')


class PortalLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/portal/login/')