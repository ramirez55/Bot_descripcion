import telebot
import requests
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6109508272:AAHcnsLRl9OF2nTfu4CepevF-OgEsJSV3Sc')
API_KEY = 'fb281810f993e41090421b93f80d01a4'
WEB_URL = 'https://ramirez55.github.io/Servicios_Oficiales/'
CHANNEL_ID = '@descriptionchanel'

# Lista de nombres de usuario de los administradores
admin_users = ['darielxd', 'pjsr55']  # Agrega aquí los nombres de usuario de los administradores




# Diccionario para almacenar los canales de los usuarios con acceso
usuarios_canales = {'darielxd'}

# Variable para el administrador agregar usuarios
add = False

# Variable para que el administrador vea los usuarios con acceso
users = False

# Variable para el administrador banear usuarios
ban = False

# Variable para almacenar las fechas de vencimiento de los contratos
contratos = {}

@bot.message_handler(commands=['start'])
def start(message):
    global add
    global users
    global ban

    add = False
    users = False
    ban = False

    bot.send_message(chat_id=message.chat.id, text=f'¡Hola, {message.from_user.username}! Bienvenido al bot de descripciones de películas y series.')
    bot.send_message(chat_id=message.chat.id, text='Por favor, únete a nuestro canal para recibir las últimas actualizaciones: ' + CHANNEL_ID)

@bot.message_handler(commands=['add'])
def pedir_add(message):
    global add

    # Verificar que el usuario que envió el mensaje sea el administrador
    if message.from_user.username == 'darielxd':
        add = True
        bot.send_message(chat_id=message.chat.id, text="Envía el nombre de usuario al que desees dar acceso al bot.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

@bot.message_handler(func=lambda message: add)
def agregar_usuario(message):
    global add

    # Verificar que el usuario que envió el mensaje sea el administrador
    if message.from_user.username == 'darielxd':
        usuario = message.text.replace("@", "")
        usuarios_canales[usuario] = True
        contratos[usuario] = None  # Inicialmente no hay fecha de vencimiento del contrato
        add = False
        bot.send_message(chat_id=message.chat.id, text=f"El usuario @{usuario} ahora tiene acceso al bot.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

@bot.message_handler(commands=['users'])
def ver_usuarios(message):
    global users

    # Verificar que el usuario que envió el mensaje sea el administrador
    if message.from_user.username == 'darielxd':
        users = True
        usuarios_texto = "n".join(usuarios_canales.keys())
        bot.send_message(chat_id=message.chat.id, text=f"Usuarios con acceso al bot:n{usuarios_texto}")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

@bot.message_handler(commands=['ban'])
def pedir_ban(message):
    global ban

    # Verificar que el usuario que envió el mensaje sea el administrador
    if message.from_user.username == 'darielxd':
        ban = True
        bot.send_message(chat_id=message.chat.id, text="Envía el nombre de usuario al que desees banear del bot.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

@bot.message_handler(func=lambda message: ban)
def banear_usuario(message):
    global ban

    # Verificar que el usuario que envió el mensaje sea el administrador
    if message.from_user.username == 'darielxd':
        usuario = message.text.replace("@", "")
        usuarios_canales.pop(usuario, None)
        contratos.pop(usuario, None)  # Eliminar la fecha de vencimiento del contrato del usuario
        ban = False
        bot.send_message(chat_id=message.chat.id, text=f"El usuario @{usuario} ha sido baneado del bot.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

@bot.message_handler(commands=['contrato'])
def establecer_contrato(message):
    # Verificar que el usuario tiene acceso al bot
    if message.from_user.username in usuarios_canales:
        global contratos

        usuario = message.from_user.username

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Establecer la fecha de vencimiento del contrato a 30 días a partir de la fecha actual
        fecha_vencimiento = fecha_actual + timedelta(days=30)

        # Guardar la fecha de vencimiento del contrato para el usuario
        contratos[usuario] = fecha_vencimiento

        # Formatear la fecha de vencimiento
        fecha_vencimiento_str = fecha_vencimiento.strftime("%d/%m/%Y")
        
        bot.send_message(chat_id=message.chat.id, text=f"Hola @{usuario}, tu contrato vence el {fecha_vencimiento_str}.")

        # Verificar si faltan dos días o menos para el vencimiento del contrato
        if fecha_vencimiento - timedelta(days=2) <= fecha_actual:
            bot.send_message(chat_id=message.chat.id, text="¡Atención! Tu contrato está próximo a vencer. Si deseas reanudarlo, pulsa el siguiente botón.")
            # Crear botón para reanudar el contrato
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Reanudar contrato", callback_data="reanudar_contrato")
            markup.add(button)
            bot.send_message(chat_id=message.chat.id, text="Si deseas reanudar el contrato antes de que se agoten los 2 días, pulsa el siguiente botón.", reply_markup=markup)
    else:
        bot.send_message(chat_id=message.chat.id, text="No tienes acceso para utilizar este bot. Solicita al administrador que te añada.")

@bot.callback_query_handler(func=lambda call: call.data == "reanudar_contrato")
def reanudar_contrato(call):
    usuario = call.from_user.username
    if usuario in contratos:
        contratos[usuario] = None  # Reiniciar la fecha de vencimiento del contrato a None
        bot.send_message(chat_id=call.message.chat.id, text="Contrato reanudado. ¡Disfruta del servicio!")
    else:
        bot.send_message(chat_id=call.message.chat.id, text="No tienes un contrato para reanudar.")

@bot.message_handler(commands=['descripcion'])
def descripcion(message):
    # Verificar si el usuario tiene acceso al bot
    if message.from_user.username in usuarios_canales:
        movie_title = message.text.split(' ', 1)[1]
        url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}&language=es'
        response = requests.get(url)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            if 'overview' in result:
                description = result['overview']
                image_path = result.get('poster_path', None)
                if image_path:
                    image_url = f"https://image.tmdb.org/t/p/original{image_path}"
                    bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=f'{description}n📽️ ¡En nuestra web encontrarás más servicios que prestamos! {WEB_URL}n')
                else:
                    bot.send_message(chat_id=message.chat.id, text=f'{description}n📽️ ¡En nuestra web encontrarás más servicios que prestamos! {WEB_URL}n')
            else:
                bot.send_message(chat_id=message.chat.id, text=f'No se encontraron descripciones para {movie_title}')
        else:
            bot.send_message(chat_id=message.chat.id, text=f'No se encontraron resultados para {movie_title}')
    else:
        bot.send_message(chat_id=message.chat.id, text="No tienes acceso para utilizar este bot. Solicita al administrador que te añada.")

bot.polling()
