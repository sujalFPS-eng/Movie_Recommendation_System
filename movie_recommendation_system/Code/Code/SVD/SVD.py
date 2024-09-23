from surprise import SVD
from Singular_Value_Decomposition.MovieDataset import MovieDataset


def build_testset_not_in_training(subject, trainingSet):
    place = trainingSet.global_mean

    testset = []

    userid = trainingSet.to_inner_uid(str(subject))
    items = set([j for (j, _) in trainingSet.ur[userid]])

    testset += [(trainingSet.to_raw_uid(userid), trainingSet.to_raw_iid(i), place) for
                     i in trainingSet.all_items() if
                     i not in items]
    return testset


testUser = 5
ml = MovieDataset()

movie_data = ml.load_dataset()

# Loading movie ratings from csv for the randomaly picked testUser number 5
userRatings = ml.get_ratings_from_user(testUser)

likedMovies = []
dislikedMovies = []

for ratings in userRatings:
    if (float(ratings[1]) > 4.0):
        likedMovies.append(ratings)
    if (float(ratings[1]) < 3.0):
        dislikedMovies.append(ratings)

print('\nUser {} liked these movies:'.format(testUser))
for movieId in likedMovies:
    print(ml.get_movie_name_by_Id(movieId[0]))

print('\nUser {} Disliked these movies:'.format(testUser))
for movieId in dislikedMovies:
    print(ml.get_movie_name_by_Id(movieId[0]))

# constructing recommendation model for user
trainingSet = movie_data.build_full_trainset()

svd = SVD()
svd.fit(trainingSet)

#calculating recommendations for the user from the training set`
testSet = build_testset_not_in_training(testUser, trainingSet)
predictions = svd.test(testSet)

recommendations = []

print('\nRecommendations:')
for u_ID, m_ID, a_rating, e_rating, _ in predictions:
    intm_ID = int(m_ID)
    recommendations.append((intm_ID, e_rating))

recommendations.sort(key=lambda p: p[1], reverse=True)

for ratings in recommendations[:8]:
    print(ml.get_movie_name_by_Id(ratings[0]))
