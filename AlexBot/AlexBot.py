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
        bot.messages.send(peer_id=who, message=re.sub('{\w*\S*\w*}', "", text), random_id=random.randint(0, 200000), attachment=attach[1][1:-1])
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

def generate_post(who):
    bot.messages.send(peer_id=who, message="Подгатавливаю пост, ждите(это может быть быстро, а может долго. Производительность рандомная, также как и генерируемый пост...)", random_id=random.randint(0, 200000))
    p = requests.get("http://loremflickr.com/900/600/all")
    out = open("random.jpg", "wb")
    out.write(p.content)
    out.close()

    img = {'photo': ('img.jpg', open(r'random.jpg', 'rb'))}
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
    

    count=0

    while(count == 0):
        try:
            ownerid=random.randint(5000, 363720000)
            count=bot.audio.getCount(owner_id=ownerid)
            time.sleep(0.1)
        except 6:
                    print("Запросы")
                    time.sleep(0.8)
                    continue

        

    list_audio=bot.audio.get(owner_id=ownerid)
    num=random.randint(0, count)
    audioid=list_audio["items"]
    audioid=audioid[num]
    audioid=audioid["id"]
    if(photo1 != '[]'):
        response = bot.photos.saveMessagesPhoto(server=server1, photo=photo1,   hash=hash1) 
        attach="photo"+str(response[0]['owner_id'])+"_"+str(response[0]['id'])+",audio"+str(ownerid)+"_"+str(audioid)
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), attachment=attach)

    

    

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
    error_message="Упс! Что то пошло не так... Ты опять все поломал! Попробуйте повторить запрос. Если эта ошибка происходит постоянно, пожалуйста, свяжитесь с vk.com/id96494615 для устранения проблеммы"
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
            if (mesg[6].split(" ")[0] == "/список"):
                try:
                    send_list(mesg[3])
                    continue    
                except Exception:
                   print("Ошибка при отправке списка") 
                   bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                   continue     
            if (mesg[6].split(" ")[0] == "/добавить"):
                try:
                    add_simple_command(mesg[6].split(" "))
                    continue
                except Exception:
                    print("Ошибка при добавлении команды")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/wolfram"):
                try:
                    wolfram_send(mesg[3], mesg[6].split(" "))
                    continue
                except Exception:
                    print("Очередной пиздец в вольфраме")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
                
            if (mesg[6].split(" ")[0] == "/добавить_дз"):
                try:
                    add_home_work(mesg[1], mesg[6].split(" "))
                    continue
                except Exception:
                    print("Ошибка при добавлении дз")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/дз"):
                try:
                    find_hw(mesg[3], mesg[6].split(" "))
                    continue
                except Exception:
                    print("Ошибка при выводе дз")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/пост"):
                try:
                    generate_post(mesg[3])
                    continue
                except IndexError:
                    print("Индекс")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
                
            continue
            if (mesg[6] in simple_command):
                try:
                    send_mesg(mesg[3], simple_command[mesg[6]])
                    continue
                except Exception:
                    print("Ошибка при отправке команды")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue


            

if (__name__ == "__main__"):
    main()