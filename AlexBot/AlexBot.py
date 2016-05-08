#coding:cp1251
import wolframalpha      
import vk
import requests
import pickle
import random
import re
import time
import datetime
import flickr
from random_words import RandomWords
def auth_vk(id, login, passwd, scope):
    session = vk.AuthSession(app_id=id, user_login=login, user_password=passwd, scope=scope)
    return vk.API(session, v='5.50')

def send_mesg(who, text):
    attach=re.findall('{\w*\S*\w*}', text)
    if(len(attach) != 0):
        bot.messages.send(peer_id=who, message=re.sub('{\w*\S*\w*}', "", text), random_id=random.randint(0, 200000), attachment=attach[0][1:-1])
    else:
        bot.messages.send(peer_id=who, message=text, random_id=random.randint(0, 200000))


   
def init_simple_command():
    file = open('simple_command.db', 'rb')
    simple_command = pickle.load(file)
    file.close()
    return simple_command
def init_home_work_db():
    file = open('home_work.db', 'rb')
    hw = pickle.load(file)
    file.close()
    return hw

def add_simple_command(mesg):
   if(len(mesg) >= 3):  
       simple_command[mesg[1]] = " ".join(mesg[2:])
       file = open('simple_command.db', 'wb')
       pickle.dump(simple_command, file)
       file.close()
def send_list(who):
    send_mesg(who, "������ ������:" + "\n" +"\n".join(simple_command.keys()))
#�������� �������� - ����� �� ������� "���������"
def wolfram_send(who, mesg):
    bot.messages.send(peer_id=who, message="������...", random_id=random.randint(0, 200000))
    res = wf_client.query(" ".join(mesg[1:]), "")
    for pod in res.pods:
        if(pod.scanner == 'Derivative'):
            bot.messages.send(peer_id=who, message="���������� ����������� ������ �������. ��������...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'Input__Step-by-step solution')
            break
        if(pod.scanner == 'ODE'):
            bot.messages.send(peer_id=who, message="���������� ����������� ������ �������. ��������...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'DifferentialEquationSolution__Step-by-step solution')
            break
        if(pod.scanner == 'Integral'):
            bot.messages.send(peer_id=who, message="���������� ����������� ������ �������. ��������...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'IndefiniteIntegral__Step-by-step solution')
            break
        if(pod.scanner == 'Integral'):
            bot.messages.send(peer_id=who, message="���������� ����������� ������ �������. ��������...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'IndefiniteIntegral__Step-by-step solution')
            break
    i=0
    for pod in res.pods:
        k=0
        for subpod in pod:
            p = requests.get(subpod.img)
            out = open("img.jpg", "wb")
            out.write(p.content)
            out.close()
            img = {'photo': ('img.jpg', open(r'img.jpg', 'rb'))}
            # �������� ������ ��� �������� �����������
            response = bot.photos.getMessagesUploadServer()
            upload_url = response['upload_url']

            # ��������� ����������� �� url
            response = requests.post(upload_url, files=img)
            result=response.json()

            # ��������� ���� �� ������� � �������� id
            photo1=result['photo'] 
            hash1=result['hash'] 
            server1=result['server']
            if(photo1 != '[]'):
                response = bot.photos.saveMessagesPhoto(server=server1, photo=photo1,   hash=hash1) 
                attach="photo"+str(response[0]['owner_id'])+"_"+str(response[0]['id'])
                bot.messages.send(peer_id=who, message=res.pods[i].title, random_id=random.randint(0, 200000), attachment=attach)
            time.sleep(0.5)
            k+=1
            if(k == int(pod.numsubpods)):
                break
        i+=1
def add_home_work(id, text):
    hw={"id":id, "subject": text[1], "date": datetime.datetime.strptime(text[2], "%d.%m.%y").date()}
    home_work_base.append(hw)
    file = open('home_work.db', 'wb')
    pickle.dump(home_work_base, file)
    file.close()
def find_hw(who, text):
    if (len(text) == 1):
        for hw in home_work_base:
            if (hw["date"]==datetime.datetime.today().date().replace(day=datetime.datetime.today().day+1)):
                bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=hw["id"])
                time.sleep(0.4)
        return
    if ((len(text) == 2) and (text[1]=="���")):
        for hw in home_work_base:
            bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=hw["id"])
            time.sleep(0.4)
        return
    if (len(text) == 2):
        for hw in home_work_base:
            if(hw["subject"]==text[1]):
                bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=hw["id"])
                time.sleep(0.4)
        return
    
    if ((len(text) == 3) and (text[1]=="���")):
        for hw in home_work_base:
            if (hw["date"] == datetime.datetime.strptime(text[2], "%d.%m.%y").date()):
                bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=hw["id"])
                time.sleep(0.4)
        return
    if (len(text) == 3):
        for hw in home_work_base:
            if ((hw["date"] == datetime.datetime.strptime(text[2], "%d.%m.%y").date()) and (hw["subject"] == text[1])):
                bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=hw["id"])   
                time.sleep(0.4)    
        return
    bot.messages.send(peer_id=who, message="������������ ������!", random_id=random.randint(0, 200000))

