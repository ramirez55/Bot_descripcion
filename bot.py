import telebot
import requests

bot = telebot.TeleBot('6109508272:AAF-oavrLtXcODRgtkBAN_Jo894Gr9hfFzo')
API_KEY = 'fb281810f993e41090421b93f80d01a4'
WEB_URL = 'https://ramirez55.github.io/Servicios_Oficiales/'
CHANNEL_ID = '@descriptionchanel'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=f'¡Hola, {message.from_user.username}! Bienvenido al bot de descripciones de películas y series.')
    bot.send_message(chat_id=message.chat.id, text='Por favor, únete a nuestro canal para recibir las últimas actualizaciones: ' + CHANNEL_ID)

@bot.message_handler(commands=['descripcion'])
def descripcion(message):
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
                bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=f'{description}nn📽️ ¡En nuestra web encontraras mas servicios q prestamos {WEB_URL} !🌐')
            else:
                bot.send_message(chat_id=message.chat.id, text=f'{description}n📽️ ¡En nuestra web encontraras mas servicios q prestamos {WEB_URL} !🌐')
        else:
            bot.send_message(chat_id=message.chat.id, text=f'No se encontraron descripciones para {movie_title}')
    else:
        bot.send_message(chat_id=message.chat.id, text=f'No se encontraron resultados para {movie_title}')

bot.polling()
