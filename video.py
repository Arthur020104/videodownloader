from pytube import YouTube
import os
import subprocess
import moviepy.editor as mpe
from youtubesearchpython import VideosSearch  # Importa a biblioteca para pesquisar vídeos no YouTube

def main():
    audio = 0
    video = 0
    audioo = ''
    qual = []
    qualaudio = []
    
    link = input("Nome do vídeo: ")
    link = link.replace(" ", "_")
    
    # Pesquisa o vídeo no YouTube
    videosSearch = VideosSearch(link, limit = 1)
    link = videosSearch.result()["result"][0]["link"]
    
    filename = input("Nome do vídeo final: ")
    onlyaudio = int(input("Apenas áudio digite 1, para vídeo com melhor qualidade digite 0, caso queira vídeo normal digite qualquer número: "))
    
    print(link)
    linkstream = YouTube(link).streams
    audioo = '' if onlyaudio in [0, 1] else 'progressive="True"'
    
    for x in linkstream:
        z = str(x)
        try:
            l = int(retornarpesquisa(z, 'res="', audioo))
            qual.append(l)
        except:
            pass
            
    for x in linkstream:
        z = str(x)
        try:
            l = int(retornarpesquisa(z, 'abr="', 'type="audio"'))
            qualaudio.append(l)
        except:
            pass
            
    for x in linkstream:
        z = str(x)
        k = max(qual)
        if (str(k) + 'p') in z:
            video = x
            break
            
    for x in linkstream:
        z = str(x)
        k = max(qualaudio)
        if (str(k) + 'kbps') in z:
            audio = x
            break
            
    audiotype = (retornarpesquisa(str(audio), 'mime_type="audio/', 'XXXXXX'))
    audiotype = audiotype[0:audiotype.find('"')]
    videoptype = (retornarpesquisa(str(video), 'mime_type="video/', 'XXXXXX'))
    videoptype = videoptype[0:videoptype.find('"')]
    
    if onlyaudio == 1:
        audio.download(f"{path}/Videos", filename=filename + '.' + audiotype)
        if audiotype != 'mp3':
            src = (f"{path}/Videos/" + filename + '.' + audiotype)
            dst = (f"{path}/Videos/" + filename + '.mp3')
            subprocess.run(f'ffmpeg -i "{src}" "{dst}"', shell=True, capture_output=False)
            os.remove(f"{path}/Videos/" + filename + '.' + audiotype)
        return
    elif onlyaudio == 0:
        audio.download(f"{path}/Videos", filename=filename + 'propad.' + audiotype)
        video.download(f"{path}/Videos", filename=filename + 'prop.' + videoptype)
        my_clip = mpe.VideoFileClip(f"{path}/Videos/" + filename + 'prop.' + videoptype)
        audio_background = mpe.AudioFileClip(f"{path}/Videos/" + filename + 'propad.' + audiotype)
        final_clip = my_clip.set_audio(audio_background)
        print(final_clip.write_videofile(f"{path}/Videos/" + filename + '.mp4'))
        os.remove(f"{path}/Videos/" + filename + 'prop.' + videoptype)
        os.remove(f"{path}/Videos/" + filename + 'propad.' + audiotype)
    else:
        video.download(f"{path}/Videos", filename=filename + '.' + videoptype)

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
    main()
