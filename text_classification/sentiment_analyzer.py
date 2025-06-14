import torch
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

# Use a pipeline as a high-level helper
from transformers import pipeline

model_path = ("../models/models--distilbert--distilbert-base-uncased-finetuned-sst-2-english/snapshots/"
              "714eb0fa89d2f80546fda750413ed43d93601a13")
analyzer = pipeline("text-classification", model=model_path)

#print(analyzer(["This product is good", "This product was quite expensive"]))

def sentiment_analyzer(review):
    sentiment = analyzer(review)
    return sentiment[0]['label']

def sentiment_bar_chart(df):
    sentiment_counts = df['Sentiment'].value_counts()

    # Create a bar chart
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', color=['green', 'red'])
    ax.set_title('Review Sentiment Counts')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    # ax.set_xticklabels(['Positive', 'Negative'], rotation=0)

    # Return the figure object
    return fig

def read_reviews_and_analyze_sentiment(file_object):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_object)

    # Check if 'Review' column is in the DataFrame
    if 'review' not in df.columns:
        raise ValueError("Excel file must contain a 'review' column.")

    # Apply the get_sentiment function to each review in the DataFrame
    df['Sentiment'] = df['review'].apply(sentiment_analyzer)
    chart_object = sentiment_bar_chart(df)
    return df, chart_object

print(read_reviews_and_analyze_sentiment("../Files/reviews.xlsx"))

demo = gr.Interface(fn=read_reviews_and_analyze_sentiment,
                    inputs=[gr.File(file_types=[".xlsx"], label="Upload your review comment file")],
                    outputs=[gr.Dataframe(label="Sentiments"), gr.Plot(label="Sentiment Analysis")],
                    title="Sentiment Analyzer",
                    description="THIS APPLICATION WILL BE USED TO ANALYZE THE SENTIMENT BASED ON FILE UPLAODED.")

demo.launch()
#pipe = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")