from database import voice_started, voice_ended, create_group_table, select_info, select_all, add_group, add_sub, del_sub, del_group
from datetime import datetime
from telebot import types
import logging.handlers, subprocess, configparser, logging, telebot, time, msgs, os

config = configparser.ConfigParser()
config.read('chatdevozbot.conf')

TOKEN = config['CHATDEVOZBOT']['TOKEN']
Channel = config['CHATDEVOZBOT']['CHANNEL']
CHATDEVOZ_LOG = config['CHATDEVOZBOT']['CHATDEVOZ_LOG']
ADMIN = ['creator', 'administrator']
COMMANDS = ['/iniciar', '/parar']

bot = telebot.TeleBot(TOKEN)

usuario = {}

logger_info = logging.getLogger('InfoLogger')
logger_info.setLevel(logging.DEBUG)
handler_info = logging.handlers.TimedRotatingFileHandler(CHATDEVOZ_LOG, when='midnight', interval=1, backupCount=7, encoding='utf-8')
logger_info.addHandler(handler_info)

markup_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_btn.row('/Participar')
markup_clean = types.ReplyKeyboardRemove(selective=False)

def log_text(message):
    logger_info.info(
        str(datetime.now()) +
        ' ' + str(message.chat.id) + ' \t' +
        str(message.message_id) + ' \t' + str(message.content_type)
    )

