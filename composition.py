from time import sleep
import datetime, pyglet
from pyglet.media import Player
from abc import ABC


class Album(ABC):
    def __init__(self, name, date, songs, author):
        self.name = name
        self.date = date
        self.songs = songs
        self.author = author

    def __str__(self):
        return "{}".format(", ".join(self.songs))



class LiveAlbum(Album):
    def __init__(self, name, date, songs, town, country, link, author):
        self.town = town
        self.country = country
        self.link = link
        super().__init__(name, date, songs, author)


    def __str__(self):
        return "{} \n{} \n{}".format(", ".join(self.songs), self.town, self.link)



class BestSongs(Album):
    def __init__(self, name, date, songs, links, numbers_of_views, author):
        self.links = links
        self.numbers_of_views = numbers_of_views
        super().__init__(name, date, songs, author)

    def __str__(self):
        return "{} \n{} \n{}".format(", ".join(self.songs), self.links, self.numbers_of_views)



class MusicalComposition:
    def __init__(self, name, author, genre, has_words, size, date, album=None):
        self.name = name
        self.author = author
        self.genre = genre
        self.has_words = has_words
        self.size = size
        self.date = date
        self.album = album

    def __str__(self):
        return 'Название композиции: {}, \nАвтор: {}, \nЖанр: {}, \nРазмер: {} MB,  \nГод создания: {}, \n{} \n \n'.format\
            (self.name, self.author, self.genre, self.size, self.date, 'есть слова' if self.has_words else 'нет слов')



class Play:
    def __init__(self, path):
        self.path = path

    def play(self):
        player = Player()
        song = pyglet.media.load(self.path, streaming=False)
        player.queue(song)
        player.play()
        sleep(5)
        pyglet.app.exit()


new_album1 = BestSongs('Best Of Tokio Hotel', datetime.date(2010, 12, 13),
['Durch Den Monsun', 'Der Letzte Tag', 'Ubers Ende Der Welt', 'Schrei', 'Spring Nicht', 'Automatisch', '1000 Meere'], ["https://www.youtube.com/watch?v=S_Sy5-sOodA", "https://www.youtube.com/watch?v=L-6u66Y6ofc",
 "https://www.youtube.com/watch?v=eJ2zsclf93Q", "https://www.youtube.com/watch?v=suRNNOeDIEA", "https://www.youtube.com/watch?v=rdTyUamjssc",
"https://www.youtube.com/watch?v=WhIlqBqRtuw", "https://www.youtube.com/watch?v=TnUJ1vU0npI"], [22549392, 3267562,
2573936, 5117275, 4983572, 19826613, 3781939], 'Tokio Hotel')

new_album2 = LiveAlbum('Live in Texas', datetime.date(2003, 11, 18), ['Somewhere I belong', 'Points of Authority',
                    'Runaway', 'Faint', 'Numb', 'Crawling', 'In the End'], "Texas", "America", "https://www.youtube.com/watch?v=7Mxg4VkkRRI", 'Linkin Park')

new_composition1 = MusicalComposition("Schrei", "Tokio Hotel", "поп-рок", True, 8, datetime.date(2009, 10, 9), new_album1)


compositions = [new_composition1]
albums = [new_album1, new_album2]
for c in compositions:
    print(c)


for a in albums:
    print(a)

while True:
    p1 = ''
    answer = str(input("хотите воспроизвести песню? (да/нет)  "))
    if answer == "да":
        for a in albums:
            print(str(a.name) + "\n")
        album_name = str(input("введите название альбома: "))
        for a in albums:
            if a.name == album_name:
                p = str(a.author)
                print(p)
                for s in a.songs:
                    print(s)
                song_name = str(input("введите название песни: "))
                for s in a.songs:
                    if s == song_name:
                        p += '_' + str(s) + '.mp3'
                        p = "".join(p.split())
                        S = Play(p)
                        S.play()
    else:
        break
