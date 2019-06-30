import serial
import telebot
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import threading

mutex = threading.Lock()

connected = False
port = 'COM3'
baud = 9600
ser = serial.Serial(port, baud, timeout=0)

TOKEN = "634289689:AAHPe0wqJomFHR7cZR4kbqY5Bw8HeO1_Ecg"
VAL_MAX = 250 #valore massimo di gas rilevato

bot = telebot.TeleBot(TOKEN)
stato = 0
chiuso = 0
ignora = 0

media = 20.334672693788715
sigma = 81.20074108736098


# 0 - devo ancora eseguire /start
# 1 - ho eseguito gia' /start
# 2 - ho chiuso la valvola
# 3 - ignoro l'emergenza


def calcola_probabilita(val, media, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi)) * np.exp((-1 / 2) * ((val - media) ** 2 / sigma ** 2)))


def scrivi_val_su_file(val):
    out_file = open("misurazioni.txt", "a+")
    out_file.write(val + "\n")
    out_file.close()


def estrai_valore(str):
    val = ''
    for x in str:
        if x != 'e' and x != 'f' and x != 'a' and x != 'w' and x != '_':
            # print("x : ",x)
            val = val + x
        if x =='_':
            break
    if val !='':
        print("Valore letto : ", val)
        scrivi_val_su_file(val)
    else:
        val = '0'
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
    markdown = """
    *Benvenuto nel sistema di monitoramento per rilevamento fughe di gas*
    _Ecco la lista di comandi disponibili :_
    
    /help - Lista comandi disponibili
    /start - Avvio monitoramento del sistema
    /chiudi - Chiude la valvola
    /apri - Apre la valvola
    /ignora - Ignora il messaggio di emergenza
    /istogramma - Istogramma delle misurazioni effettuate
    """
    bot.send_message(message.chat.id, markdown, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start_control(message):
    global chiuso , media, sigma,stato,VAL_MAX,ignora, mutex

    SOGLIA =calcola_probabilita(VAL_MAX,media,sigma)

    flag = 0
    fuga = 0
    if stato == 1:
        bot.send_message(message.chat.id, "IMPOSSIBILE : SONO GIA' IN ASCOLTO")
        return
    if stato == 0:

        stato = 1
        while True:
            while ser.inWaiting() > 0:
                mutex.acquire()
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                mutex.release()
                val=estrai_valore(data_str)

                if int(val) >= 0 or val != '':
                    prob = calcola_probabilita(int(val), media, sigma)
                else:
                    print("errore calcolo probabilità")
                    prob = calcola_probabilita(0, media, sigma)
                if len(data_str) == 0:
                    data_str = " "

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
                '''
                    Qui controllo anchese la probabilita' della misurazione e' sotto la soglia ancor prima di ottenere
                    un messaggio di allarme
                    in questo modo se il sensore dovesse non funzionare più la sua uscita analogica sara'
                    nulla ed arduino inviera' sicuramente un segnale che inizia con 'a'
                '''
                if data_str[0] == 'a' or prob < SOGLIA:
                    print("attenzione, il bot verrà arrestato. Il condotto verrà chiuso. RILEVATO GAS")
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
    if ignora == 0:
        if chiuso == 0:
            # richiamerò la funzione che mandail messaggio di chiusura ad arduino
            chiuso = 1
            markdown = """
                       *Valvola chiusa*
                       """
            bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
            chiudi_valvola()
        else:
            markdown = """
                        _La valvola è già chiusa_
                        """
            bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
            chiudi_valvola()
    else:
        markdown = "*messaggio di allarme ignorato*" \
                   "\nDigitare /start per ricominciare il controllo del sistema"
        bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
        ignora = 0

@bot.message_handler(commands=['ignora'])
def start_control(message):
    global ignora
    ignora = 1
    bot.reply_to(message, "ignoro")



def controllo_errore_chiusura_apertura():
    mex =""
    flag = 0
    mex_letto =""
    while True:
        while ser.inWaiting() > 0:
            mex_letto = ser.read(ser.inWaiting()).decode('ascii')
        print(mex_letto)
        for i in mex_letto:
            if i == 'e':
                flag = 1
            if i == 'f':
                flag = 2
            if i == 'T':
                flag = 3
        if flag == 1 or flag == 2 or flag== 3:
            break
    if flag == 1:
        mex += "ERRORE CHIUSURA/APERTURA !!!!" \
              "NECESSARIA AZIONE MANUALE"
    if flag == 2 and flag == 1:
        mex += "\nFLUSSO NON RILEVATO"
    if flag == 3:
        mex = ""
    print("mex : ", mex)
    return mex






@bot.message_handler(commands=['apri'])
def start_control(message):
    global chiuso, mutex
    if chiuso == 1:
        chiuso = 0
        bot.reply_to(message, "apro")
        apri_valvola()
        mutex.acquire()
        mess = controllo_errore_chiusura_apertura()
        mutex.release()
        if mess != "":
            bot.send_message(message.chat.id, mess)
    else:
        bot.reply_to(message, "è già aperta")


@bot.message_handler(commands=['chiudi'])
def start_control(message):
    global chiuso
    if chiuso == 0:
        chiuso = 1
        bot.reply_to(message, "chiudo")
        chiudi_valvola()

        mutex.acquire()
        mess = controllo_errore_chiusura_apertura()
        mutex.release()

        if mess != "":
            bot.send_message(message.chat.id, mess)
    else:
        bot.reply_to(message, "è già chiusa")


def calcola_istogramma():
    seq_in = np.array([])

    in_file = open("misurazioni.txt", "r")
    # text = in_file.read()
    for i in in_file.read().split():
        #print(i)
        i = int(i)
        if i != 0 and i < 900:
            # print(i)
            seq_in = np.append(seq_in, int(i))
    in_file.close()

    fig = plt.figure()
    plt.hist(seq_in, normed=False, bins=30)
    plt.ylabel('Frequenza')
    plt.xlabel('Valori')
    fig.savefig('plot.png')
    #plt.show()


# Handle '/istogramma'
@bot.message_handler(commands=['istogramma'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Invio Instogramma")
    # sendPhoto
    calcola_istogramma()
    time.sleep(1)
    photo = open("plot.png", 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Non ho capito \"" + m.text + "\"\nProva a digitare il comando /help")

bot.polling()




