# This Python file uses the following encoding: utf-8

import datetime

from core.commands import CommandBase

class SpokenTimeCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(SpokenTimeCommand, self).__init__(commands, CommandBase.TYPE_CHANNEL, "speak")

    def help(self, config, event):
        return "Tell the current date and time in words."

    def work(self, config, event):

        month = ['','Januar','Februar',"März",'April','Mai','Juni','Juli',
                 'August','September','Oktober','November','Dezember']

        w_day = ['Montag','Dienstag','Mittwoch',"Donnerstag",
                 'Freitag','Samstag','Sonntag']

        spokenDateTime = ""
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute

        if event["text"] == "speak time de":
            stunde = numToDeWords(h)
            if m == 0:
                spokenDateTime = ":alarm_clock: Es ist {} Uhr".format(stunde)
            else:
                if m == 1:
                    minute  = "eine"
                    einheit = "Minute"
                else:
                    minute  = numToDeWords(m)
                    einheit = "Minuten"
                spokenDateTime = ":alarm_clock: Es ist {} Uhr und {} {}".format(stunde,minute,einheit)

        elif event["text"] == "speak date de":
            we = datetime.datetime.now().weekday() # Localtime(DE).weekday_name?
            da = datetime.datetime.now().day
            mo = datetime.datetime.now().month # Localtime(DE).monat_name?
            ye = datetime.datetime.now().year
            spokenDateTime = ":calendar: Heute ist {}, der {}te {} {}".format(w_day[we],
                                                                              numToDeWords(da),
                                                                              month[mo],
                                                                              numToDeWords(ye).capitalize(),)

        else:
            spokenDateTime = "Please use `speak [date|time] [de]`"

        response = "<@{}> {}."\
            .format(event["user"],
                    spokenDateTime)
        return response

def numToDeWords(num,join=True):
    '''words = {} convert an integer number into German words'''
    units = ['','ein','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
    teens = ['','elf','zwölf','dreizehn','vierzehn','fünfzehn','sechszehn', \
             'siebzehn','achtzehn','neunzehn']
    tens = ['','zehn','zwanzig','dreizig','vierzig','fünfzig','sechszig','siebzig', \
            'achzig','neunzig']
    thousands = ['','tausent','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('null')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundert')
            if t>1:
                if u>=1: words.append(units[u])
                if u>=1: words.append('und')
                words.append(tens[t])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): 
                words.append(thousands[g])
                words.append('und')
    if join: return '-'.join(words)
    return words
