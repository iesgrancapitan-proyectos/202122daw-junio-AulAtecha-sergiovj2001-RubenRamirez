from zipapp import create_archive
import pymysql
import time
from threading import Thread
import threading
import tkinter as tk
from tkinter import ttk

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='192.168.31.219',
            user='admin',
            password='admin',
            db='ateca_access'
            )
        self.cursor = self.connection.cursor()
        
        print('Conectado\n')
      
    def create_user(self, username, card_id, rol):
      sql = "INSERT into users (name, card_id, rol) values ('{}', '{}','{}')".format(username, card_id, rol)

      try:
        self.cursor.execute(sql)
        self.connection.commit()

      except Exception as e:
        raise

    def select_all_users(self):
      sql = 'SELECT id, name, card_id, rol FROM users'
        
      try:
        self.cursor.execute(sql)
        users= self.cursor.fetchall()
        
        return users
          
      except Exception as e:
        raise

    def get_roles(self):
      sql = "SELECT * FROM roles"

      try:
        self.cursor.execute(sql)
        result= self.cursor.fetchall()
        
        roles = list(sum(result,()))

        return roles
          
      except Exception as e:
        raise

class CardService:
        
    def read_card_id(self,card_id):
        self.id = card_id
        

class FullScreen_Window:
    global db
    global card
    db = Database()
    card = CardService()

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("ATECA USERS")
        self.frame = tk.Frame(self.tk)
        self.frame.grid()
        self.tk.columnconfigure(0, weight=1)
        
        self.tk.attributes('-zoomed', True)
        self.tk.attributes('-fullscreen', True)
        self.state = True
        # self.tk.bind("<F11>", self.toggle_fullscreen)
        # self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.config(cursor='arrow')
        
        self.show_idle()
        
        # t = Thread(target=self.listen_rfid)
        # t.daemon = True
        # t.start()    

    def show_idle(self):
        self.welcomeLabel = ttk.Label(self.tk, text="ATECA USERS")
        self.welcomeLabel.config(font='size, 28', justify='center', anchor='center')
        self.welcomeLabel.grid(sticky=tk.W+tk.E, pady=70)
        self.createButton = ttk.Button(self.tk, text='Crear Usuario', command=self.show_create_user)
        self.createButton.grid(pady=50)
        self.show_users()

    def show_users(self):
      self.table = ttk.Treeview(self.tk, columns=(1, 2, 3, 4), show='headings', height=10)
      self.table.grid()

      self.table.heading(1, text='Id')          
      self.table.heading(2, text='Nombre')          
      self.table.heading(3, text='Tarjeta')          
      self.table.heading(4, text='Rol')

      users = db.select_all_users()

      for user in users:
        self.table.insert('','end',values=user)   

    def show_create_user(self):
      self.welcomeLabel.grid_forget()
      self.createButton.grid_forget()
      self.table.grid_forget()

      self.createLabel = ttk.Label(self.tk, text="CREAR NUEVO USUARIO")
      self.createLabel.config(font='size, 28', justify='center', anchor='center')
      self.createLabel.grid(sticky=tk.W+tk.E, pady=70)

      self.nameLabel = ttk.Label(self.tk, text="Nombre ")
      self.nameLabel.config(font='size, 20', justify='center', anchor='center')
      self.nameLabel.grid(sticky=tk.W+tk.E, pady=30)

      self.nameInput = ttk.Entry(self.tk)
      self.nameInput.grid()

      self.cardLabel = ttk.Label(self.tk, text="Tarjeta ")
      self.cardLabel.config(font='size, 20', justify='center', anchor='center')
      self.cardLabel.grid(sticky=tk.W+tk.E, pady=30)

      self.cardInput = ttk.Entry(self.tk)
      self.cardInput.grid()

      self.cardAdviceLabel = ttk.Label(self.tk, text="Para introducir la tarjeta pasela por el lector ")
      self.cardAdviceLabel.config(font='size, 15', justify='center', anchor='center')
      self.cardAdviceLabel.grid(sticky=tk.W+tk.E, pady=30)

      roles = db.get_roles()
      self.clicked = tk.StringVar()
      self.clicked.set(roles[0])
      self.rolesMenu = ttk.OptionMenu(self.tk, self.clicked, roles[0], *roles)
      self.rolesMenu.grid(pady=30)

      self.createButton = ttk.Button(self.tk, text="Crear",command=self.create_user)
      self.createButton.grid()

    def create_user(self):
      if self.nameInput.get() == '' and self.cardInput.get() == '':
        t = Thread(target=self.display_error)
        t.start()

      else:
        db.create_user(self.nameInput.get(), self.cardInput.get(),self.clicked.get())  
        self.createLabel.grid_forget()
        self.nameLabel.grid_forget()
        self.nameInput.grid_forget()
        self.cardLabel.grid_forget()
        self.cardInput.grid_forget()
        self.cardAdviceLabel.grid_forget()
        self.rolesMenu.grid_forget()
        self.createButton.grid_forget()
        self.show_idle()


    def display_error(self):
      self.createLabel.grid_forget()
      self.nameLabel.grid_forget()
      self.nameInput.grid_forget()
      self.cardLabel.grid_forget()
      self.cardInput.grid_forget()
      self.cardAdviceLabel.grid_forget()
      self.rolesMenu.grid_forget()
      self.createButton.grid_forget()
      self.errorLabel = ttk.Label(self.tk, text="Datos Incorrectos \n Por introduzca de forma correcta su nombre y su tarjeta")
      self.errorLabel.config(font='size, 35', justify='center', anchor='center')
      self.errorLabel.grid(sticky=tk.W+tk.E, pady=250)
      time.sleep(3)
      self.errorLabel.grid_forget()
      self.show_idle()


if __name__ == '__main__':
    w = FullScreen_Window()
    w.tk.mainloop()
