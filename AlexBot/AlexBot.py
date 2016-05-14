#coding:cp1251
import wolframalpha      
import vk
import requests
import shelve
import pickle
import random
import re
import time
import datetime
import flickr
from random_words import RandomWords
import wikipedia
import multiprocessing
from notice import *
from time import mktime
import parsedatetime
import shelve
import datetime
import json

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
def get_audio_user():
    trigger=0
    while(trigger == 0):
        list_id=str(random.randint(5000, 363720000))
        for i in range(0,9):
            list_id= list_id +","+ str(random.randint(5000, 363720000) )
        ownerid=bot.execute.get_audioid(list=list_id)
        if(ownerid !=0): 
            trigger = 1
    return ownerid
def get_random_audio(number):
    result=""
    k=0
    need_num=number
    while(k != number):
        ownerid=get_audio_user()
        list_audio=bot.audio.get(owner_id=ownerid[0], count=ownerid[1])
        count=list_audio["count"]
        need_num=number-k
        if(need_num > count): 
            need_num=int(count/2)
            while(need_num !=0):
                audioid=list_audio["items"]
                audioid=audioid[need_num-1]
                audioid=audioid["id"]
                if (k == 0):
                    result=result+"audio"+str(ownerid[0])+"_"+str(audioid)
                    need_num-=1
                    k+=1
                else:
                    result=result+",audio"+str(ownerid[0])+"_"+str(audioid)
                    need_num-=1
                    k+=1
        else: 
            need_num= number-k
            while(need_num !=0):
                num=random.randint(0, count)
                try:
                    audioid=list_audio["items"]
                    audioid=audioid[num]
                    audioid=audioid["id"]
                except IndexError:
                    print("Index!")
                    continue
                if (k == 0):
                    result=result+"audio"+str(ownerid[0])+"_"+str(audioid)
                    need_num-=1
                    k+=1
                else:
                    result=result+",audio"+str(ownerid[0])+"_"+str(audioid)
                    need_num-=1
                    k+=1
        time.sleep(0.5)
    return result

def add_task(who, out, x):
    jobs_base=shelve.open('jobs.db')
  #  c = parsedatetime.Constants(localeID="ru_RU", usePyICU=False)
    cal = parsedatetime.Calendar()
    time1, parse_status = cal.parse(x)
    time1=datetime.datetime.fromtimestamp(mktime(time1)).strftime('%a %b %d %H:%M %Y')
    jobs_base[time1]=[send_mesg, {"who":who, "text":"[!Напоминание!] "+out}]
    send_mesg(who, "Я напомню вам: "+"'"+out+"'. "+ "Дата: " + time1)
    jobs_base.close()

def set_notice(who, mesg):
        get = mesg
        text = get+' ' # добавляем в конец пробел, чтобы отрабатывать уведомления типа "напомнить мне через 10 минут". Если бы пробела не было, параметр clock был бы пуст. В параметре clock после слова "час" тоже стоит пробел, чтобы различать поиск "час" и "часов".
        find = re.findall('ерез [0-9]+|В [0-9:-]+|в [0-9:-]+|ерез час',text)

        if get: # убеждаемся, заполнено ли поле ввода
            if find: # убеждаемся, указано ли время напоминания
                what = find[0].split()
                timex = what[1].replace('-',':').replace('час','1')

                if len(timex) > 2: # заменяет выражения типа "в 10" на "в 10:00"
                    time = timex
                else:
                    time = timex+':00'	
                
                whatdate, delwhatdate = get_datex(text)
                when, delday = get_day(text)
                how, delclock = get_clock(text)

                reps = {'ерез':'at now + %s %s' % (timex,how),'В':'at %s %s %s' % (time,when,whatdate),'в':'at %s %s %s' % (time,when,whatdate)}
                wors = {'Через %s %s' % (what[1],delclock):'','через %s %s' % (what[1],delclock):'','В %s ' % what[1]:'','в %s ' % what[1]:'', '%s' % delday:'', 'Через час':'', 'через час':'', '%s' % delwhatdate:'',} # какие слова мы будем удалять
                x = replace_all(what[0], reps) # это время, на которое запланировано появление напоминания
                out = replace_all(text, wors) # это текст напоминания

                add_task(who, out, x)
                
            else:
                return 0
        else:
            return 0

