from flask import Flask, request, abort
import requests
import json
import random
from project.Config import *
from uncleengineer import thaistock

app = Flask(__name__)
chat_state = {"userid":"id"}
ans_state = {"userid":"ans"}
index = 1
Q=['',
'https://res.cloudinary.com/velody750/image/upload/v1579667082/samples/VPuzzle/1_vsxw5v.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667082/samples/VPuzzle/2_pof9i8.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/3_judc9j.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/4_gdv5gu.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/5_takj1a.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/6_bcxyxn.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/7_h17ooq.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667082/samples/VPuzzle/8_atlhyf.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667082/samples/VPuzzle/9_r3gm2q.jpg',
'https://res.cloudinary.com/velody750/image/upload/v1579667083/samples/VPuzzle/10_tkilrn.jpg']
ANS=['',"ตาราง","รองเท้า","คนสำคัญ","ฝรั่งเศส","อินทริเกต","กลศาสตร์","สยามพารากอน","เนตรนารี","ดัชนีหักเห","ส่วนเบี่ยงเบนมาตรฐาน"]

#Q1 = ["https://drive.google.com/file/d/1qINPCg7qcIL0tBezJP_3L73TuLroSNI7/view?usp=sharing"]
#Q1_follow = ["","","เท่าไหร่","มีเท่าไหร่","ทั้งหมดเท่าไหร่","มีทั้งหมดเท่าไหร่"]

def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE




@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(payload)
        user = payload["events"][0]['source']['userId']
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if(user not in chat_state):
            chat_state[user]=0
            ans_state[user]=1
        if chat_state[user] == 0:
            ReplyImage(Reply_token,1,Channel_access_token,user)
            chat_state[user] = 1
       
        elif chat_state[user] == 1:
            if message == ANS[ans_state[user]] :
                Reply_messasge = "ถูกต้องงงง พร้อมสำหรับข้อต่อไปหรือยัง (press any key to the next question)"
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                chat_state[user] = 2
            
                
            
            elif message != ans_state[user] :
                Reply_messasge = "ผิดจ้า ลองตอบใหม่นะ"
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif chat_state[user] == 2:
            ans_state[user]+=1
            ReplyImage(Reply_token,ans_state[user],Channel_access_token,user)
            chat_state[user] = 1


        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200


@app.route('/')
def hello():
    return 'hello world bok',200

def ReplyImage(Reply_token, Index, Line_Acees_Token,user):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            'type': "image",
            'originalContentUrl': Q[ans_state[user]] ,
            'previewImageUrl': Q[ans_state[user]]
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200
def game():
    
    index2 = random.randint(1,10)
    
    return Q1[0]+" " , index2