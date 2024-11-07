import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def build_recommendation_system(df):
    # Convert descriptions into TF-IDF features
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Create a series for the movie titles
    indices = pd.Series(df.index, index=df['title']).to_dict()

    def recommend_movies(title, cosine_sim=cosine_sim):
        # Get the index of the movie that matches the title
        idx = indices.get(title)
        if idx is None:
            return "Movie not found in the dataset."

        # Get the pairwise similarity scores for all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 3 most similar movies
        sim_scores = sim_scores[1:4]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 3 most similar movies with ratings
        recommendations = df[['title', 'rating']].iloc[movie_indices].to_dict('records')
        return recommendations

    return recommend_movies
