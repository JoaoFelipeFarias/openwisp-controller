import requests
import datetime
import urllib.parse as urlparse
import logging

from django.db.models import Q

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import logout
from portal.forms import SignupForm, LoginForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from portal.models import Controller, PortalDevice, CoovaDevice, OpenWispDevice, ConnectionTable
from openwisp_controller.config.models import *
from radius.models import Radacct, Radcheck, Radreply
from tests import constants
# Create your views here.

from django.template.defaulttags import register
from portal.serializers import serializers as portal_serializers
from rest_framework import routers, serializers, viewsets


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
        #print(request.session['template_name'])
        is_coova_login = False
        is_coova_login = RequestAnalyser.coovachilli_signup(request)

        if not is_coova_login:
            logger.warning('its not a coova login, attempting to register user anyway')
            form = SignupForm()
            return render(request, 'sign_up.html', {'form': form})
        else:
            controller = Controller.objects.filter(uuid=request.session['controller_id'])
            if controller:
                controller = controller[0]
                #Device.objects.register_device(mac=request.session['mac'],
                #                               user_agent=request.META['HTTP_USER_AGENT'])
                request.session['controller_id'] = request.session['controller_id']
                request.session['controller_model_name'] = \
                    constants.ControllersTypes.choices[controller.controller_model - 1][1]
                request.session['controllers_types'] = constants.ControllersTypes.choices
                request.session['controller_ip'] = request.session['controller_ip']
                request.session['redirect_url'] = controller.redirect_url
                request.session['template_name'] = 'sign_up'
                print(request.session['template_name'])
                form = SignupForm()
                return render(request, 'sign_up.html', {'form': form})
            else:
                logger.warning('No controller was found for uuid: %s', request.session['controller'])
                form = SignupForm()
                return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        logger.warning('post was sent')
        logger.warning(form.is_valid())
        if form.is_valid():
            logger.warning('form is valid!')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.warning(user)
            # radius_auth = requests.post('http://192.168.1.41:8002',
            #                             {'auth_user': username, 'auth_pass': raw_password, 'accept': 'Continue'})
            if user is not None:
                logger.warning('user conseguiu logar depois de se registar')
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

        logger.warning(query_params)

        request_has_session = RequestAnalyser.coovachilli_has_session(request)

        request_well_formed = RequestAnalyser.coovachilli_login(request)

        logger.warning('is request well formed??? ' + str(request_well_formed))

        if request_well_formed:

            controller = Controller.objects.filter(uuid=query_params['controller_id'])
            if controller:
                controller = controller[0]
                #Device.objects.register_device(mac=query_params['mac'],
                #                               user_agent=request.META['HTTP_USER_AGENT'])
                called = query_params['called']
                logger.warning(called)
                coova_device = CoovaDevice.search_for_openwisp_device(mac=called,controller=controller)


                request.session['controller_id'] = query_params['controller_id']
                request.session['controller_model_name'] = \
                    constants.ControllersTypes.choices[controller.controller_model - 1][1]
                print(request.session['controller_model_name'])
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
            logger.warning(user)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                #ConnectionTable.objects.create(user=user, mac=request.session['mac'], remaining_time_seconds=0, client=request.session)

                return HttpResponse(200)

            else:
                return HttpResponse("O usuário não existe ou a senha está incorreta.", status=404)
        else:
            return redirect('http://g1.globo.com')

    def home(self, request):
        return render(request, 'home.html')

class CoovaManagerView(View):
    def get(self, request):
        #from django.core import serializers
        #data = serializers.serialize("python", CoovaDevice.objects.all(), fields=('name', 'mac_address', 'last_ip'))

        serializer = portal_serializers.CoovaDeviceSerializer(CoovaDevice.objects.all(), many=True)

        for item in serializer.data:
            logger.warning("serializer data")
            logger.warning(item['openwisp_device']['last_ip'])

        return render(request, 'coovamanager.html', {'data': serializer.data })

