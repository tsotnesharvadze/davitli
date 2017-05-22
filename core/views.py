# from django.shortcuts import render

import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import wolframalpha
from mtranslate.core import translate

from django.db.models import Q

from .models import QuestionMix,Question
#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAB1GgOpEzQBAIr3IqVHrcmZAtm1edVXO2Im2IZCt5y6ueTucOSgQXypgDoXy5bSRALy9jlPq2El11zbFFU93RfDBLm2F4uar6ZAVuNGH42L86OHZCk8BxsSuwZBibXpzlnv8luXeOGmvdVWLmqdq4tZClQLZAzCbZAQZBbTNSaWZAFQZDZD"
VERIFY_TOKEN = "mamasheni"

dicti1 = {'მოდული': 'absolute value of', 'უკვეცი': 'irreducible', 'ლოგარითმი': 'log',
 		'ინტეგრალი': 'integrate', 'სადაც': 'where', 'მნიშვნელობა': 'value', 'ნამდვილიდან ნამდვილ ცვლადშია': 'from real to real',
		'მეორე რიგის წარმოებული': 'second derivative', 'წარმოებული': 'derivative', 'მაქსიმალური მნიშვნელობა': 'maximum value',
 		'პი': 'pi', 'ციფრი': 'digit', 'ამოხსენი': 'solve', 'განსაზღვრული': 'definite', 'კონსტანტა': 'constant', 'განუსაზღვრელი': 'indefinite', 
		'დიფერენციალი': 'differential', 'ზღვარი': 'limit', 'უსასრულობა': '∞', 'გამოთვალე': 'calculate', 'მინიმალური მნიშვნელობა': 'minimum value'}

# Helper function
def post_facebook_message(fbid, recevied_message):
    # user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    # user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    # user_details = requests.get(user_details_url, user_details_params).json()

    if recevied_message == 'კითხვაარა':
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":'უი, მე მხოლოდ შემიძლია ტექსტის წაკითხვა'}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    elif recevied_message ==  369239263222822:
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
        response_msg = json.dumps({"recipient":{"id":fbid}, 'message': {'attachments': [{'payload': {'sticker_id': 369239263222822,
                                          'url': 'https://scontent.xx.fbcdn.net/v/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m&oh=51f7030fcdd99dc871819c84a847931f&oe=59B05CDC'},
                                                                'type': 'image'}],
                                                'mid': 'mid.$cAAFVWv8dBK1iXCbtpVcKuGWb0dL1',
                                                'seq': 1472925,
                                                'sticker_id': 369239263222822},
                                    'recipient': {'id': '298694183907664'},
                                    'sender': {'id': '1313880405374024'},
                                    'timestamp': 1495368050085,
                                    'text':'ლიქე ლიქე ლიქე'})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    else:
        
        app_id = '8LJR68-JKELEXKH5X'

        quest = recevied_message
        listi = quest.split(' ')

        for index,word in enumerate(listi) :
            if word in dicti1.keys():
                listi[index] = dicti1[word]



        quest = ' '.join(listi)


        trans =   translate(quest,'en','auto')


        client = wolframalpha.Client(app_id)
        res = client.query(trans)
        try:
            answer1 = ''
            for answer in res.results:
                answer1+=answer.text + '\n'
            # answer1 = next(res.results).text
            # if not ('(' in answer1 or '+' in answer1 or '=' in answer1) :
            pasuxi = translate(answer1,'ka','auto')
            try:
                pasuxi.replace('განუყოფელი','განუსაზღვრელი')
                pasuxi.replace('ინტეგრალური','ინტეგრალი')
            except:
                pass
            # else:
                # pasuxi = answer1
        
        except Exception as ge:
            pasuxi =  'უი, რაღაც ისე ვერაა ქე რო უნდა იყოს :/'
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":pasuxi}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},
        data=response_msg)
        pprint(status.json())

# Create your views here.
class Index(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    try:
                        message1 = message['message']['text']
                        ques = Q(question = message1) or Q(question__startswith = message1) or Q(question__icontains = message1)
                        msg = Question.objects.filter(ques)
                        pprint(msg)
                        if msg:
                            answ = msg.first().mix.answer_set.all().order_by('?').first().answer
                            post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
                            response_msg = json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":answ}})
                            status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
                            break
                        
                    except Exception as E:
                        pprint(E)
                        try:
                            message1 = message['message']['sticker_id']
                        except:
                            message1 = 'კითხვაარა'
                    post_facebook_message(message['sender']['id'], message1)    
        return HttpResponse() 



# "persistent_menu":[
#     { 
#       "locale":"default",
#       "composer_input_disabled":True, 
#       "call_to_actions":[  
#         {
#           "title":"My Account",
#           "type":"nested",
#           "call_to_actions":[
#             {
#               "title":"Pay Bill",
#               "type":"postback",
#               "payload":"PAYBILL_PAYLOAD"
#             },
#             {
#               "title":"History",
#               "type":"postback",
#               "payload":"HISTORY_PAYLOAD"
#             },
#             {
#               "title":"Contact Info",
#               "type":"postback",
#               "payload":"CONTACT_INFO_PAYLOAD"
#             }
#           ]
#         },
#         {
#           "type":"web_url",
#           "title":"Latest News",
#           "url":"http://petershats.parseapp.com/hat-news",
#           "webview_height_ratio":"full"
#         }
#       ]
#     },
#     {
#       "locale":"zh_CN",
#       "composer_input_disabled":False
#     }
#   ]