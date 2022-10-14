from pytube import YouTube
def main():
    y = 0
    x = int(input("Audio(1:sim,0:nao):"))
    audioo = '' if 0 == x else 'progressive="True"'
    qual = []
    link  = input("Link do video:")
    for x in YouTube(link).streams:
        z = str(x)
        l = int(retornarpesquisa(z,'res="',audioo))
        qual.append( l)
    for x in YouTube(link).streams:
        z = str(x)
        k = max(qual)
        if str(k) in z :
            y=x
            break
    y.download('C:\\Users\\Arthur\\Videos')
def retornarpesquisa(frase, acao,audioo):
    location = frase.find(acao)
    location += len(acao)
    name = ''
    name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
    if audioo in name:
        name_t = ''
        for x in name:
            if x == 'p':
                break
            name_t += x
        try:
            if(int(name_t)):
                return name_t.lstrip()
        except ValueError: 
            return 1
    return 1

if __name__=='__main__':
    main()