class ElcomaCoovaManager(View):
    def get(self, request):
        coova_from_openwrt = RequestAnalyser.coovachilli_from_openwrt(request)
        request_has_session = RequestAnalyser.coovachilli_has_session(request)
        request_well_formed = RequestAnalyser.coovachilli_login(request)
        data = {}

        if coova_from_openwrt:
            query_params = request.GET
        else:
            parsed = urlparse.urlparse(request.GET['loginurl'])
            query_params = urlparse.parse_qs(parsed.query)

        # todo: fix the if else for request well formed and controller check
        if request_well_formed:
            controller = Controller.objects.filter(uuid=query_params['controller_id'])

            if controller:
                controller = controller[0]

                urlparams = ''
                for parameter in request.GET:
                    urlparams = urlparams + '&' + parameter + '=' + request.GET[parameter]
                urlparams = urlparams[1:]
                urlparams = '?' + urlparams
                print(urlparams)

                request.session['controller_ip'] = query_params['uamip']
                request.session['redirect_url'] = controller.redirect_url
                request.session['urlparams'] = urlparams

                #searching for mac on table:
                print(query_params['mac'])
                rad_acct_obj = Radacct.objects.filter(callingstationid=query_params['mac'],
                                                      acctterminatecause=None)
                print('printando os rad_acct para o MAC')
                print(rad_acct_obj)
                rad_last_null_obj = rad_acct_obj.order_by('-radacctid')
                print('printando todos os rad_acct que são None ou string vazia ')
                print(rad_last_null_obj)
                # for ob in rad_last_null_obj:
                #     if ob.acctterminatecause == '':
                #         print('vazio')
                #     elif ob.acctterminatecause == None:
                #         print('None')
                #     else:
                #         print('alguma coisa')

                # if there is no terminate cause, meaning NULL on acctterminatecause, check if last connection has a
                # time difference bigger than the first Radreply with 'Session-Timeout' of that user. That means that
                # more time has passed than allowed for his session time out and he should not be allowed. Otherwise,
                # login the user returning the html witch will communicate with coova.
                rad_acct_obj = rad_last_null_obj
                print(rad_acct_obj[0].acctterminatecause)
                print('id é ' + str(rad_acct_obj[0].radacctid))

                if rad_acct_obj[0].acctterminatecause == '' or \
                        rad_acct_obj[0].acctterminatecause == None:
                    print('is null')

                    print(rad_acct_obj[0].acctstarttime)
                    time_of_last_acct_record = datetime.datetime.fromtimestamp(rad_acct_obj[0].acctstarttime)
                    print(time_of_last_acct_record.strftime("%c"))
                    now = datetime.datetime.now()
                    delta = (now - time_of_last_acct_record).total_seconds()

                    print(rad_acct_obj[0].username)

                    radreply_for_user = Radreply.objects.filter(username=rad_acct_obj[0].username,
                                                                    attribute='Session-Timeout')

                    # if there is radreply for user, compare with value from first Session-Timeout Insert
                    print(radreply_for_user)
                    print(delta)
                    if radreply_for_user:
                        session_time_for_user = radreply_for_user[0].value
                        print(session_time_for_user)
                        if delta > int(session_time_for_user):
                            print('delta is bigger than session_time for user, redirecting to login page')
                            data['login_coova'] = False
                            #return redirect('/portal/login/', request=request)
                            return render(request, 'elcomacoovamanager.html', {'data': data})
                        else:
                            print(delta)
                            data['username'] = rad_acct_obj[0].username
                            data['password'] = 'vagamesh'
                            data['login_coova'] = True
                            print(data)
                            return render(request, 'elcomacoovamanager.html', {'data': data})

                    # if there is no radreply for user, compare with default coova session time - 14400 sec
                    elif delta > 14400:
                        data['login_coova'] = False
                        print('delta is bigger than default coova delta time, redirecting to login page')
                        #return redirect(reverse('portal_login') + urlparams)
                        return render(request, 'elcomacoovamanager.html', {'data': data})

                    else:
                        data['username'] = rad_acct_obj[0].username
                        data['password'] = 'vagamesh'
                        data['login_coova'] = True
                        print('delta is lower than 14400, trying to login')
                        # return redirect('/portal/login/', request=request)
                        return render(request, 'elcomacoovamanager.html', {'data': data})


                else:
                    data['login_coova'] = False
                    print('there is a RadAcct with something on terminate cause, redirecting to login page')
                    #return redirect('/portal/login/', request=request)
                    return render(request, 'elcomacoovamanager.html', {'data': data})


class PortalLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/portal/login/')