def generate_post(who, num, flag):
    if(len(num) > 1):
        if(int(num[1]) < 7):
            num = int(num[1])
        else: num = 1
    else: num = 1
    rw = RandomWords()
    if(flag == 0):
        bot.messages.send(peer_id=who, message="Подготавливаю пост, ждите(это может быть быстро, а может долго. Производительность рандомная, также как и генерируемый пост...)", random_id=random.randint(0, 200000))
    """p = requests.get("https://unsplash.it/900/600/?random")"""

    word = rw.random_word()
    url = flickr.get_random_img(word)
    p = requests.get(url)
    out = open("random.jpg", "wb")
    out.write(p.content)
    out.close()

    img = {'photo': ('img.jpg', open(r'random.jpg', 'rb'))}
    # Получаем ссылку для загрузки изображений
    if(flag == 0):
        response = bot.photos.getMessagesUploadServer()
    else: response = bot.photos.getWallUploadServer()
    upload_url = response['upload_url']

    # Загружаем изображение на url
    response = requests.post(upload_url, files=img)
    result=response.json()

    # Сохраняем фото на сервере и получаем id
    photo1=result['photo'] 
    hash1=result['hash'] 
    server1=result['server']
  
    text = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=text&lang=ru")
    if(photo1 != '[]'):
        if(flag == 0): 
            response = bot.photos.saveMessagesPhoto(server=server1, photo=photo1,   hash=hash1) 
        else: response = bot.photos.saveWallPhoto(user_id="360474541", server=server1, photo=photo1,   hash=hash1)
        attach="photo"+str(response[0]['owner_id'])+"_"+str(response[0]['id'])+","+get_random_audio(num)
        if(flag == 0):
            bot.messages.send(peer_id=who, random_id=random.randint(0, 200000),message=text.text, attachment=attach)
        else: bot.wall.post(owner_id="360474541", guid=random.randint(0, 200000),message=text.text, attachment=attach)

def send_wiki_info(who, text):
    answ=" ".join(text)
    if(answ[-1] == "?"): answ = answ[:-1]
    wikipedia.set_lang("ru")
    try:
        resp=wikipedia.summary(answ, sentences=6, chars=1, auto_suggest=False, redirect=True)
    except wikipedia.exceptions.DisambiguationError as error:
        resp=wikipedia.summary(error.options[0], sentences=6, chars=1, auto_suggest=False, redirect=True)
    except  wikipedia.exceptions.WikipediaException:
        resp=wikipedia.summary(answ, sentences=6, chars=0, auto_suggest=True, redirect=True)
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000),message=resp)

def send_random_audio(who, num):
    if(len(num) > 1):
        if(int(num[1]) < 7):
            num = int(num[1])
        else: num = 1
    else: num = 1
    list_id=get_random_audio(num)
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), attachment=list_id)

def get_timetable(group, mode):
    num_sem=2
    year_now=2016
    base1=requests.get("http://timetable.mephist.ru/getEvents.php?get=settings&rType=json")
    base1=base1.json()
    group=group.split("-")
    base_group=base1["groups"]
    for gr in base_group:
        if (gr["letter"] == group[0][0] and gr["num"] == group[1] and year_now-int(group[0][1:])/num_sem == int(gr["StartYear"])): 
            group_id = gr["id"]
    if (mode == "day"):
        start = datetime.datetime.today().date()
        end = start+datetime.timedelta(days=1)
        start_t = time.mktime(start.timetuple())
        end_t = time.mktime(end.timetuple())
    elif(mode == "week"):
        start=datetime.datetime.today().date() - datetime.timedelta(days=datetime.datetime.today().date().weekday())
        end = start+datetime.timedelta(days=7)
        start_t = time.mktime(start.timetuple())
        end_t = time.mktime(end.timetuple())
    timetable = requests.get("http://timetable.mephist.ru/getEvents.php?rType=json&start="+str(start_t)+"&end="+str(end_t)+"&groupId="+str(group_id)+"&tz=-180")
    timetable=timetable.json()
    return timetable

