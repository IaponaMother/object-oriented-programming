from time import sleep
import datetime, pyglet
from pyglet.media import Player


class Musical_Composition:

    def __init__(self, name, author, genre, is_words, size, date, path=None, album=None):
        self.name = name
        self.author = author
        self.genre = genre
        self.is_words = is_words
        self.size = size
        self.date = date
        self.path = path
        self.album = album

    def __str__(self):
        print(f"Название композиции: {self.name} \nАвтор: {self.author} \nЖанр: {self.genre} \n"
              f"Размер: {self.size} MB \nГод создания: {self.date} \n \n ")

    def play(self, reps=1):

        if self.is_words:
            player = Player()
            song = pyglet.media.load(self.path, streaming=False)
            for i in range(reps):
                player.queue(song)

            player.play()
            sleep(15)
            pyglet.app.exit()


class Albums:
    def __init__(self, *args):
        print(args)
        

Best_of_Tokio_Hotel = Albums('Durch Den Monsun', 'Der Letzte Tag', 'Madchen Aus Dem All', 'Ubers Ende Der Welt', 'Schrei',
'Spring Nicht', 'Automatisch', 'Ich Brech Aus', 'Rette Mich', '1000 Meere', 'Коmm', 'Sonnensystem')

new_composition1 = Musical_Composition("Schrei", "Tokio Hotel", "поп-рок", True, 8, datetime.date(2009, 10, 9),
                                       'TokioHotel_Schrei.mp3', Best_of_Tokio_Hotel)

new_composition2 = Musical_Composition("Clair de Lune", "Debussy", "классическая музыка", False, 9,
                                       datetime.date(1890, 1, 1), None, None)

compositions = [new_composition1, new_composition2]
for c in compositions:
    c.__str__()
    c.play()