def generate_post(who):
    rw = RandomWords()
    bot.messages.send(peer_id=who, message="������������� ����, �����(��� ����� ���� ������, � ����� �����. ������������������ ���������, ����� ��� � ������������ ����...)", random_id=random.randint(0, 200000))
    """p = requests.get("https://unsplash.it/900/600/?random")"""

    word = rw.random_word()
    url = flickr.get_random_img(word)
    p = requests.get(url)
    out = open("random.jpg", "wb")
    out.write(p.content)
    out.close()

    img = {'photo': ('img.jpg', open(r'random.jpg', 'rb'))}
    # �������� ������ ��� �������� �����������
    response = bot.photos.getMessagesUploadServer()
    upload_url = response['upload_url']

    # ��������� ����������� �� url
    response = requests.post(upload_url, files=img)
    result=response.json()

    # ��������� ���� �� ������� � �������� id
    photo1=result['photo'] 
    hash1=result['hash'] 
    server1=result['server']
    

    trigger=0
    while(trigger == 0):
        list_id=str(random.randint(5000, 363720000))
        for i in range(0,9):
            list_id= list_id +","+ str(random.randint(5000, 363720000) )
        ownerid=bot.execute.get_audioid(list=list_id)
        if(ownerid !=0): 
            trigger = 1
               

    list_audio=bot.audio.get(owner_id=ownerid[0], count=ownerid[1])
    num=random.randint(0, list_audio["count"]-1)
    try:
        audioid=list_audio["items"]
        audioid=audioid[num]
        audioid=audioid["id"]
    except IndexError:
        print("Index!")
        audioid=list_audio["items"]
        audioid=audioid[ownerid[1]-num-1]
        audioid=audioid["id"]
    text = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=text&lang=ru")
    if(photo1 != '[]'):
        response = bot.photos.saveMessagesPhoto(server=server1, photo=photo1,   hash=hash1) 
        attach="photo"+str(response[0]['owner_id'])+"_"+str(response[0]['id'])+",audio"+str(ownerid[0])+"_"+str(audioid)
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000),message=text.text, attachment=attach)

    

    

def main():
    global bot
    global wf_client
    global simple_command
    global home_work_base
    simple_command={}
    home_work_base=[]
    home_work_base=init_home_work_db()
    simple_command=init_simple_command()
    bot = auth_vk('5419077', "89851906212", "dicks228", 'wall,messages,photos,audio')
    print("Ready!")
    wf_client = wolframalpha.Client("KW45EP-XHU7PVPVTX")
    error_message="���! ��� �� ����� �� ���... �� ����� ��� �������! ���������� ��������� ������. ���� ��� ������ ���������� ���������, ����������, ��������� � vk.com/id96494615 ��� ���������� ���������"
    while (True):
        try:
            poll = bot.messages.getLongPollServer()
            r = requests.request("GET","http://"+poll['server']+"?act=a_check&key="+poll['key']+"&ts="+str(poll['ts'])+"&wait=25&mode=2", timeout = 50)
            mesg_poll=r.json()
        except Exception:
            print("Error")
            time.sleep(4)
            poll = bot.messages.getLongPollServer()
            continue
        for mesg in mesg_poll['updates']:
            if (mesg[0] != 4):
                continue
            if (mesg[6].split(" ")[0] == "/������"):
                try:
                    send_list(mesg[3])
                    continue    
                except Exception:
                   print("������ ��� �������� ������") 
                   bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                   continue     
            if (mesg[6].split(" ")[0] == "/��������"):
                try:
                    add_simple_command(mesg[6].split(" "))
                    continue
                except Exception:
                    print("������ ��� ���������� �������")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/wolfram"):
                try:
                    wolfram_send(mesg[3], mesg[6].split(" "))
                    continue
                except Exception:
                    print("��������� ������ � ���������")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
                
            if (mesg[6].split(" ")[0] == "/��������_��"):
                try:
                    add_home_work(mesg[1], mesg[6].split(" "))
                    continue
                except Exception:
                    print("������ ��� ���������� ��")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/��"):
                try:
                    find_hw(mesg[3], mesg[6].split(" "))
                    continue
                except Exception:
                    print("������ ��� ������ ��")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/����"):
               try:
                    generate_post(mesg[3])
                    continue
               except Exception:
                    print("������ ��� ��������� �����")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
                
            if (mesg[6] in simple_command):
                try:
                    send_mesg(mesg[3], simple_command[mesg[6]])
                    continue

                except Exception:
                    print("������ ��� �������� �������")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue


            

if (__name__ == "__main__"):
    main()