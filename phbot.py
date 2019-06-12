import telebot, phh, requests
from urllib.parse import unquote


userStep = {}
knownUsers = []
userUrl = {}
bot = telebot.TeleBot('885843885:AAEn6WXEsvgZwoi7eNp8GkocdDh8sN-D07c')


def bitly(url):
    session = requests.Session()
    r = session.get('https://bitly.com/')
    xsrf = r.cookies.get_dict()['_xsrf']
    cookie = '_xsrf='+xsrf
    headers = {'cookie':cookie, 'x-xsrftoken':xsrf}
    r = requests.post('https://bitly.com/data/shorten', data = {'url':url}, headers = headers)
    link = r.json()['data']['anon_shorten']['link']
    return link


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0


@bot.message_handler(commands=['start', 'help'])
def command_start(m):
    cid = m.chat.id
    get_user_step(cid)
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.reply_to(m, "Hi. Send me command /get or /ph if you want get direct link")
    else:
        bot.reply_to(m, "Hi. Send me command /get or /ph if you want get direct link")



#######PH#########
@bot.message_handler(commands=['ph', 'get'])
def command_ph(m):
    cid = m.chat.id
    bot.reply_to(m, "Send me PornHub video link")  # show the keyboard
    userStep[cid] = 1

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def get_url_ph(m):
    cid = m.chat.id
    userUrl[cid] = [m.text]
    bot.send_chat_action(cid, 'typing')
    try:
        res = phh.get(m.text)
        userUrl[cid].append(res)
        quals = res['qualitys']
        quals_string = ''
        for i in quals:
            quals_string += i+'\n'
        bot.reply_to(m, '''Choose quality:
{}'''.format(quals_string))
        userStep[cid] = 2
    except:
        bot.reply_to(m, 'Sorry, but the link is incorrect: (')
        userStep[cid] = 1
    

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def get_qua_ph(m):
    cid = m.chat.id
    userUrl[cid].append(m.text)
    bot.send_chat_action(cid, 'typing')
    url = userUrl[cid][0]
    res = userUrl[cid][1]
    qua = userUrl[cid][2].replace('p', '')+'p'
    dur = res['duration']
    if 3600 <= dur:
        dur /= 3600
        dur = str(round(dur, 1))+' hr'
    elif 60 <=dur:
        dur /= 60
        dur = str(round(dur, 1))+' min'
    else: dur = str(dur)+' sec'
    try:
        url = res['videos'][qua]
        title = res['title']
        size = float(requests.head(url).headers['Content-Length'])
        if size > 1.024e+9:
            size /= 1.024e+9
            size = str(round(size, 1))+'GB'
        elif 1e+6 <= size < 1.024e+9:
            size /= 1.024e+6
            size = str(round(size, 1))+'MB'
        elif 1000 <= size < 1e+6:
            size /= 1000
            size = str(round(size, 1))+'KB'
        elif size < 1000:
            size = str(size)+'B'
        bot.reply_to(m, '''Title: {}
Direct link: {}
Shorten link: {}
Duration: ≈ {}
Size: {}'''.format(title, url, bitly(url), dur, size))
        userStep[cid] = 1
    except:
        bot.reply_to(m, 'Error :(')
        userStep[cid] = 1
#####PH########


bot.polling(none_stop=False)
