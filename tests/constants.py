from djchoices import DjangoChoices, ChoiceItem

CONTROLLERS = {
    'swarm': {
        'controller_name' : 'Elcoma Networks - Swarm',
        'username_placeholder': 'auth_user',
        'password_placeholder': 'auth_pass',
        'submit_button_name': 'login',
        'action': None, #por aqui esta None pois mode mudar dependendo do ip da swarm do cliente,
        'controller_id' : 1
    },
    'aerohive': {
        'controller_name' : 'Aerohive Networks - Aerohive',
        'username_placeholder': 'username',
        'password_placehoder': 'password',
        'submit_button_name': 'login',
        'action': 'http://1.1.1.1',
    },
    'coovachilli' : {
        'controller_name' : 'Elcoma Networks - CoovaChilli',
    }
}

user_agent_mandatory_string = 'Mozilla/5.0'

#
# {
# "name":"John",
# "age":30,
# "cars":[ "Ford", "BMW", "Fiat" ]
# }

coova_options_json_model = "utilize o formato {key: value, key:value} onde key sao options do coova chilli, ex:{\n\
'radiusserver1' : 10.1.1.1,\n 'radiusserver2' : 192.168.1.1, \ndhcpif : 'br-lan'}"


class ControllersTypes(DjangoChoices):
    swarm = ChoiceItem(1)
    aerohive = ChoiceItem(2)
    coovachilli = ChoiceItem(3)