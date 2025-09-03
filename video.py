from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import os
import subprocess
import moviepy.editor as mpe
from youtubesearchpython import VideosSearch# Importa a biblioteca para pesquisar vídeos e playlists no YouTube

def main(path):
    typeOfDownload = requestUntilInput("Tipo de download (0 - Vídeo com melhor qualidade, 1 - Apenas áudio, 2 - Playlist): ", "Por favor, insira um número 0, 1 ou 2.", int)

    videoLink = requestUntilInput("Nome do vídeo: " if typeOfDownload != 2 else "URL da playlist: ", "Por favor, insira um nome válido." if typeOfDownload != 2 else "Por favor, insira um URL válido.", str)


    # Pesquisa o vídeo no YouTube
    if typeOfDownload != 2:
        videosSearch = VideosSearch(videoLink, limit = 20)
        if not videosSearch.result()["result"]:
            print("Nenhum resultado encontrado.")
            return
        else:
            for count, video in enumerate(videosSearch.result()["result"], start=1):
                print(f"{count}. {video['title']} ({video['link']})")

        videoChoice = requestUntilInput("Escolha o número do vídeo que deseja baixar: ", "Por favor, insira um número válido.", int)
        videoLink = videosSearch.result()["result"][videoChoice - 1]["link"]


    yt = YouTube(videoLink, client='WEB', use_oauth=True) if typeOfDownload != 2 else  Playlist(videoLink, client='WEB', use_oauth=True)

    if not isinstance(yt, Playlist):
        yt = [yt]
    else:
        yt = yt.videos

    quality = 3 #high quality with audio
    if typeOfDownload in [0, 2]:
        quality = requestUntilInput("Qualidade (0 - Muito Alta(tempo de espera alto), 1 - Alta: ", "Por favor, insira um número válido.", int)
        quality = quality if quality != 1 else 3
    
    for video in yt:
        videoTitle = video.title#.replace('|', '').replace('"', '').replace('?', '').replace('*', '').replace('<', '').replace('>', '').replace(':', '').replace('/', '').replace('\\', '')
        print(f"Baixando: {videoTitle}")
        downloadVideo(video.streams, quality, f"{path}/Videos/", videoTitle)

def requestUntilInput(prompt, messageError, typeOfInput):
    while True:
        try:
            return typeOfInput(input(prompt))
        except ValueError:
            print(messageError)

def downloadVideo(linkstream, onlyaudio, path, filename):
    qualVideo = []
    qualAudio = []

    audioo = '' if onlyaudio in [0, 1] else 'progressive="True"'

    #Refatorar esta parte, TODO revisao do codigo(nao lembro como funciona)
    for x in linkstream:
        z = str(x)
        try:
            l = int(retornarpesquisa(z, 'res="', audioo))
            qualVideo.append(l)
        except:
            pass
            
    for x in linkstream:
        z = str(x)
        try:
            l = int(retornarpesquisa(z, 'abr="', 'type="audio"'))
            qualAudio.append(l)
        except:
            pass
            
    for x in linkstream:
        z = str(x)
        k = max(qualVideo)
        if (str(k) + 'p') in z:
            video = x
            break
            
    for x in linkstream:
        z = str(x)
        k = max(qualAudio)
        if (str(k) + 'kbps') in z:
            audio = x
            break
            
    audiotype = (retornarpesquisa(str(audio), 'mime_type="audio/', 'XXXXXX'))
    audiotype = audiotype[0:audiotype.find('"')]
    videoptype = (retornarpesquisa(str(video), 'mime_type="video/', 'XXXXXX'))
    videoptype = videoptype[0:videoptype.find('"')]
    
    if onlyaudio == 1:
        audio.download(path + "Videos", filename=filename + '.' + audiotype)
        if audiotype != 'mp3':
            src = (path + filename + '.' + audiotype)
            dst = (path + filename + '.mp3')
            subprocess.run(f'ffmpeg -i "{src}" "{dst}"', shell=True, capture_output=False)
            os.remove(path + filename + '.' + audiotype)
        return
    elif onlyaudio == 0:
        audio.download(path, filename=filename + 'propad.' + audiotype)
        video.download(path, filename=filename + 'prop.' + videoptype)
        my_clip = mpe.VideoFileClip(path + filename + 'prop.' + videoptype)
        audio_background = mpe.AudioFileClip(path + filename + 'propad.' + audiotype)
        final_clip = my_clip.set_audio(audio_background)
        print(final_clip.write_videofile(path + filename + '.mp4'))
        os.remove(path + filename + 'prop.' + videoptype)
        os.remove(path + filename + 'propad.' + audiotype)
    else:
        video.download(path, filename=filename + '.' + videoptype)


def retornarpesquisa(frase, acao, audioo):
    location = frase.find(acao)
    location += len(acao)
    name = ''
    name = "".join([i if i != "/n" and i != "" else "" for i in frase[location:len(frase)]])
    if audioo in name:
        name_t = ''
        for i in range(len(name)):
            x = name[i]
            if x == 'p' or (x == 'k' and name[i + 1] == 'b'):
                break
            name_t += x
        try:
            if int(name_t):
                return name_t.lstrip()
        except ValueError:
            return 1
    return name

if __name__ == '__main__':
    login = os.getlogin()
    path = f"C:/Usuários/{login}/Área de Trabalho/" if os.path.exists(f"C:/Usuários/{login}/Área de Trabalho/") else f"C:/Users/{login}/OneDrive/Área de Trabalho/" if os.path.exists(f"C:/Users/{login}/OneDrive/Área de Trabalho/") else f"C:/Users/{login}/Desktop/"
    main(path)
