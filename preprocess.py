import re
import csv
from collections import defaultdict

counter = 0
counts = defaultdict(int)
genres = ['horror','adventure','fantasy' ,'western','mystery','romance','war','action','thriller','superhero','comedy','drama','crime', 'sci-fi' ]

with open("wiki_movie_plots_deduped.csv", "r", encoding="utf8", newline='') as data:
    with open("movie_preprocess", "w") as f:
        reader = csv.reader(data)
        movies = []
        for a in reader:
            movies.append(a)
        movies = reversed(movies)
        for movie in movies:
            counter = counter + 1
            genre = re.split(r'[/\s,]',movie[5])[0].strip().lower()
            if not genre in genres:
                continue
            year = movie[0]
            title = movie[1]
            origin = movie[2].strip().lower()
            director = movie[3]
            actors = movie[4]
           
            counts[genre] = counts[genre] + 1
            wiki = movie[6]
            plot = re.sub("\n","",movie[7]) 
            if  counts[genre] > 10 and counts[genre] <= 500:
                try:
                    f.write(genre + "  " +
                            title + "  " +
                            director + "  " +
                            actors + "  " +
                            plot + "\n") 
                except:
                    continue
        f.closed
data.closed

   