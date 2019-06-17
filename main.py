import serial
import telebot
import time
connected = False
port = 'COM3'
baud = 9600
ser = serial.Serial(port, baud, timeout=0)

TOKEN = "634289689:AAHPe0wqJomFHR7cZR4kbqY5Bw8HeO1_Ecg"


bot = telebot.TeleBot(TOKEN)
stato = 0
# 0 - devo ancora eseguire /start
# 1 - ho eseguito già /start

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "digita /start, o guarda i comandi preimpostati")

@bot.message_handler(commands=['start'])
def start_control(message):
    global stato
    gas = 0
    if stato != 0:
        bot.send_message(message.chat.id, "IMPOSSIBILE : SONO GIA' IN ASCOLTO")

    if stato == 0:
        stato = 1
        bot.reply_to(message, "Avvio il controllo del sistema")
        while True:
            data_str = " "
            while ser.inWaiting() > 0:
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print("data_str ", data_str)
            if data_str[0] == 'w':
                if gas == 0:
                    time.sleep(0.5)
                    bot.send_message(message.chat.id,"I sistemi funzionano normalmente. Resto in attesa")


            if data_str[0] == 'a' and gas == 0:
                gas=1
                bot.send_message(message.chat.id,"Emergenza : Rilevato valore di gas sopra la Norma"
                                                 "\nChiudere il condotto ? /chiudi"
                                                 "\nIgnorare il problema ? /ignora"
                                                 "\n\nil rilevamento verrà fermato, per continuare :"
                                                 "\n/start")
                break

            print("sto eseguendo")
            time.sleep(1)
        '''
        print("Fuori Dal While, Gas = ",gas)
        stato = 0
        '''
        print("Fuori Dal While, Gas = ", gas)
        if gas == 1:
            pass

        stato = 0

@bot.message_handler(commands=['ignora'])
def start_control(message):
    bot.reply_to(message, "ignoro")

@bot.message_handler(commands=['apri'])
def start_control(message):
    bot.reply_to(message, "apro")

@bot.message_handler(commands=['chiudi'])
def start_control(message):
    bot.reply_to(message, "chiudo")

'''
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
# default handler for every other text
'''
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Non ho capito \"" + m.text + "\"\nProva a digitare il comando /help")

bot.polling()
stato = 0
while True:
    print("culo")



