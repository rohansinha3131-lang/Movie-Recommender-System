import pickle
from rapidfuzz import process
from scipy.sparse import csr_matrix

model = pickle.load(open("models/knn_model.pkl","rb"))
movie_user_matrix = pickle.load(open("models/movie_matrix.pkl","rb"))

movie_sparse = csr_matrix(movie_user_matrix.values)


def find_movie(movie):

    movies = movie_user_matrix.index.tolist()

    match = process.extractOne(movie, movies)

    # match = (movie_name, score, index)

    if match[1] < 60:   # threshold
        return None

    return match[0]


def recommend(movie):

    movie = find_movie(movie)

    movie_index = movie_user_matrix.index.get_loc(movie)

    distances, indices = model.kneighbors(
        movie_sparse[movie_index],
        n_neighbors=6
    )

    recommendations = []

    for i in range(1, len(indices[0])):

        movie_name = movie_user_matrix.index[indices[0][i]]

        similarity = 1 - distances[0][i]

        recommendations.append((movie_name, round(similarity,3)))

    return recommendations