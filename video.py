from pytube import YouTube
import os
def main():
    audio = 0
    video = 0
    audioo = '' 
    qual = []
    qualaudio = []
    link  = input("Link do video:")
    filename = input("Nome do video final:")
    onlyaudio = int(input("Apenas audio digite 1, para video com melhor qualidade digite 0, caso queira video normal digite qualquer número: ")) 
    linkstream = YouTube(link).streams
    audioo = '' if onlyaudio in [0,1] else 'progressive="True"'
    for x in linkstream:
        z = str(x)
        try :
            l = int(retornarpesquisa(z,'res="',audioo))
            qual.append( l)
        except:
            pass
    for x in linkstream:
        z = str(x)
        try :
            l = int(retornarpesquisa(z,'abr="','type="audio"'))
            qualaudio.append(l)
        except:
            pass
    for x in linkstream:
        z = str(x)
        k = max(qual)
        if (str(k)+'p') in z :
            video=x
            break
    for x in linkstream:
        z = str(x)
        k = max(qualaudio)
        if (str(k)+'kbps') in z :
            audio=x
            break
    audiotype = (retornarpesquisa(str(audio), 'mime_type="audio/','XXXXXX'))
    audiotype= audiotype[0:audiotype.find('"')]
    videoptype = (retornarpesquisa(str(video), 'mime_type="video/','XXXXXX'))
    videoptype= videoptype[0:videoptype.find('"')]
    if onlyaudio == 1:
        audio.download('C:\\Users\\Arthur\\Videos',filename = filename+'.'+audiotype)
        if audiotype != 'mp3':
            src = ('C:\\Users\\Arthur\\Videos\\'+filename+'.'+audiotype)
            dst = ('C:\\Users\\Arthur\\Videos\\'+filename+'.mp3')
            import subprocess
            print(subprocess.run(f'ffmpeg -i "{src}" "{dst}"',shell=True,capture_output=True))
            os.remove('C:/Users/Arthur/Videos/'+filename+'.'+audiotype)
    elif onlyaudio==0:
        audio.download('C:\\Users\\Arthur\\Videos',filename = filename+'propad.'+audiotype)
        video.download('C:\\Users\\Arthur\\Videos',filename = filename+'prop.'+videoptype)
        import moviepy.editor as mpe
        #source::https://www.programcreek.com/python/example/105718/moviepy.editor.VideoFileClip Example no 6 ||https://stackoverflow.com/questions/28219049/combining-an-audio-file-with-video-file-in-python
        my_clip = mpe.VideoFileClip('C:/Users/Arthur/Videos/'+filename+'prop.'+videoptype)
        audio_background = mpe.AudioFileClip('C:/Users/Arthur/Videos/'+filename+'propad.'+audiotype)
        final_clip = my_clip.set_audio(audio_background)
        print(final_clip.write_videofile('C:/Users/Arthur/Videos/'+filename+'.mp4'))
        os.remove('C:/Users/Arthur/Videos/'+filename+'prop.'+videoptype)
        os.remove('C:/Users/Arthur/Videos/'+filename+'propad.'+audiotype)
    else:
        video.download('C:\\Users\\Arthur\\Videos',filename = filename+'.'+videoptype)
def retornarpesquisa(frase, acao,audioo):
    location = frase.find(acao)
    location += len(acao)
    name = ''
    name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
    if audioo in name:
        name_t = ''
        for i in range(len(name)):
            x=name[i]
            if x =='p'or (x=='k'and name[i+1]=='b'):
                break
            name_t += x
        try:
            if(int(name_t)):
                return name_t.lstrip()
        except ValueError: 
            return 1
    return name

if __name__=='__main__':
    main()