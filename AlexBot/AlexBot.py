#coding:cp1251
import wolframalpha      
import vk
import requests
import pickle
import random
import re
import time
import datetime
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
    send_mesg(who, "Список команд:" + "\n" +"\n".join(simple_command.keys()))
#гребаный вольфрам - вечер из разряда "потрачено"
def wolfram_send(who, mesg):
    bot.messages.send(peer_id=who, message="Считаю...", random_id=random.randint(0, 200000))
    res = wf_client.query(" ".join(mesg[1:]), "")
    for pod in res.pods:
        if(pod.scanner == 'Derivative'):
            bot.messages.send(peer_id=who, message="Обнаружена возможность выдачи решения. Ожидайте...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'Input__Step-by-step solution')
            break
        if(pod.scanner == 'ODE'):
            bot.messages.send(peer_id=who, message="Обнаружена возможность выдачи решения. Ожидайте...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'DifferentialEquationSolution__Step-by-step solution')
            break
        if(pod.scanner == 'Integral'):
            bot.messages.send(peer_id=who, message="Обнаружена возможность выдачи решения. Ожидайте...", random_id=random.randint(0, 200000))
            res = wf_client.query(" ".join(mesg[1:]), 'IndefiniteIntegral__Step-by-step solution')
            break
        if(pod.scanner == 'Integral'):
            bot.messages.send(peer_id=who, message="Обнаружена возможность выдачи решения. Ожидайте...", random_id=random.randint(0, 200000))
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
            # Получаем ссылку для загрузки изображений
            response = bot.photos.getMessagesUploadServer()
            upload_url = response['upload_url']

            # Загружаем изображение на url
            response = requests.post(upload_url, files=img)
            result=response.json()

            # Сохраняем фото на сервере и получаем id
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
    if ((len(text) == 2) and (text[1]=="все")):
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
    
    if ((len(text) == 3) and (text[1]=="все")):
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
    bot.messages.send(peer_id=who, message="Неправильный формат!", random_id=random.randint(0, 200000))

    

def main():
    global bot
    global wf_client
    global simple_command
    global home_work_base
    simple_command={}
    home_work_base=[]
    home_work_base=init_home_work_db()
    simple_command=init_simple_command()
    print("Enter login")
    login=input()
    print("Enter passwd")
    passwd=input()
    bot = auth_vk('5419077', login, passwd, 'wall,messages,photos')
    print("Ready!")
    wf_client = wolframalpha.Client("KW45EP-XHU7PVPVTX")
    while (True):
        try:
            poll = bot.messages.getLongPollServer()
            r = requests.request("GET","http://"+poll['server']+"?act=a_check&key="+poll['key']+"&ts="+str(poll['ts'])+"&wait=25&mode=2", timeout = 50)
        except Exception:
            print("Error")
            time.sleep(4)
            poll = bot.messages.getLongPollServer()
            continue

        for mesg in r.json()['updates']:
            if (mesg[0] != 4):
                continue
            if (mesg[6].split(" ")[0] == "/список"):
                send_list(mesg[3])
                continue           
            if (mesg[6].split(" ")[0] == "/добавить"):
                add_simple_command(mesg[6].split(" "))
                continue
            if (mesg[6].split(" ")[0] == "/wolfram"):
                wolfram_send(mesg[3], mesg[6].split(" "))
                continue
            if (mesg[6].split(" ")[0] == "/добавить_дз"):
                add_home_work(mesg[1], mesg[6].split(" "))
                continue
            if (mesg[6].split(" ")[0] == "/дз"):
                find_hw(mesg[3], mesg[6].split(" "))
                continue
            if (mesg[6] in simple_command):
                send_mesg(mesg[3], simple_command[mesg[6]])
                continue

   

if (__name__ == "__main__"):
    main()