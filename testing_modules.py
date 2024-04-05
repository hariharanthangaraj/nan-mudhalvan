import nltk
nltk.download('stopwords')

from nltk.corpus import wordnet

import demoji

import unicodedata
import html
import string
import re


text_emoticons = {
    ":)": "smile",
    "=)": "smile",
    "<3": "smile",
    "<3": "heart",
    ":(": "sad",
    ":-)": "smile",
    ":)": "smile",
    ":-]": "smile",
    ":]": "smile",
    ":->": "smile",
    ":>": "smile",
    "8-)": "smile",
    "8)": "smile",
    ":-}": "smile",
    ":}": "smile",
    ":o)": "smile",
    ":c)": "smile",
    ":^)": "smile",
    "=]": "smile",
    "=)": "smile",
    ":-D": "laugh",
    ":D": "laugh",
    "8-D": "laugh",
    "8D": "laugh",
    "=D": "laugh",
    "=3": "laugh",
    "B^D": "laugh",
    "c:": "laugh",
    "C:": "laugh",
    "x-D": "laugh",
    "xD": "laugh",
    "X-D": "laugh",
    "XD": "laugh",
    ":-))": "very happy",
    ":-(": "sad",
    ":(": "sad",
    ":-c": "sad",
    ":c": "sad",
    ":-<": "sad",
    ":<": "sad",
    ":-[": "sad",
    ":[": "sad",
    ":-||": "sad",
    ":{": "sad",
    ":@": "sad",
    ":(": "sad",
    ";(": "sad",
    ":-c": "sad",
    ":'-(": "crying",
    ":'(": "crying",
    ":=(": "crying",
    ":'-)": "tears of happiness",
    ":')": "tears of happiness",
    ':"D': "tears of happiness",
    ">:(": "angry",
    ">:[": "angry",
    ":-O": "shock",
    ":O": "shock",
    ":-o": "shock",
    ":o": "shock",
    ":-0": "shock",
    ":0": "shock",
    "8-0": "shock",
    ">:O": "shock",
    "=O": "shock",
    "=o": "shock",
    "=0": "shock",
    ":c": "shock",
    ":-<": "shock",
    ":<": "shock",
    ":-[": "shock",
    ":[": "shock",
    ":-||": "shock",
    ":{": "shock",
    ":@": "shock",
    ":(": "shock",
    ";(": "shock",
    ">:3": "smile",
    ":-*": "kiss",
    ":*": "kiss",
    ":x": "kiss",
    ":-|": "no expression",
    ":|": "no expression",
    "%-)": "confused",
    "%)": "confused",
    "</3": "broken heart",
    "<\\3": "broken heart",
    "@>-->--": "rose",
    "@}-;-'---": "rose",
    "@}->--": "rose",
    "@};-": "rose",
    "(>_<)": "trouble",
    "(>_<)>": "trouble",
    "(>w<)": "trouble",
    "^_^": "joyful",
    "(°o°)": "joyful",
    "(^_^)/": "joyful",
    "(^O^)/": "joyful",
    "(^o^)/": "joyful",
    "(^^)/": "joyful",
    "(≧∇≦)/": "joyful",
    "(/◕ヮ◕)/": "joyful",
    "(^o^)丿": "joyful",
    "∩(·ω·)∩": "joyful",
    "(·ω·)": "joyful",
    "^ω^": "joyful",
    "(ー_ー)!!": "shame",
    "(-.-)": "shame",
    "(-_-)": "shame",
    "(一一)": "shame",
    "(;一_一)": "shame",
}


def decode_label(label):
    if label == 0:
        return "negative"
    if label == 1:
        return "neutral"
    if label == 2:
        return "positive"


def Negation(words):
    temp = int(0)
    for i in range(len(words)):
        if words[i - 1] in ["not", "n't"]:
            antonyms = []
            for syn in wordnet.synsets(words[i]):
                syns = wordnet.synsets(words[i])
                w1 = syns[0].name()
                temp = 0
                for l in syn.lemmas():
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())
                max_dissimilarity = 0
                for ant in antonyms:
                    syns = wordnet.synsets(ant)
                    w2 = syns[0].name()
                    syns = wordnet.synsets(words[i])
                    w1 = syns[0].name()
                    word1 = wordnet.synset(w1)
                    word2 = wordnet.synset(w2)
                    if isinstance(word1.wup_similarity(word2), float) or isinstance(
                        word1.wup_similarity(word2), int
                    ):
                        temp = 1 - word1.wup_similarity(word2)
                    if temp > max_dissimilarity:
                        max_dissimilarity = temp
                        antonym_max = ant
                        words[i] = antonym_max
                        words[i - 1] = ""
    while "" in words:
        words.remove("")
    return words


from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

wnl = WordNetLemmatizer()


def clean_tweets(tweets):
    cleaned_tweets = []

    for tweet in tweets:
        cleaned_words = []

        # html Entities decoding
        tweet = html.unescape(tweet)

        # Emoji decoding

        emoji_dict = demoji.findall(tweet) | text_emoticons

        if emoji_dict:
            for emoji in emoji_dict.keys():
                tweet = tweet.replace(emoji, " " + emoji_dict[emoji] + " ")

        words = [word.lower().strip() for word in tweet.split()]

        # #, @, http link, punctuation removal

        for word in words:
            regex_cond = (
                re.match(r"@.+", word),
                re.match(r"#.*", word),
                re.match(r"http.?:.*", word),
            )

            if any(regex_cond):
                words.remove(word)

        cleaned_words = Negation(words)

        tweet = " ".join(cleaned_words)

        words = []

        for word, tag in pos_tag(word_tokenize(tweet)):
            w_tags = tag[0].lower()
            w_tags = w_tags if w_tags in ["a", "r", "n", "v"] else None
            if not w_tags:
                lemma = word
            else:
                lemma = wnl.lemmatize(word, w_tags)
            words.append(lemma)
        punctuation = string.punctuation
        for word in words:
            if re.match(f"[{punctuation}]?[0-9]+", word):
                words.remove(word)

        cleaned_words = []
        for word in words:
            for char in word:
                if unicodedata.category(char).startswith("P") or char in punctuation:
                    word = word.replace(char, "")

            cleaned_words.append(word)

        tweet = " ".join(cleaned_words)

        # Stop words removal without punctuation

        cleaned_words = [
            word.lower().strip()
            for word in tweet.split()
            if word.lower() not in ["t", "s", "re", "nt", "d", "ve"]
        ]

        tweet = " ".join(cleaned_words)

        # Digits and words with digits removal
        tweet = re.sub(r"\w*\D*\d\w*", "", tweet)

        cleaned_tweets.append(tweet.strip())

    return cleaned_tweets


from wordcloud import WordCloud
from collections import Counter


def get_context_stop_words(dataset, sentiment_col, text_col, sentiments, stop_words):
    top25_words = []

    for sentiment in sentiments:
        new_df = dataset[dataset[sentiment_col] == sentiment]
        words = " ".join(new_df[text_col])
        cleaned_word = " ".join([word for word in words.split()])
        wordcloud = WordCloud(
            stopwords=stop_words, background_color="black", width=3000, height=2500
        ).generate(cleaned_word)

        top25_words.extend(list(wordcloud.words_.keys())[0:25])

    count = Counter(top25_words)

    context_stop_words = [word.lower() for word, freq in count.items() if freq >= 3]

    return context_stop_words
