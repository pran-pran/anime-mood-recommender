import streamlit as st
import pandas as pd
import random

#load dataset
anime_data= pd.read_csv("anime.csv")

#personal watchlist
personal_list = ["Death Note", "Naruto", "My Hero Academia", "Attack on Titan", "One Piece"]

#mood to genre mapping
mood_genre_map = {
    "Sad": ["Drama", "Tragedy", "Romance"],
    "Happy": ["Comedy", "Adventure"],
    "Moody": ["Psychological", "Thriller"],
    "Drama": ["Drama"]
}

st.set_page_config(page_title="Anime Mood Recommender 🎌", layout="centered")
st.title("🎌 Anime Mood Recommender")
st.markdown("Feeling something? Let's match it with the right anime vibe!")

#inputs
mood = st.selectbox("What's your mood?", list(mood_genre_map.keys()))
genre = st.selectbox("Preferred genre (optional)", ["Any"] + sorted(set(g for genres in anime_data['genre'].dropna().str.split(',') for g in genres)))

#personal watchlist input
personal_input = st.text_area(
    "Enter your personal watchlist (separate anime names by commas):",
    placeholder="e.g., Death Note, Naruto, My Hero Academia"
)

#input string to list, stripping whitespace
personal_list = [anime.strip() for anime in personal_input.split(",") if anime.strip()]

#recommendation function
def get_recommendation(mood, genre, n_personal=3, n_general=3):
    mood_genres = mood_genre_map.get(mood, [])
    filtered = anime_data.copy()

    # Filter by genre or mood genres
    if genre != "Any":
        filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
    elif mood_genres:
        pattern = '|'.join(mood_genres)
        filtered = filtered[filtered["genre"].str.contains(pattern, case=False, na=False)]

    from_personal = []
    for anime in personal_list:
        anime_row = anime_data[anime_data['name'] == anime]
        if not anime_row.empty:
            genre_str = anime_row['genre'].values[0]
            if any(mg.lower() in genre_str.lower() for mg in mood_genres):
                from_personal.append(anime)

    from_general = filtered[~filtered['name'].isin(personal_list)]

    # Pick up to n_personal random from personal watchlist matches
    personal_recs = random.sample(from_personal, min(n_personal, len(from_personal))) if from_personal else ["Nothing in your watchlist matched the vibe, sorryy!! :p"]

    # Pick up to n_general random from general filtered list
    if not from_general.empty:
        general_list = from_general['name'].tolist()
        general_recs = random.sample(general_list, min(n_general, len(general_list)))
    else:
        general_recs = ["No new anime watched either, sorryy :p"]

    return personal_recs, general_recs

#output
if st.button("🎲 Recommend Me Something!"):
    personal, new_suggestion = get_recommendation(mood, genre)
    st.subheader("🎞️ From Your Watchlist:")
    st.write(personal)
    st.subheader("🌟 Try This New Anime:")
    st. write(new_suggestion)