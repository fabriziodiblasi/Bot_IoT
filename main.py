import telepot
import time
import serial as ser
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "728881262:AAHL2_K1vK4kODhj5NUqxk7gO3-aMqYCE6E"
connected = False
port = 'COM3'
baud = 9600
ser = ser.Serial(port, baud, timeout=500)

'''
def leggi_seriale():
    data_str = " "
    print("dentro funzione leggi seriale")
    while True :
        if ser.inWaiting() > 0:
            data_str = ser.read(ser.inWaiting()).decode('ascii')
            print("data_str ",data_str)
        if data_str[0]==" ":
            print("return q")
            return 'q'
    
        if data_str[0] == 'w':
            print("return w")
            return "w"
        if data_str[0] == 'a':
            val = ""
            for i in data_str:
                if i != 'a' and i != '_':
                    val += i
            print("return val ",'a'+val)
            return 'a'+val
'''



def on_chat_message(msg):  # crea la tastiera personalizzata
    content_type, chat_type, chat_id = telepot.glance(msg)
    '''
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Chiudi Valvola", callback_data='/chiudi'),
                                                      InlineKeyboardButton(text="Apri Valvola", callback_data='/apri')],
                                                     [InlineKeyboardButton(text="Monitora", callback_data='/monitora'),
                                                      InlineKeyboardButton(text="Andamento giornaliero", callback_data='/andamento')]])
    '''
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Start", callback_data='/start')]])
    bot.sendMessage(chat_id, 'seleziona un comando', reply_markup=keyboard)
    print(content_type,' ', chat_type,' ', chat_id)


def on_callback_query(msg):  # aziona i vari LED in base al pulsante toccato
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    #content_type, chat_type, chat_id = telepot.glance(msg)

    print('Callback Query:', ' ', query_id, ' ', from_id, ' ', query_data)

    if query_data == '/chiudi':
        #bot.answerCallbackQuery(query_id, text='comando chiudi eseguito')
        bot.sendMessage(from_id,"comando chiudi eseguito")
        bot.answerCallbackQuery(query_id, text='')

    elif query_data == '/apri':
        bot.sendMessage(from_id, text='Comando apri eseguito')
        bot.answerCallbackQuery(query_id, text='')

    elif query_data == '/start':
        bot.sendMessage(from_id, text='Benvenuto, contatto il MCU')
        data_str = " "
        flag = 1
        while True:
            #print("sto monitorando")
            data_str = " "
            if ser.inWaiting() > 0:
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print("data_str ", data_str)

            if data_str[0] == 'w':
                stato = 0 # non c'è alcuna emergenza
                print("stato 0")
            if data_str[0] == 'a':
                stato = 1

            if stato ==0 :
                print("stato 0")
                bot.sendMessage(from_id, text='tutti i sistemi funzionano normalmente')
                stato = -1

            if stato ==1 and flag == 1 :
                flag = 0
                bot.sendMessage(from_id, text='rilevata fuga di gas')
                bot.sendMessage(from_id, text='attenzione!!!! livello di gas sopra la norma')
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="Chiudi Valvola", callback_data='/chiudi'),
                                      InlineKeyboardButton(text="Apri Valvola", callback_data='/apri')]])
                bot.sendMessage(from_id, 'seleziona un comando', reply_markup=keyboard)

                bot.sendMessage(from_id, text='rilevata fuga di gas')
                stato = -1
            time.sleep(0.1)


    elif query_data == '/andamento':
        bot.sendMessage(from_id, text='Andamento eseguito')
        bot.answerCallbackQuery(query_id, text='')




bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')


while 1:

    time.sleep(0.1)
