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
chiuso = 0
ingnora = 0
# 0 - devo ancora eseguire /start
# 1 - ho eseguito già /start
# 2 - ho chiuso la valvola
# 3 - ignoro l'emergenza


def estrai_valore(str):
    out_file = open("misurazioni.csv", "a+")
    val = ''
    for x in str:
        if x != 'a' and x != 'w' and x != '_':
            # print("x : ",x)
            val = val + x
        if x =='_':
            break
    if val !='':
        print("Valore letto : ", val)
        out_file.write('"' + val + '"' + "\n")
        out_file.close()
    return val



def chiudi_valvola():
    '''
    invio il carattere 'c' che serve a far chiudere la valvola del gas
    '''
    ser.write(str.encode('c'))


def apri_valvola():
    '''
    invio il carattere 'o' che serve a far chiudere la valvola del gas
    '''
    ser.write(str.encode('o'))

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "digita /start, o guarda i comandi preimpostati")

@bot.message_handler(commands=['start'])
def start_control(message):
    global stato
    global chiuso

    flag = 0
    fuga = 0
    if stato == 1:
        bot.send_message(message.chat.id, "IMPOSSIBILE : SONO GIA' IN ASCOLTO")
        return
    if stato == 0:
        stato = 1
        while True:
            while ser.inWaiting() > 0:
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                val=estrai_valore(data_str)
                if data_str[0] == 'w' and flag == 0:
                    print("tutto ok")
                    flag =1
                    fuga = 0
                    '''
                    flag serve a far entrare una sola volta nel ciclo il programma
                    in modo da mandare un solo messaggio all'utente
                    '''
                    time.sleep(0.5)
                    bot.send_message(message.chat.id, "I sistemi funzionano normalmente. Resto in attesa")

                if data_str[0] == 'a':
                    print("attenzione")
                    fuga = 1
                    bot.send_message(message.chat.id, "Emergenza : Rilevata fuga di gas : " + val +
                                     "\nChiudere il condotto ? /chiudi"
                                     "\nIgnorare il problema ? /ignora"
                                     "\n\nIL RILEVAMENTO VERRA' FERMATO!!"
                                     "\n per continuare :"
                                     "\n/start")
                    time.sleep(0.5)
                    markdown = """
                                *in assenza di risposta, verrà chiuso automaticamente tra 5 secondi*
                                """
                    ret_msg = bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
                    break #esco dal while della ricezione da seriale
                time.sleep(0.5)

            if fuga == 1:
                '''alla fine del while di ricezione da seriale controllo il motivo dell'uscita
                perchè è possibile o che arduino sia malfunzionante e quindi non manda più niente
                oppure 
                caso principale che sono uscito perchè ho rilevato una fuga di gas'''
                break # esco dal while infinito
    stato=0
    time.sleep(5)
    if chiuso == 0:
        # richiamerò la funzione che mandail messaggio di chiusura ad arduino
        chiuso=1

        markdown = """
                   *Valvola chiusa*
                   """
        bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
        chiudi_valvola()


@bot.message_handler(commands=['ignora'])
def start_control(message):
    global ignora
    ignora = 1
    bot.reply_to(message, "ignoro")

@bot.message_handler(commands=['apri'])
def start_control(message):
    bot.reply_to(message, "apro")

@bot.message_handler(commands=['chiudi'])
def start_control(message):
    global chiuso
    chiuso = 1
    bot.reply_to(message, "chiudo")
    chiudi_valvola()


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
    print("hello_world")



