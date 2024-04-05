# nan-mudhalvan

Author : Hariharan T
Dataset : https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment

Documentation : https://github.com/hariharanthangaraj/nan-mudhalvan/Project.ppt

Source Code : https://github.com/hariharanthangaraj/nan-mudhalvan/NMV.ipynb

Predicted Dataset : https://github.com/hariharanthangaraj/nan-mudhalvan/Tweets_Output.csv

Google Colab : https://colab.research.google.com/drive/1vIUKmRqcNrkrG1ftWgilaW6lsZUrEwTd?usp=sharing

StreamLit Deployment : https://airlines-sentiment-analysis.streamlit.app

Problem Definition:
The problem is to perform sentiment analysis on customer feedback to gain insights into competitor products. By understanding customer sentiments, companies can identify strengths and weaknesses in competing products, thereby improving their own offerings. This project requires utilizing various NLP methods to extract valuable insights from customer feedback.

Project Outcomes:
The Project helps companies Visualize and Understand:

Customer satisfaction
Product feedback
Brand perception
Competitive Intelligence
Market Trend Analysis
This information helps the Companies to improve their products and services by observing the performance of Competitor's products among the Public. Thus, improving the Brand’s perception among the Public leads to Profit and Growth of the Company.

Dependancies :
Data Loading and Visualization

Pandas pip install pandas
Numpy pip install numpy
Matplotlib pip install matplotlib
Seaborn pip install seaborn
Text Processing

Demoji pip install demoji
Unicode pip install unicode
Html pip install html
string
re
NLTK pip install nltk
WordCloud pip install wordcloud
Collections
Model Training

PyTorch pip install torch
Transfomers pip install transformers
Deployment

Streamlit pip install streamlit
Vega-Altair pip install altair
How to Execute?
Install the required Dependencies and Dataset.
Execute the Source Code file (NMV.ipynb) to Pre-process the data, Train Data Models and Generate an Input dataset for Visualizing in the Dashboard.
Execute the Dashboard Code file (dash.py), using the following: streamlit run dash.py to create a Dashboard Using Streamlit.
Key Features
Context-Based Stop Words Identification: Identifies and eliminates the top 25 frequently used words in all sentiment categories to enhance analysis relevance.
Emojis and Emoticons Understanding: Analyzes emojis and emoticons to capture nuanced sentiment expressions and improve analysis accuracy.
Negation Handling: Identifies and reverses negation statements in the text to ensure accurate sentiment classification.
Robust Model: Utilize the RoBERTa Deep-Learning Model for higher prediction accuracy.
Interactive Dashboard: Enable targeting specific companies in the dashboard for focused analysis.
Dashboard
![image](https://github.com/hariharanthangaraj/nan-mudhalvan/assets/117925958/77f23c07-1afa-4949-bab9-690c46a83cb8)
