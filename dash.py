import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud

from testing_modules import get_context_stop_words


df = pd.read_csv("Tweets_Output.csv")

company_sentiment_count = {}

for company in df["company"].unique():
    company_sentiment_count[company] = df.loc[
        df["company"] == company, "sentiment"
    ].value_counts()

company_negative_reasons = {}

for company in df["company"].unique():
    company_negative_reasons[company] = df.loc[
        df["company"] == company, "negativereason"
    ].value_counts()


def generate_company_sentiment_count_bar_chart(company, filtered_df):
    companies = list(filtered_df["company"].unique())
    companies.sort()

    try:
        sentiments = (
            filtered_df[["company", "sentiment", "cleaned_text"]]
            .groupby(["company", "sentiment"])
            .count()
            .to_dict()["cleaned_text"]
        )

        print(sentiments)

    except:
        sentiments = (
            df[["sentiment", "cleaned_text"]].groupby(["sentiment"]).count().to_dict()
        )["cleaned_text"]

        sentiments[(company, "positive")] = sentiments["positive"]
        sentiments[(company, "neutral")] = sentiments["neutral"]
        sentiments[(company, "negative")] = sentiments["negative"]

    stacked_barchart_df = pd.DataFrame(
        {
            "Company": companies,
            "Positive": [
                sentiments[(i, j)] for i, j in sentiments.keys() if j == "positive"
            ],
            "Negative": [
                sentiments[(i, j)] for i, j in sentiments.keys() if j == "negative"
            ],
            "Neutral": [
                sentiments[(i, j)] for i, j in sentiments.keys() if j == "neutral"
            ],
        }
    )

    data = pd.melt(
        stacked_barchart_df.reset_index(),
        id_vars=["Company"],
        value_vars=["Positive", "Negative", "Neutral"],
        value_name="No of Tweets",
        var_name="Sentiment",
    )

    custom_color_palette = ["#fd463b", "#979690", "#118dff"]

    st.markdown(f"### **{company} Sentiments**")

    chart = (
        alt.Chart(data, height=400, width=900)
        .mark_bar()
        .encode(
            x="No of Tweets:Q",
            y="Company:N",
            color=alt.Color("Sentiment:N", scale=alt.Scale(range=custom_color_palette)),
            order=alt.Order("Sentiment", sort="descending"),
        )
    )
    return chart


def generate_company_negative_reasons_donut_chart(company, filtered_df):
    reasons = (
        filtered_df[["negativereason", "cleaned_text"]]
        .groupby(["negativereason"])
        .count()
        .to_dict()["cleaned_text"]
    )

    total = sum(list(reasons.values()))

    reasons = {i: round((reasons[i] / total), 2) * 100 for i in reasons.keys()}

    source = pd.DataFrame(
        {"Reason": list(reasons.keys()), "Percentage": list(reasons.values())}
    )

    st.markdown(f"### **{company} Negative sentiment reasons**")

    chart = (
        alt.Chart(source, height=400, width=700)
        .mark_arc()
        .encode(
            theta=alt.Theta(field="Percentage", type="quantitative"),
            color=alt.Color(field="Reason", type="nominal"),
        )
    )

    return chart


from nltk.corpus import stopwords
import string


STOP_WORDS_P = []
nltk_words = list(stopwords.words("english"))
STOP_WORDS_P.extend(nltk_words)

STOP_WORDS_P.extend(["i", "u", "amp", "us"])

STOP_WORDS = []


for stop_word in STOP_WORDS_P:
    temp_word = ""
    for char in stop_word:
        if char not in string.punctuation:
            temp_word += char
    STOP_WORDS.append(temp_word)

STOP_WORDS += get_context_stop_words(
    df,
    "sentiment",
    "cleaned_text",
    ["positive", "negative", "neutral"],
    STOP_WORDS + STOP_WORDS_P,
)


def generate_wordCloud(dataset, company, sentiment_col, text_col, sentiment):
    stop_words = STOP_WORDS + STOP_WORDS_P

    new_df = dataset[dataset[sentiment_col] == sentiment]

    words = " ".join(new_df[text_col])
    cleaned_word = " ".join([word for word in words.split()])

    st.markdown(
        f"### **Word Cloud of {sentiment.title()} words by {company} customers**"
    )

    wordcloud = (
        WordCloud(
            stopwords=stop_words,
            width=4500,
            height=3500,
        )
        .generate(cleaned_word)
        .to_image()
    )

    return wordcloud


st.title("Twitter Sentiment Analysis Dashboard")

companies = list(company_sentiment_count.keys())
companies.sort()

company_radio_buttons = st.radio("Select Company", ["All"] + companies)

if company_radio_buttons == "All":
    filtered_df = df
else:
    filtered_df = df.loc[df["company"] == company_radio_buttons]

# Bar chart

st.altair_chart(
    generate_company_sentiment_count_bar_chart(company_radio_buttons, filtered_df)
)

# Pie chart

st.altair_chart(
    generate_company_negative_reasons_donut_chart(company_radio_buttons, filtered_df)
)

# Word clouds

st.image(
    generate_wordCloud(
        filtered_df, company_radio_buttons, "sentiment", "cleaned_text", "positive"
    )
)
st.image(
    generate_wordCloud(
        filtered_df, company_radio_buttons, "sentiment", "cleaned_text", "negative"
    )
)
