import telebot
import requests

bot = telebot.TeleBot('6109508272:AAHcnsLRl9OF2nTfu4CepevF-OgEsJSV3Sc')
API_KEY_TMDB = 'fb281810f993e41090421b93f80d01a4'  # Reemplaza con tu API key de TMDb
API_KEY_RAWG = '6a15efce69a64898baec03ec846c3358'  # Reemplaza con tu API key de RAWG
WEB_URL = 'https://ramirez55.github.io/Servicios_Oficiales/'
CHANNEL_ID = '@descriptionchanel'

# Diccionario para almacenar los canales de los usuarios con acceso
usuarios_canales = {'darielxd'}

# Variable para el administrador agregar usuarios
add = False

# Variable para que el administrador vea los usuarios con acceso
users = False

# Variable para el administrador banear usuarios
ban = False

@bot.message_handler(commands=['start'])
def start(message):
    global add
    global users
    global ban

    add = False
    users = False
    ban = False

    bot.send_message(chat_id=message.chat.id, text=f'¡Hola, {message.from_user.username}! Bienvenido al bot de descripciones de películas, series y juegos.')
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
        usuarios_texto = "\n".join(usuarios_canales.keys())
        bot.send_message(chat_id=message.chat.id, text=f"Usuarios con acceso al bot:\n{usuarios_texto}")
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
        ban = False
        bot.send_message(chat_id=message.chat.id, text=f"El usuario @{usuario} ha sido baneado del bot.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Lo siento, esta función es solo para administradores.")

def obtener_descripcion_pelicula(nombre_pelicula):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY_TMDB}&query={nombre_pelicula}&language=es'
    response = requests.get(url)
    data = response.json
    ()
    if 'results' in data and len(data['results']) > 0:
        result = data['results'][0]
        if 'overview' in result:
            return result['overview']
    return None

def obtener_descripcion_juego(nombre_juego):
    url = f'https://api.rawg.io/api/games?key={API_KEY_RAWG}&search={nombre_juego}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        result = data['results'][0]
        if 'description_raw' in result:
            return result['description_raw']
    return None

@bot.message_handler(commands=['descripcion'])
def descripcion(message):
    # Verificar si el usuario tiene acceso al bot
    if message.from_user.username in usuarios_canales:
        parametro = message.text.split(' ', 1)
        if len(parametro) < 2:
            bot.send_message(chat_id=message.chat.id, text="Por favor, proporciona el tipo de descripción (pelicula/serie o juego) y el nombre.")
            return

        tipo_descripcion = parametro[0].lower().replace("/", "")
        nombre = parametro[1]

        descripcion = None

        if tipo_descripcion == "pelicula" or tipo_descripcion == "serie":
            descripcion = obtener_descripcion_pelicula(nombre)
        elif tipo_descripcion == "juego":
            descripcion = obtener_descripcion_juego(nombre)
        
        if descripcion:
            bot.send_message(chat_id=message.chat.id, text=descripcion)
        else:
            bot.send_message(chat_id=message.chat.id, text=f"No se encontró la descripción para '{nombre}'.")
    else:
        bot.send_message(chat_id=message.chat.id, text="No tienes acceso para utilizar este bot. Solicita al administrador que te añada.")

bot.polling()