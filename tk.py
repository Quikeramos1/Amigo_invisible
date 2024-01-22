from tkinter import *
import tkinter as tk
from tkinter import ttk,font
from dotenv import load_dotenv
import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()




class Aplicacion(Toplevel):
    def __init__(self,master=None):
        super().__init__(master)
        
              
        self.title("Sorteo Amigo Invisible")
        fuente=font.Font(weight="bold")

        #variables de entrada
        self.nombre= StringVar()
        self.email= StringVar()

        #configuracion ventana principal

        ttk.Label(self, text= "Bienvenid@ a sorteo de amigo invisible",font=fuente).pack(pady=10)
        self.width = int(self.winfo_screenwidth()//2)
        self.height = int(self.winfo_screenheight()//1)
        self.pwidth = round(self.winfo_screenwidth() // 2 - self.width // 2)
        self.pheight = round(self.winfo_screenheight() // 2 - self.height // 2)
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.pwidth, self.pheight))
        self.iconbitmap("/media/icon.png")

        #widgets

        self.etiqueta_nombre=ttk.Label(self, text= "Introduce el nombre del participante:").pack(pady=20)
        self.entrada_nombre=ttk.Entry(self, textvariable=self.nombre).pack()

        self.etiqueta_mail=ttk.Label(self, text= "Introduce el email del participante:").pack(pady=20)
        self.entrada_mail=ttk.Entry(self, textvariable= self.email).pack()

        ttk.Button(self, text="Añadir otro amigo", command=self.pedir_datos).pack(pady=20)

        ttk.Button(self, text="Realizar Sorteo", command=self.sorteo).pack(pady=20)

        ttk.Button(self, text='Salir', command=quit).pack(pady=20)

        self.ventana=tk.Text(self)
        self.ventana.pack()
        
        
        self.mainloop()

    def log(self, message):
        self.ventana.insert(tk.END, f"{message}\n")
        self.ventana.see(tk.END)  


    def enviar_correo(self,destinatario, asunto, cuerpo):

        # Configuración del correo
        remitente = os.getenv("CORREO")
        contraseña = os.getenv("PASS")

        # Crear el objeto MIMEText
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Conexión con el servidor SMTP de Gmail
        try:
            servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            servidor_smtp.starttls()
            servidor_smtp.login(remitente, contraseña)

            # Envío del correo
            servidor_smtp.sendmail(remitente, destinatario, mensaje.as_string())

            # Cierre de la conexión
            servidor_smtp.quit()
            self.log("Correo enviado exitosamente.")
            
        except Exception as e:
            self.log(f"Error al enviar el correo: {e}")
            
            


    personas = {}
    def pedir_datos(self):
        personas = self.personas
          
        nombre = self.nombre.get()
        email = self.email.get()
        if nombre == "":
            self.log("Debe introducir un nombre")
            
            return      
                                    
        if email == "":
            self.log("Debe introducir un email") 
            return
            
        elif email in personas.values():
            self.log("Este email ya se ha registrado, por favor usa otro.")
            return
            

        personas[nombre] = email
        self.log(f"{nombre} añadido exitosamente.")
        self.log(f"Personas registradas hasta ahora: {personas}")
        
        # Limpia las entradas para permitir nuevas entradas
        self.nombre.set("")
        self.email.set("")
            
        
                
        
        return personas
            
        
    def sorteo(self):
        personas = self.personas 
        self.log(personas)
        
        lista_mails = list(personas.values())
        lista_mails2 =sorted(lista_mails)   
        self.regalas = {}
        self.parejas = {}

        for i in lista_mails:
            for a in lista_mails2:
                if a != i and a not in self.regalas.values():
                    self.regalas[i] = a
                            
                

        for personamail, amigo_invisiblemail in self.regalas.items():
            
            for clave, valor in personas.items():
                if personamail == valor:
                    persona = clave
                elif amigo_invisiblemail == valor:
                    amigo_invisible = clave
            self.parejas[persona]=amigo_invisible    
            print(f"{persona} le regalará a {amigo_invisible}")
        print(self.parejas)
        self.enviar_parejas(personas,self.parejas )
        return personas, self.parejas


    def enviar_parejas(self,personas, parejas):
        for persona, amigo_invisible in parejas.items():
            self.destinatario = personas[persona] 
            asunto = "Sorteo de Amigo Invisible"
            cuerpo = f"Hola {persona},\n\nYa tenemos los resultados del sorteo de Amigo Invisible. Este año, deberás regalarle a {amigo_invisible}.\n\n¡Buena suerte y felices fiestas!"
            self.enviar_correo(self.destinatario, asunto, cuerpo)



def mostrar_aplicacion(master):
     app = Aplicacion(master=master)

def mostrar_ventana_splash():
    splash_root = Tk()
    splash_root.overrideredirect(True)

    image_path = "media/splash.png"
    image = PhotoImage(file=image_path)
    img_label = Label(splash_root, image=image)
    img_label.pack()

    nombre_text = "®Enrique Ramos Fuster\n2024\nAplicación diseñada para\nsu libre uso y distribución."
    nombre_label = Label(splash_root, text=nombre_text)
    

    

    width = int(splash_root.winfo_screenwidth()//2)
    height = int(splash_root.winfo_screenheight()//1)
    pwidth = round(splash_root.winfo_screenwidth() // 2 - width // 2)
    pheight = round(splash_root.winfo_screenheight() // 2 - height // 2)
    splash_root.geometry("{}x{}+{}+{}".format(width, height, pwidth, pheight))

    nombre_label_x = (width - nombre_label.winfo_reqwidth()) // 2
    nombre_label_y = (height - nombre_label.winfo_reqheight()) //2  

    nombre_label.place(x=nombre_label_x, y=nombre_label_y)
    ttk.Label(splash_root, text="¡Bienvenido!").pack(pady=10)
    ttk.Button(splash_root, text="Abrir Aplicación", command=lambda: mostrar_aplicacion(splash_root)).place(x=nombre_label_x +20, y=(nombre_label_y+80))

    
    
    splash_root.mainloop()



     



   



if __name__ == "__main__":
   mostrar_ventana_splash()
    