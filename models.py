from dotenv import load_dotenv
import random, smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

def enviar_correo(destinatario, asunto, cuerpo):

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
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")



def pedir_datos():
    personas = {}
    nombre = "a"

    while nombre != "":
        nombre = input("Nombre: ")
        if nombre =="" and len(personas) %2 != 0:
            print("Para poder realizar el sorteo debe haber un numero Par de personas")
            nombre = input("Nombre: ")
            
        elif nombre =="" and (len(personas)) %2 == 0:    
            break

        
        mail = input("Email: ")
        while mail == "":
            print("Debe introducir un email")  
            mail = input("Email: ")
        while mail in personas.values():
            print("Este email ya se ha registrado, por favor usa otro.")
            mail = input("Email: ")

        personas[nombre] = mail
        print(len(personas))
    
             
       
    return personas
        
      
def sorteo():
    personas = pedir_datos()
    
    lista_mails = list(personas.values())
    lista_mails2 =sorted(lista_mails)   
    regalas = {}
    parejas = {}

    for i in lista_mails:
        for a in lista_mails2:
            if a != i and a not in regalas.values():
                regalas[i] = a
                        
               

    for personamail, amigo_invisiblemail in regalas.items():
        
        for clave, valor in personas.items():
            if personamail == valor:
                persona = clave
            elif amigo_invisiblemail == valor:
                amigo_invisible = clave
        parejas[persona]=amigo_invisible    
        print(f"{persona} le regalará a {amigo_invisible}")
    print(parejas)
    enviar_parejas(personas,parejas )
    return personas, parejas


def enviar_parejas(personas, parejas):
    for persona, amigo_invisible in parejas.items():
        destinatario = personas[persona] 
        asunto = "Sorteo de Amigo Invisible"
        cuerpo = f"Hola {persona},\n\nYa tenemos los resultados del sorteo de Amigo Invisible. Este año, deberás regalarle a {amigo_invisible}.\n\n¡Buena suerte y felices fiestas!"
        enviar_correo(destinatario, asunto, cuerpo)


    
   
