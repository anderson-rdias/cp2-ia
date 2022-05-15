import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import os.path
from datetime import datetime

import python_weather
import asyncio

async def pegarTemperatura():
    # Declara ao sistema as métricas de clima a serem usadas (celsius, km/h, etc.)
    client = python_weather.Client(format=python_weather.METRIC)

    # Retorna o valor da temperatura da cidade informada acima
    robs = pyttsx3.init()
    print("Informe uma cidade: ")
    robs.say("Obrigado por informar uma cidade")

    som = recon.listen(source)
    cidade = recon.recognize_google(som, language='pt-br')
    recon.adjust_for_ambient_noise(source, duration=3)

    weather = await client.find(cidade)

    temperaturaAtual = "A temperatura da cidade de: " + cidade + " é de: " + str(weather.current.temperature) + " Graus Celsius"
    print(temperaturaAtual)
    robo.say(temperaturaAtual)
    robo.runAndWait()

    # Fecha o sistema
    await client.close()

def abrirWebsite(comando, url):
    robo.say("Abrindo " + comando)
    print("Abrindo " + comando + "...")
    robo.runAndWait()
    webbrowser.open(url, autoraise=True)

recon = sr.Recognizer()
resposta = ""
hora = (str(datetime.today().hour) + ":" + str(datetime.today().minute))

parar = False

with sr.Microphone(1) as source:
    while not parar:
        audio = recon.listen(source)
        recon.adjust_for_ambient_noise(source)
        res = recon.recognize_google(audio, language='pt-br')
        resposta = res.lower()
        print("Texto reconhecido: ", resposta.lower())

        if resposta == "ok sexta-feira":
            robo = pyttsx3.init()
            robo.say("Olá mestre seja bem vindo, o que deseja?")
            print("Olá mestre seja bem vindo, o que deseja?")
            robo.setProperty("voice", b'brasil')
            robo.setProperty('rate', 140)
            robo.setProperty('volume', 1)
            robo.runAndWait()

            while True:

                audio = recon.listen(source)
                res = recon.recognize_google(audio, language='pt-br')
                recon.adjust_for_ambient_noise(source, duration=3)
                resposta = res.lower()
                print("Texto reconhecido: ", resposta)

                if "youtube" in resposta:
                    abrirWebsite(resposta, 'https://www.youtube.com/')

                if "notícias" in resposta:
                    abrirWebsite(resposta, 'https://g1.globo.com/sp/sao-paulo/')

                if "que horas são" in resposta:
                    robo.say(hora)
                    print(hora)
                    robo.runAndWait()

                if "temperatura atual" in resposta:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(pegarTemperatura())
                    # robo.say(pegarTemperatura())
                    #print(str(pegarTemperatura()))
                    # robo.runAndWait()

                if "cadastrar evento" in resposta:
                    fala = "Ok, qual evento devo cadastrar?"
                    robo.say(fala)
                    print(fala)
                    robo.runAndWait()

                    audio = recon.listen(source)
                    resAgenda = recon.recognize_google(audio, language='pt-br')

                    file_exists = os.path.exists('agenda.txt')

                    if not file_exists:
                        text_file = open("agenda.txt", "w")
                        text_file.write(resAgenda)
                        text_file.close()
                        robo.say("Evento cadastrado")
                        print("Evento cadastrado")
                        break

                    else:
                        text_file = open("agenda.txt", "a")
                        text_file.write("\n" + resAgenda)
                        text_file.close()
                        robo.say("Evento cadastrado")
                        print("Evento cadastrado")
                        continue

                if "ler agenda" in resposta:
                    with open("agenda.txt") as file:
                        for line in file:
                            line = line.strip()  # preprocess line
                            robo.say(line)
                            robo.runAndWait()

                if "assuntos do momento" in resposta:
                    robo.say("Mostrando as trendings")
                    robo.runAndWait()
                    webbrowser.open('https://twitter.com/explore/tabs/trending', autoraise=True)

                elif "parar" in resposta:
                    robo.say("OK! Até mais tarde senhor!")
                    robo.runAndWait()
                    parar = True
                    break