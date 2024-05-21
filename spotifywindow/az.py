
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re
#para transformar letras con acento en letras sin acento
from unidecode import unidecode

#hace distintas transformaciones para que la url de azlyrics sea valida
def parse_artist(artist_name):
    url_artist = artist_name.lower() #lo pongo en minuscula
    url_artist = unidecode(url_artist) #cambio áéíóúýñ por aeiouyn
    if url_artist.split(' ')[0] == 'the': #le saco el the
        url_artist = ''.join(url_artist.split(' ')[1:])
    url_artist = url_artist.split('&')[0].split(',')[0]
    url_artist = url_artist.replace(' ','') #le saco los espacios ya que no me sirven en la url
    url_artist = re.sub("[^a-z0-9]+", "", url_artist) #re.sub saca todo lo que no sea caracter de azAZ09 (alfanumerico)
    if len(url_artist)<3: #le agrego band al final si el nombre tiene 2 caracteres
        url_artist += 'band'
    return url_artist

#re.sub le saca al nombre cosas como apostrofes ' ó guiones - 
def parse_track(track_name):
    url_track = track_name.lower() #lo pongo en minuscula
    url_track = unidecode(url_track) #cambio áéíóúýñ por aeiouyn
    url_track = ''.join(url_track.split(" - ")[0].replace(' ','').split('-')) #cambio a - b por a solo
    url_track_noand = url_track.replace('&','')
    url_track_and = url_track.replace('&','and')
    url_track3 = re.sub("[^a-z0-9]+", "", url_track_and)
    url_track4 = re.sub("[^a-z0-9]+", "", url_track_and.split('(')[0])
    url_track2 = re.sub("[^a-z0-9]+", "", url_track_noand) #el track name entero sacando parentesis
    url_track = re.sub("[^a-z0-9]+", "", url_track_noand.split('(')[0]) #corto el track name en (...
    return url_track, url_track2, url_track3, url_track4
    
def parse_url(artist_name, track_name):
    url_artist = parse_artist(artist_name)
    url_track, url_track2, url_track3, url_track4 = parse_track(track_name)
    url = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track+'.html'
    url2 = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track2+'.html'
    url3 = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track3+'.html'
    url4 = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track4+'.html'
    return url, url2, url3, url4 #retorno las 4 posibles urls

"""
-------------------------------------------------------------------------------------
https://www.azlyrics.com/lyrics/tonightalive/breakingentering.html
https://www.azlyrics.com/lyrics/tonightalive/breakingentering.html
https://www.azlyrics.com/lyrics/tonightalive/breakingandentering.html
https://www.azlyrics.com/lyrics/tonightalive/breakingandentering.html
-------------------------------------------------------------------------------------
https://www.azlyrics.com/lyrics/taylorswift/foreveralways.html
https://www.azlyrics.com/lyrics/taylorswift/foreveralwayspianoversiontaylorsversion.html
https://www.azlyrics.com/lyrics/taylorswift/foreverandalwayspianoversiontaylorsversion.html
https://www.azlyrics.com/lyrics/taylorswift/foreverandalways.html
-------------------------------------------------------------------------------------
1)una cancion se llama breaking & entering
2)otra se llama forever & always
en 1) la url valida es breakingandentering
en 2) la url valida es foreveralways
por otro lado en 2) vemos que la cancion tiene nombre forever & always (piano version) (taylor's version)
entonces se dan las 4 variantes posibles:
    url = foreveralways
    url = foreveralwayspianoversiontaylorsversion
    url = foreverandalwayspianoversiontaylorsversion
    url = foreverandalways
-------------------------------------------------------------------------------------
"""

#recibe nombre artista y nombre de cancion y retorna la letra si es que existe
#o no lyrics si no la encuentra
def get_lyrics(artist_name, track_name):
    
    #setting up the url according to azlyrics criteria
    url, url2, url3, url4 = parse_url(artist_name, track_name)
    print(url,'\n',url2,'\n',url3,'\n',url4)
    
    #request = requests.get(url) #usando mi propia ip

    #usando scraperapi con mi propia cuenta y token (5mil request gratis por mes)
    #para no usar mi ip y que me baneen de azlyrics
    payload = {'api_key': '2315b2be779810a3e745bdd118ddb7c7', 'url': url}
    payload2 = {'api_key': '2315b2be779810a3e745bdd118ddb7c7', 'url': url2}
    payload3 = {'api_key': '2315b2be779810a3e745bdd118ddb7c7', 'url': url3}
    payload4 = {'api_key': '2315b2be779810a3e745bdd118ddb7c7', 'url': url4}

    all_differents = (url!=url2!=url3!=url4) #mejorar esto, 2 y 3 pueden ser iguales y 1 y 2 tambien

    request = requests.get('http://api.scraperapi.com', params=payload2)
    print("1r")
    
    if all_differents and request.status_code == 404:
        return None
    
    if request.status_code == 404:
        request = requests.get('http://api.scraperapi.com', params=payload)
        print("2r")
        if request.status_code == 404:
            request = requests.get('http://api.scraperapi.com', params=payload4)
            print("3r")
            if request.status_code == 404:
                request = requests.get('http://api.scraperapi.com', params=payload3) 
                print("4r") 
                if request.status_code == 404:
                    return None
                else:
                     html_text = request.content
            else:
                 html_text = request.content
        else:
            html_text = request.content
    else:
        html_text = request.content#text #si uso text en vez de content tengo problemas con caracteres español

    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all('div')[22].text #el div 22 tiene la letra