def send_timetable(who, mesg):
    if(len(mesg) == 2):
        timetable = get_timetable(mesg[1], "day")
        text = """
        _________________________
        Сегодня:
        _________________________\n"""
        for subj in timetable:
            text=text+"Предмет: "+ subj["title"]+"\n"
            text=text+"Преподователь: "+ subj["teachers"]+"\n"
            text=text+"Аудитория: "+ subj["auditories"]+"\n"
            text=text+"Тип занятия: "+ subj["type"]+"\n"
            text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
            text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
            text=text+"\n_________________________\n"
    elif(len(mesg)==3 and mesg[2]=="неделя"):
        timetable = get_timetable(mesg[1], "week")
        text = """
        _________________________
        Понедельник:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 0):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
        text =text+ """
        _________________________
        Вторник:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 1):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
        text =text+ """
        _________________________
        Среда:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 2):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
        text =text+ """
        _________________________
        Четверг:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 3):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
        text =text+ """
        _________________________
        Пятница:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 4):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
        text =text+ """
        _________________________
        Суббота:
        _________________________\n"""
        for subj in timetable:
            if(datetime.datetime.fromtimestamp(int(subj["start"])).weekday() == 5):
                text=text+"Предмет: "+ subj["title"]+"\n"
                text=text+"Преподователь: "+ subj["teachers"]+"\n"
                text=text+"Аудитория: "+ subj["auditories"]+"\n"
                text=text+"Тип занятия: "+ subj["type"]+"\n"
                text=text+"Начало занятия: "+ datetime.datetime.fromtimestamp(int(subj["start"])).strftime('%H:%M')+"\n"
                text=text+"Окончание занятия: "+ datetime.datetime.fromtimestamp(int(subj["end"])).strftime('%H:%M')+"\n"
                text=text+"\n_________________________\n"
    send_mesg(who, text)

def start_notice():
   global bot 
   bot = auth_vk('5419077', "89851906212", "dicks228", 'wall,messages,photos,audio')
   print("login 2")
   global jobs_base
   cur_time=datetime.datetime.now()
   while(True):
       jobs_base=shelve.open('jobs.db')
       for times in jobs_base:           
           if (times == datetime.datetime.now().strftime('%a %b %d %H:%M %Y')): 
              print(times)
              jobs_base[times][0](**jobs_base[times][1])
              del jobs_base[times]
       if(datetime.timedelta(hours=4) < (datetime.datetime.now()) - cur_time):
           jobs_base["post"][0](**jobs_base["post"][1])
           cur_time=datetime.datetime.now()
      # print(datetime.datetime.now()-cur_time)
       jobs_base.close()
   

def main():
    global bot
    global wf_client
    global simple_command
    global home_work_base
    jobs_base=shelve.open('jobs.db')
    jobs_base["post"]=[generate_post, {"who":360474541, "num":"1", "flag":1}]
    jobs_base.close()
    simple_command={}
    home_work_base=[]
    home_work_base=init_home_work_db()
    simple_command=init_simple_command()
    bot = auth_vk('5419077', "89851906212", "dicks228", 'wall,messages,photos,audio')
    print("Ready!")
    wf_client = wolframalpha.Client("KW45EP-XHU7PVPVTX")
    error_message="Упс! Что то пошло не так... Попробуйте повторить запрос. Если эта ошибка происходит постоянно, пожалуйста, свяжитесь с vk.com/id96494615 для устранения проблеммы"
    proc = multiprocessing.Process(target = start_notice)
    proc.start()
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
                    generate_post(mesg[3], mesg[6].split(" "), 0)
                    continue
               except Exception as error:
                    print("Ошибка при генерации поста")
                    time.sleep(1)
                    print(error)
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/ппост"):
               try:
                    generate_post(mesg[3], mesg[6].split(" "), 1)
                    continue
               except Exception as error:
                    print("Ошибка при генерации поста")
                    time.sleep(1)
                    print(error)
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/расписание"):
               try:
                    send_timetable(mesg[3], mesg[6].split(" "))
                    continue
               except Exception as error:
                    print("Ошибка при генерации поста")
                    time.sleep(1)
                    print(error)
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[:3] == ["Саныч,", "что", "такое"]):
              try:
                    send_wiki_info(mesg[3], mesg[6].split(" ")[3:])
                    continue
              except Exception:
                    print("Ошибка при запросе в вики")
                    bot.messages.send(peer_id=mesg[3], message="Что то тут не то... В википедии нет такой страницы, или произошла другая ошибка! Попробуйте еще раз!", random_id=random.randint(0, 200000))
                    continue   
            if (mesg[6].split(" ")[0] == "/песенки"):
               try:
                    send_random_audio(mesg[3], mesg[6].split(" "))
                    continue
               except Exception as error:
                    time.sleep(1)
                    print("Ошибка при отправке музыки")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    print(error)
                    continue         
            if (mesg[6].split(" ")[0] == "/напомнить"):
               try:
                    set_notice(mesg[3], mesg[6][11:])
                    continue
               except Exception as error:
                    time.sleep(1)
                    print("Ошибка при отправке добавлении напоминания!")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    print(error)
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