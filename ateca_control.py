import pymysql
import time
from threading import Thread
import threading
import tkinter as tk
from tkinter import ttk

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            db='ateca_access'
            )
        self.cursor = self.connection.cursor()
        
        # print('Conectado\n')
    
    def select_user(self,card):
        sql = 'SELECT id, name, rol FROM users WHERE card_id = {}'.format(card.id)
        
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            if (user): 
                if not (card.status):
                    card.login()
                    self.set_login(user[0], card.id)

                    return user[1]
                else:
                    card.logout()
                    self.set_logout(user[0], card.id)

                    return user[1]
            
            
        except Exception as e:
            raise
        
#     def select_all_users(self):
#         sql = 'SELECT id, name, card_id, rol FROM users'
#         
#         try:
#             self.cursor.execute(sql)
#             users= self.cursor.fetchall()
#             
#             print('\nMostrando datos de los usuarios: \n')
#             for user in users:
#             
#                 print('Id:', user[0])
#                 print('Name:', user[1])
#                 print('Card:', user[2])
#                 print('Rol:', user[3])
#                 print('\n')
#             
#         except Exception as e:
#             raise
        
    def set_card(self,id,card_id):
        sql = 'UPDATE users SET card_id = {} WHERE id = {}'.format(card_id,id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            
        except Exception as e:
            raise
        
    def set_login(self, user_id, card_id):
        sql = "INSERT into activities (activity, user_id,card_id) VALUES('{}', '{}', '{}')".format('Entrada al aula',user_id,card_id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except Exception as e:
            raise
        
    def set_logout(self, user_id, card_id):
        sql = "INSERT INTO activities (activity, user_id, card_id) VALUES('{}', '{}', '{}')".format('Salida del aula',user_id,card_id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            
        except Exception as e:
            raise

    def set_error_log(self, card_id):
        sql = "INSERT INTO activities (activity, card_id) VALUES('{}', '{}')".format('Intento de log incorrecto',card_id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            
        except Exception as e:
            raise
        
    def close(self):
        self.connection.close()
        
class CardService:
    def __init__(self):
        self.status = False
        
    def read_card_id(self,card_id):
        self.id = card_id
        
    def login(self):
        self.status = True
        
    def logout(self):
        self.status = False
        
class FullScreen_Window:
    global db
    global card
    db = Database()
    card = CardService()

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("ATECA CONTROL ACCESS")
        self.frame = tk.Frame(self.tk)
        self.frame.grid()
        self.tk.columnconfigure(0, weight=1)
        
        self.tk.attributes('-zoomed', True)
        self.tk.attributes('-fullscreen', True)
        self.state = True
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.config(cursor="none")
        
        self.show_idle()      

    def show_idle(self):
        self.welcomeLabel = ttk.Label(self.tk, text="Por favor\nPase su identificador por el lector")
        self.welcomeLabel.config(font='size, 70', justify='center', anchor='center')
        self.welcomeLabel.grid(sticky=tk.W+tk.E, pady=370)
        self.input = tk.Entry(self.tk, show='*')
        self.input.grid(sticky=tk.W+tk.E, pady=210)
        self.input.focus()        
        self.input.bind("<Return>", self.listen_rfid)        

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def listen_rfid(self,card_id):
        card.read_card_id(self.input.get())
        if not card.status:
            username = db.select_user(card)
            if username:
                self.current_user_name = username
                self.current_user_card = card.id
                self.welcomeLabel.config(text="Bienvenido {} \nPase su identificador de nuevo para salir".format(username), font='size, 60')
                self.input.delete(0,'end')
                self.input.focus()
                self.input.bind("<Return>", self.listen_rfid)
                
            else:
                t = Thread(target=self.error_action, args=(None,))
                t.start()
        
        else:
            username = db.select_user(card)
            if username and self.current_user_card == card.id:
                self.current_user_card = None
                self.current_user_name = None
                t = Thread(target=self.leave_action, args=(username,))
                t.start()

            else:
                t = Thread(target=self.error_action, args=(self.current_user_name,))
                t.start()

    def leave_action(self,username):
        self.input.grid_forget()
        self.welcomeLabel.config(text="Hasta la próxima {}".format(username))
        time.sleep(3)
        self.welcomeLabel.grid_forget()
        self.show_idle()
    
    def error_action(self, username):
        self.welcomeLabel.grid_forget()
        self.input.grid_forget()
        self.invalidUserLabel = ttk.Label(self.tk, text="Tarjeta no válida")
        self.invalidUserLabel.config(font='size, 70', justify='center', anchor='center')
        self.invalidUserLabel.grid(sticky=tk.W+tk.E, pady=370)
        db.set_error_log(card.id)
        time.sleep(4)
        self.invalidUserLabel.grid_forget()
        if username: 
            self.welcomeLabel = ttk.Label(self.tk, text="Bienvenido {} \nPase su identificador de nuevo para salir".format(username))
            self.welcomeLabel.config(font='size, 60', justify='center', anchor='center')
            self.welcomeLabel.grid(sticky=tk.W+tk.E, pady=370)
            self.input = tk.Entry(self.tk, show='*')
            self.input.grid(sticky=tk.W+tk.E, pady=210)
            self.input.focus()        
            self.input.bind("<Return>", self.listen_rfid)
        else:
            self.show_idle()

if __name__ == '__main__':
    w = FullScreen_Window()
    w.tk.mainloop()

