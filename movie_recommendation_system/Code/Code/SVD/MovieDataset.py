import os
import sys
import csv
from surprise import Dataset
from surprise import Reader

from collections import defaultdict
# class that defines the dataset for the movies and has methods that process the data from the dataset.
class MovieDataset:

    movieID_to_name = {}
    name_to_movieID = {}


    ratingsPath = '../ml-latest-small/ratings.csv'
    moviesPath = '../ml-latest-small/movies.csv'

    # method that reads the ratings of user and movies from the ratings.csv and movies.csv respectively and loads the result into respective arrays/lists

    def load_dataset(self):
        os.chdir(os.path.dirname(sys.argv[0]))

        self.movieID_to_name = {}
        self.name_to_movieID = {}

        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        print(self.moviesPath)
        print(self.ratingsPath)
        ratings_set = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.moviesPath, newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)

            for row in movieReader:
                movieID = int(row[0])
                movieName = row[1]
                self.movieID_to_name[movieID] = movieName
                self.name_to_movieID[movieName] = movieID

        return ratings_set
    # method that returns ratings from particular user whose id has been provided
    def get_ratings_from_user(self, user_id):
        user_ratings = []
        top_user = False

        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)

            for row in ratingReader:
                u_id = int(row[0])
                if (user_id == u_id):
                    movieID = int(row[1])
                    rating = float(row[2])
                    user_ratings.append((movieID, rating))
                    top_user = True

                if (top_user and (user_id != u_id)):
                    break
        return user_ratings

    # method that returns popular ratings from users in the dataset
    def get_popular_rank(self):
        ratings = defaultdict(int)
        ranks = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)

            for row in ratingReader:
                movie_id = int(row[1])
                ratings[movie_id] += 1

            rank = 1
            for movie_id, r_count in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
                ranks[movie_id] = rank
                rank += 1
            return ranks

    # method that returns name of the movie for particular movie id that has been provided
    def get_movie_name_by_Id(self, m_id):
        if m_id in self.movieID_to_name:
            return self.movieID_to_name[m_id]
        else:
            return ""

    # method that returns id of the movie for particular movie name that has been provided
    def get_movieid_by_name(self, movieName):
        if movieName in self.name_to_movieID:
            return self.name_to_movieID[movieName]
        else:
            return 0



# end of code and class