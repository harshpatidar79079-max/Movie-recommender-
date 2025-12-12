import streamlit as st
import pickle
import pandas as pd
import base64

# -----------------------------------------------------------
# Load Required Files
# -----------------------------------------------------------
movies_list = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_df = pd.DataFrame(movies_list)

# -----------------------------------------------------------
# Recommendation Function
# -----------------------------------------------------------
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[index]
    movies_list_sorted = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_titles = []
    for i in movies_list_sorted:
        recommended_titles.append(movies_df.iloc[i[0]].title)
    return recommended_titles


# -----------------------------------------------------------
# Background Image Function
# -----------------------------------------------------------
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# -----------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Background image (must be inside the same folder)
add_bg("bg.jpg")

# -----------------------------------------------------------
# Title Section
# -----------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: white; font-size: 55px;'>
        🎬 Movie Recommender System
    </h1>
    <h3 style='text-align: center; color: #e0e0e0;'>
        Developed by Harsh & Prakhar
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center; color: red; font-weight: bold;'>NETFLIX</h2>",
    unsafe_allow_html=True
)

st.write("")
st.write("")


# -----------------------------------------------------------
# User Input Section
# -----------------------------------------------------------
selected_movie = st.selectbox(
    "Search here to get AI based movie recommendations:",
    movies_df['title'].values,
    key="movie_select"
)

# Button with unique key (to avoid duplicate ID error)
if st.button("Recommend", key="recommend_button"):
    recommendations = recommend(selected_movie)
    st.write("### Recommended Movies:")
    for movie in recommendations:
        st.write("✔ " + movie)
