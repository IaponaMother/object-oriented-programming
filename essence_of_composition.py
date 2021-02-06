import datetime
class Musical_Composition:

    def __init__(self, name, author, genre, words, size, date):
        self.name = name
        self.author = author
        self.genre = genre
        self.words = words
        self.size = size
        self.date = date

    def str(self):
        print(f"Название композиции: {self.name} \nАвтор: {self.author} \nЖанр: {self.genre} \n"
              f"Размер: {self.size} MB \nГод создания: {self.date}")
        if self.words:
            print("В композиции есть слова \n\n")
        else:
            print("В композиции нет слов \n\n")

newComposition1 = Musical_Composition("Schrei", "Tokio Hotel", "поп-рок", True, 8, datetime.date(2009, 10, 9))
newComposition2 = Musical_Composition("Clair de Lune", "Debussy", "классическая музыка", False, 9, datetime.date(1890, 1, 1))
Compositions = [newComposition1, newComposition2]
for c in Compositions:
    c.str()
