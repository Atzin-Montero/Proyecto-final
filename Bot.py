### librerías

import discord
import requests
import time
from bs4 import BeautifulSoup
from discord.ext import commands
from settings import settings
from googletrans import Translator

### Comandos necesarios para el funcionamiento de las funciones

translator = Translator()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

### Inicialización del bot
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

### Comandos que el usuario puede utilizar
@bot.command()
async def help_me(ctx):
    await ctx.send("Aquí tienes una lista de comandos con los que te puedo ayudar: \n $instalar \n $buscar")

### Saludo
@bot.command()
async def hola(ctx):
    await ctx.send(f'Que tal! Soy un bot {bot.user}, mi proposito es ayudarte a encontrar el mejor videojuego para tí despúes de que me hables de tus preferencias. Puedo buscar en Steam por ahora')
    time.sleep(3)
    ### Proximamnete se agregarán más plataformas de las que se podrá buscar
    #await ctx.send(f'Para definir en que plataforma prefieres buscar, utiliza el comando $seleccionar y el nombre de la plataforma')
    time.sleep(2)
    await ctx.send(f'Si necesitas saber que comandos puedo utilizar, utiliza el comando $help_me')

### Seleccionar plataforma (todavía no fucnional)
#@bot.command()
#async def seleccionar(ctx, texto):
#    aplicacion = texto
#    await ctx.send("Plataforma seleccionada: ", aplicacion)
#    if (aplicacion == "Steam"):
#        url = "https://store.steampowered.com/"

### Instalar la plataforma
@bot.command()
async def instalar(ctx):
    aplicacion = "Steam"
    if (aplicacion == "Steam"):
        await ctx.send(f'Para installar Steam necesitas el instalador que puedes obtener directamente en https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe para Windouws, https://cdn.fastly.steamstatic.com/client/installer/steam.dmg para Mac o https://support.google.com/chromebook?p=steam_on_chromebook para Chromebook; también puedes explorar en la página oficial de Steam (https://store.steampowered.com/)')

### Buscar videojuegos (por ahora llega solo a géneros, pero pronto llegará a más)
@bot.command()
async def buscar(ctx):
    aplicacion = "Steam"
    url = "https://store.steampowered.com/"
    response = requests.get(url)
    bs = BeautifulSoup(response.text,"lxml")
    if (aplicacion == "Steam"): 
        temp = bs.find_all("a", "gutter_item")

    tam = len(temp)
    await ctx.send("¿Tienes un género en mente? Si es así selecciona alguno de los siguientes (envía solo el número):")
    arreglo = [0] * tam
    href_value = [] * (tam)
    j = 0
    for link in temp:
        href_val = link.get('href')
        href_value.append(href_val)
        j=j+1
    for i in range(tam):
        texto = temp[i].text
        texto = texto.replace("\n","")
        texto = texto.replace("\t","")
        texto = translator.translate(texto, dest='es')
        await ctx.send(f"{i}. {texto.text}")
        arreglo[i] = i
    await ctx.send("Si no sabes por donde buscar, envia 'no' y te ayudaré a decidir")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and (
        message.content.isdigit() and int(message.content) in range(0, len(arreglo) + 1) or message.content == 'no'
    )
    response = await bot.wait_for('message', check=check)
    
    if (response == "no"):
        await ctx.send("Envia el comando 'genero' para ayudarte a averiguar que género te gustaría más")
    else:
        for i in range(tam): 
            if int(response.content) == i:
                link = href_value[i]
                print(link)
                break
        url = link
        await ctx.send(f"Has elegido el género número {response.content}, por ahora aquí tienes un enlace para acceder directamente a buscar: {url}") #proximamente buscará juegos y recomendará de estos

bot.run(settings['TOKEN'])
