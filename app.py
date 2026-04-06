import pandas as pd
import streamlit as st
import pickle
import requests

# ------------------ Fetch Poster ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a04f469a10dad9cf77dffb45b00e6e3e&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# ------------------ Recommend Function ------------------ #
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id   # dataset has id column
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ------------------ Load Data ------------------ #
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# ------------------ UI ------------------ #
st.title("🍿 Movie Recommendation System")

option = st.selectbox(
    "Select a movie",
    movies['title'].values
)


# ------------------ Button ------------------ #
if st.button("Recommend 🎬"):

    names, posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)

    for col, name, poster in zip(
        [col1, col2, col3, col4, col5],
        names,
        posters
    ):
        with col:
            st.text(name)
            st.image(poster)