import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Charger et nettoyer les données
# Charger et nettoyer les données
def load_and_clean_data(filepath):
    # Charger le dataset
    movies_df = pd.read_csv(filepath)

    # Nettoyer les colonnes avec des espaces dans les noms
    movies_df.columns = movies_df.columns.str.strip()

    # Nettoyer la colonne 'genres'
    movies_df['genres'] = movies_df['genres'].str.strip("[]").str.replace("'", "").str.replace(",", " ").fillna("")

    # Nettoyer la colonne 'keywords'
    movies_df['keywords'] = movies_df['keywords'].str.strip("[]").str.replace("'", "").str.replace(",", " ").fillna("")

    # Nettoyer la colonne 'overview'
    movies_df['overview'] = movies_df['overview'].fillna("")

    # Normaliser les titres (en minuscule pour la recherche insensible à la casse)
    movies_df['title_normalized'] = movies_df['title'].str.lower()

    # Combiner les colonnes pertinentes pour créer la colonne 'features'
    movies_df['features'] = (
        movies_df['genres'] + " " +
        movies_df['keywords'] + " " +
        movies_df['overview']
    )

    return movies_df
import urllib.parse  # Pour encoder les titres correctement

def run_streamlit_app(movies_df, similarity_matrix, tfidf_vectorizer, tfidf_matrix, threshold=0.1):
    st.title("Système de Recommandation de Films 🎥")

    st.markdown("""
    Bienvenue dans le système de recommandation de films !
    - **Option 1 :** Recherchez des films similaires par leur titre.
    - **Option 2 :** Recherchez des films similaires à partir de mots-clés.
    """)

    search_type = st.radio("Choisissez une méthode de recherche :", ["Par Titre", "Par Mots-clés"])

    if search_type == "Par Titre":
        title = st.text_input("Entrez le titre du film :").strip().lower()

        if st.button("Rechercher par Titre"):
            if title in movies_df['title_normalized'].values:
                st.subheader(f"Films similaires à '{title}':")
                title_index = movies_df[movies_df['title_normalized'] == title].index[0]
                similarity_scores = similarity_matrix[title_index]
                
                # Appliquer le seuil
                similar_indices = [
                    idx for idx, score in enumerate(similarity_scores)
                    if score >= threshold and idx != title_index
                ]
                similar_indices = sorted(similar_indices, key=lambda idx: similarity_scores[idx], reverse=True)[:5]

                if not similar_indices:
                    st.warning(f"Aucun film trouvé avec un score de similarité ≥ {threshold}.")
                else:
                    for i, idx in enumerate(similar_indices, start=1):
                        similar_movie = movies_df.iloc[idx]
                        encoded_title = urllib.parse.quote(similar_movie['title'])  # Encodage URL

                        # Afficher les informations du film
                        st.write(f"### {i}. {similar_movie['title']}")
                        st.write(f"   - **Genres :** {similar_movie['genres']}")
                        st.write(f"   - **Mots-clés :** {similar_movie['keywords']}")
                        st.write(f"   - **Résumé :** {similar_movie['overview']}")

                        # Ajouter les boutons dynamiques pour les plateformes
                        st.markdown(
                            f"""
                            <style>
                            .button-container {{
                                display: flex;
                                gap: 10px;
                                margin-top: 10px;
                            }}
                            .button-container a {{
                                text-decoration: none;
                                padding: 10px 15px;
                                border: 1px solid #ddd;
                                border-radius: 5px;
                                color: white;
                                font-weight: bold;
                                text-align: center;
                            }}
                            .google {{
                                background-color: #4285F4;
                            }}
                            .justwatch {{
                                background-color: #f39c12;
                            }}
                            .imdb {{
                                background-color: #f5c518;
                                color: black;
                            }}
                            </style>
                            <div class="button-container">
                                <a class="google" href="https://www.google.com/search?q={encoded_title} watch online" target="_blank">🔍 Google</a>
                                <a class="justwatch" href="https://www.justwatch.com/us/search?q={encoded_title}" target="_blank">📺 JustWatch</a>
                                <a class="imdb" href="https://www.imdb.com/find?q={encoded_title}" target="_blank">🎬 IMDb</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.warning(f"Le film '{title}' n'existe pas dans la base de données.")

    elif search_type == "Par Mots-clés":
        keywords = st.text_input("Entrez des mots-clés (séparés par des espaces) :")

        if st.button("Rechercher par Mots-clés"):
            if keywords:
                keywords_vector = tfidf_vectorizer.transform([keywords])
                similarity_scores = cosine_similarity(keywords_vector, tfidf_matrix)[0]

                # Appliquer le seuil
                similar_indices = [
                    idx for idx, score in enumerate(similarity_scores)
                    if score >= threshold
                ]
                similar_indices = sorted(similar_indices, key=lambda idx: similarity_scores[idx], reverse=True)[:5]

                if not similar_indices:
                    st.warning(f"Aucun film trouvé avec un score de similarité ≥ {threshold}.")
                else:
                    st.subheader(f"Films similaires pour les mots-clés : '{keywords}'")
                    for i, idx in enumerate(similar_indices, start=1):
                        similar_movie = movies_df.iloc[idx]
                        encoded_title = urllib.parse.quote(similar_movie['title'])  # Encodage URL

                        # Afficher les informations du film
                        st.write(f"### {i}. {similar_movie['title']}")
                        st.write(f"   - **Genres :** {similar_movie['genres']}")
                        st.write(f"   - **Mots-clés :** {similar_movie['keywords']}")
                        st.write(f"   - **Résumé :** {similar_movie['overview']}")

                        # Ajouter les boutons dynamiques pour les plateformes
                        st.markdown(
                            f"""
                            <style>
                            .button-container {{
                                display: flex;
                                gap: 10px;
                                margin-top: 10px;
                            }}
                            .button-container a {{
                                text-decoration: none;
                                padding: 10px 15px;
                                border: 1px solid #ddd;
                                border-radius: 5px;
                                color: white;
                                font-weight: bold;
                                text-align: center;
                            }}
                            .google {{
                                background-color: #4285F4;
                            }}
                            .justwatch {{
                                background-color: #f39c12;
                            }}
                            .imdb {{
                                background-color: #f5c518;
                                color: black;
                            }}
                            </style>
                            <div class="button-container">
                                <a class="google" href="https://www.google.com/search?q={encoded_title} watch online" target="_blank">🔍 Google</a>
                                <a class="justwatch" href="https://www.justwatch.com/us/search?q={encoded_title}" target="_blank">📺 JustWatch</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.warning("Veuillez entrer des mots-clés pour effectuer une recherche.")


# Calculer la similarité cosine
def calculate_similarity(movies_df):
    # Vectorisation TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['features'])

    # Calcul de la similarité cosine
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return similarity_matrix, tfidf_vectorizer, tfidf_matrix

# Charger les données et lancer l'application
if __name__ == "__main__":
    # Remplacez 'clean_data.csv' par le chemin vers votre fichier CSV
    filepath = "clean_data.csv"
    movies_df = load_and_clean_data(filepath)

    # Calculer la similarité
    similarity_matrix, tfidf_vectorizer, tfidf_matrix = calculate_similarity(movies_df)

    # Lancer Streamlit
    run_streamlit_app(movies_df, similarity_matrix, tfidf_vectorizer, tfidf_matrix)
