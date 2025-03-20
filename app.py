import pandas as pd
import streamlit as st
import pickle
import requests

# fetch poster

# def posters(movieid):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZGI2MTdhZjg5OGIwZDhmYjM5YTZhZTU1ZDQzYjFmMyIsIm5iZiI6MTc0MjMyNjYwNi44MTMsInN1YiI6IjY3ZDljYjRlYjNiNGY4MDEwNDBlODgyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.riHEHpGYiDmn8iOkV6KprxLgj8QKe6mpYdx8tgQOzGM&language=en-US".format(movieid)
#     data = requests.get(url)
#
#     data=data.json()
#
#
#
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def posters(movieid):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movieid)


    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZGI2MTdhZjg5OGIwZDhmYjM5YTZhZTU1ZDQzYjFmMyIsIm5iZiI6MTc0MjMyNjYwNi44MTMsInN1YiI6IjY3ZDljYjRlYjNiNGY4MDEwNDBlODgyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.riHEHpGYiDmn8iOkV6KprxLgj8QKe6mpYdx8tgQOzGM"
    }

    data = requests.get(url, headers=headers)
    data = data.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']



# main transferred data

similarity=pickle.load(open('similarity.pkl','rb'))
movies_list=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_list)



# main function

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended=[]
    recommended_poster=[]
    for i in movies_lists:
        moviesid=str(movies.iloc[i[0]].movie_id)
        recommended.append(movies.iloc[i[0]].title)
        recommended_poster.append(posters(moviesid))
    return recommended,recommended_poster


# webpage
st.title("Movie recommender system")
selectedMovie = st.selectbox(
    "Select the movie",
    movies['title'].values,
)

if st.button("Recommend"):
    names,poster=recommend(selectedMovie)


    col1, col2, col3,col4 ,col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(poster[0])

    with col2:
        st.header(names[1])
        st.image(poster[1])

    with col3:
        st.header(names[2])
        st.image(poster[2])

    with col4:
        st.header(names[3])
        st.image(poster[3])

    with col5:
        st.header(names[4])
        st.image(poster[4])