@bot.message_handler(commands=['iniciar'])
def bot_start(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.chat.id < 0:
        status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        group = select_info('ChatDeVoz', 'groupid', message.chat.id)
        if status in ADMIN:
            try:
                bot.send_message(message.from_user.id, msgs.start_admin, parse_mode='HTML')
                msg = bot.send_message(message.chat.id, msgs.start_group, parse_mode='HTML', reply_markup=markup_btn)
                if not group:
                    bot.pin_chat_message(message.chat.id, msg.message_id, disable_notification=True)
                    add_group(message.chat.id, message.from_user.id, msg.message_id)
                else:
                    del_group('ChatDeVoz', group[1])
                    add_group(message.chat.id, message.from_user.id, group[3])
            except:
                bot.send_message(message.chat.id, msgs.start_user_unstarted, parse_mode='HTML')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        # bot.send_message(message.chat.id, msgs.start_bot_not_admin, parse_mode='HTML')
        pass

@bot.message_handler(commands=['Participar'])
def bot_start(message):
    try:
        msg = bot.send_message(message.from_user.id, msgs.voice_start, parse_mode='HTML')
        usuario[message.from_user.id] = message.chat.id
    except:
        group = select_info('ChatDeVoz', 'groupid', message.chat.id)
        if group:
            msg = bot.send_message(message.chat.id, msgs.voice_group_send.format(message.from_user.id, message.chat.id), parse_mode='HTML', disable_web_page_preview=True)
            try:
                bot.delete_message(message.chat.id, group[2])
            except:
                pass
        # else:
            # bot.send_message(message.chat.id, msgs.voice_not_started_not_admin.format(message.from_user.id), parse_mode='HTML', disable_web_page_preview=True)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

@bot.message_handler(content_types=['voice_chat_ended'])
@bot.channel_post_handler(content_types=['voice_chat_ended'])
@bot.message_handler(commands=['parar'])
def bot_stop(message):
    log_text(message)
    try:
        if message.chat.id < 0:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if status in ADMIN:
                group = select_info('ChatDeVoz', 'groupid', message.chat.id)
                del_group('ChatDeVoz', group[1])
                bot.send_message(message.chat.id, msgs.stop_group, parse_mode='HTML', reply_markup=markup_clean)
                bot.unpin_chat_message(message.chat.id, message_id=group[3])
    except:
        pass
    groupid = 'g' + str(message.chat.id*-1)
    msg = select_info('Chats_de_Voz', 'groupid', groupid)
    if msg:
        try:
            voice_ended(msg[0])
            bot.delete_message(Channel, msg[2])
        except:
            pass
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=['voice', 'video_note'])
def get_voice_msg(message):
    if message.chat.id < 0:
        return 0
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        group = select_info('ChatDeVoz', 'groupid', str(usuario[message.from_user.id]))
        msg = msgs.voice_forwarded.format(
            str(usuario[message.from_user.id]).replace('-100', ''),
            group[2]
        )
        bot.forward_message(group[2], message.chat.id, message.message_id)
        usuario[message.from_user.id] = None
        bot.reply_to(message, msg, parse_mode='HTML', disable_web_page_preview=True)
    except:
        bot.reply_to(message, msgs.voice_not_forwarded, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def bot_start(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.split('@')[0] in COMMANDS:
        return 0
    if 'g100' in message.text:
        bot_notify(message)
    elif '-100' in message.text:
        msg = bot.send_message(message.from_user.id, msgs.voice_start, parse_mode='HTML')
        usuario[message.from_user.id] = message.text.replace('/start ', '')
    elif message.chat.id > 0:
        #bot.send_document(message.from_user.id, 'CgACAgEAAxkBAAPTYEexcA2G2cn6g2CdZS4MOVvm4ScAAhgBAAJhYUFGN48mu1WuJXMeBA')
        bot.send_message(message.from_user.id, msgs.start_user, parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['MeAvise'])
def bot_notify(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    if message.chat.id < 0:
        try:
            bot.send_chat_action(message.from_user.id, 'typing')
        except:
            bot.send_message(message.chat.id, msgs.start_user_unstarted, parse_mode='HTML')
            return 0
        groupid = 'g' + str(message.chat.id*-1)
    elif message.chat.id > 0 and 'start' in message.text:
        groupid = message.text.replace('/start ','')
    try:
        try:
            try:
                groupname = bot.get_chat(groupid.replace('g', '-')).title
            except:
                bot.send_message(message.from_user.id, msgs.not_in_group)
                return 0
            user = select_info(groupid, 'userid', message.from_user.id)
        except sqlite3.OperationalError:
            create_group_table(groupid)
            user = select_info(groupid, 'userid', message.from_user.id)
        if not user:
            if message.from_user.id > 0:
                print('Adicionado')
                add_sub(groupid, message.from_user.id)
                bot.send_message(message.from_user.id, msgs.voice_sub.format(groupname), parse_mode='HTML')
        else:
            print('Removido')
            del_sub(groupid, message.from_user.id)
            bot.send_message(message.from_user.id, msgs.voice_unsub.format(groupname), parse_mode='HTML')
    except:
        pass

@bot.message_handler(content_types=['voice_chat_started'])
@bot.channel_post_handler(content_types=['voice_chat_started'])
@bot.message_handler(commands=['Notificar'])
def voice_notify(message):
    log_text(message)
    groupid = 'g' + str(message.chat.id*-1)
    msg = select_info('Chats_de_Voz', 'groupid', groupid)
    try:
        voice_ended(msg[0])
    except:
        pass

    if message.chat.username:
        msg = bot.send_message(Channel, msgs.voice_started_group.format(message.chat.username), parse_mode='HTML')
        voice_started(groupid, msg.message_id)

    status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if status in ADMIN:
        i = 0
        groupid = 'g' + str(message.chat.id*-1)
        try:
            users = select_all(groupid)
        except:
            create_group_table(groupid)
            users = select_all(groupid)
        for user in users:
            msg = msgs.voice_started.format(message.chat.title, str(message.chat.id).replace('-100', ''), message.message_id, groupid)
            try:
                bot.send_message(user[0], msg, parse_mode='HTML', disable_web_page_preview=True)
                time.sleep(0.2)
                i = i+1
            except:
                del_sub(groupid, user[0])
                pass
    try:
        bot.send_message(message.chat.id, msgs.notified.format(i, groupid), parse_mode='HTML', disable_web_page_preview=True)
    except:
        pass
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

bot.polling()
