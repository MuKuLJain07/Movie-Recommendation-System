import streamlit as st
import pickle as pkl
import pandas as pd
import requests

# Load data
df = pd.read_csv('cleaned_data.csv')
similarity = pkl.load(open('similarity.pkl', 'rb'))



# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=86a1b5a28169d721a6bf484224253ce8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']



# Recommendation function
def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for movie in movie_list:
        recommended_movies_posters.append(fetch_poster(df.iloc[movie[0]].movie_id))
        recommended_movies.append(df.iloc[movie[0]].title)

    return recommended_movies, recommended_movies_posters




# App title and description
st.title("Movie Recommendation System")
st.write("Select a movie from the dropdown below to get recommendations for similar movies.")



# Movie selection dropdown
option = st.selectbox(
    "Choose a movie:",
    df['title']
)


# Recommend button
if st.button("Recommend"):
    st.write(f"Recommendations for '{option}':")
    recommended_movies, recommended_movies_posters = recommend(option)

    # Display recommended movies and posters
    col1, col2, col3, col4, col5   = st.columns(5)

    with col1:
        st.image(recommended_movies_posters[0], use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{recommended_movies[0]}</p>", unsafe_allow_html=True)

    with col2:
        st.image(recommended_movies_posters[1], use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{recommended_movies[1]}</p>", unsafe_allow_html=True)

    with col3:
        st.image(recommended_movies_posters[2], use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{recommended_movies[2]}</p>", unsafe_allow_html=True)

    with col4:
        st.image(recommended_movies_posters[3], use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{recommended_movies[3]}</p>", unsafe_allow_html=True)

    with col5:
        st.image(recommended_movies_posters[4], use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{recommended_movies[4]}</p>", unsafe_allow_html=True)


