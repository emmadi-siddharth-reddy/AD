import sys
import os
import pandas as pd
from data_loader import load_data
from recommendation import build_recommendation_system

def main():
    # Add the src directory to the system path if running from a different location
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    
    # Load the dataset
    file_path = 'data/movies.csv'
    df = load_data(file_path)
    
    # Build the recommendation system
    recommend_movies = build_recommendation_system(df)
    
    # User input
    user_input = input("Enter the movie you liked: ")
    recommendations = recommend_movies(user_input)
    
    if isinstance(recommendations, str):
        print(recommendations)
    else:
        print("Recommended movies:")
        for movie in recommendations:
            print(movie)

if __name__ == "__main__":
    main()
