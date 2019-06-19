
@bot.message_handler(commands=['start'])
def start_control(message):
    global stato
    gas = 0
    if stato == 1:
        bot.send_message(message.chat.id, "IMPOSSIBILE : SONO GIA' IN ASCOLTO")

    if stato == 0:
        stato = 1
        bot.reply_to(message, "Avvio il controllo del sistema")
        while True:
            data_str = ""
            while ser.inWaiting() > 0:
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print("data_str ", data_str)
            if data_str[0] == 'w':
                if gas == 0:
                    time.sleep(0.5)
                    bot.send_message(message.chat.id,"I sistemi funzionano normalmente. Resto in attesa")


            if data_str[0] == 'a' and gas == 0:
                gas=1
                num=estrai_valore(data_str)
                
                bot.send_message(message.chat.id,"Emergenza : Rilevato valore di gas sopra la Norma : " + num +
                                                 "\nChiudere il condotto ? /chiudi"
                                                 "\nIgnorare il problema ? /ignora"
                                                 "\n\nil rilevamento verrà fermato, per continuare :"
                                                 "\n/start")

                markdown = """
                        *in assenza di risposta, verrà chiuso automaticamente tra 5 secondi*
                        """
                ret_msg = bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
                break

            print("sto eseguendo")
            time.sleep(1)
        '''
        print("Fuori Dal While, Gas = ",gas)
        stato = 0
        '''
        print("Fuori Dal While, Gas = ", gas)
        if gas == 1:
            time.sleep(5)
            if stato == 1:
                #richiamerò la funzione che mandail messaggio di chiusura ad arduino
                markdown = """
                           *Valvola chiusa*
                           """
                bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
                pass
        stato = 0
