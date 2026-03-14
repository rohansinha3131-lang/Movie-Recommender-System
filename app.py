from flask import Flask, render_template, request
from recommender import recommend, movie_user_matrix

app = Flask(__name__)

# movie list for autocomplete
movies = movie_user_matrix.index.tolist()

@app.route("/", methods=["GET", "POST"])
def home():

    results = None

    if request.method == "POST":

        movie = request.form.get("movie")

        if movie is None or movie.strip() == "":
            results = [("Please enter a movie name", 0)]
        else:
            results = recommend(movie)

    return render_template("index.html", results=results, movies=movies)


if __name__ == "__main__":
    app.run(debug=True)