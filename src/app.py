from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from data_loader import load_data
from recommendation import build_recommendation_system

app = Flask(__name__)

# Load the dataset and build the recommendation system
file_path = 'data/movies.csv'
df = load_data(file_path)
recommend_movies = build_recommendation_system(df)

def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    bar_plot = None
    pie_chart = None
    if request.method == 'POST':
        user_input = request.form.get('movie')
        recommendations = recommend_movies(user_input)

        if isinstance(recommendations, list) and recommendations:
            titles = [rec['title'] for rec in recommendations]
            ratings = [rec['rating'] for rec in recommendations]

            # Bar Plot
            fig, ax = plt.subplots()
            sns.barplot(x=titles, y=ratings, ax=ax)
            ax.set_xlabel('Movies')
            ax.set_ylabel('Ratings')
            ax.set_title('Recommended Movies with Ratings')
            bar_plot = plot_to_base64(fig)
            plt.close(fig)

            # Pie Chart
            fig, ax = plt.subplots()
            sizes = [rating for rating in ratings]
            ax.pie(sizes, labels=titles, autopct='%1.1f%%', startangle=140)
            ax.set_title('Rating Distribution of Recommended Movies')
            pie_chart = plot_to_base64(fig)
            plt.close(fig)

    return render_template('index.html', recommendations=recommendations, bar_plot=bar_plot, pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)
