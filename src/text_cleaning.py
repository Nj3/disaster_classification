"""Module for Text cleaning
"""

import string
import re
import html
from bs4 import BeautifulSoup
import emoji


def remove_URL(text: str, url_pattern: str) -> str:
    cleaned_text = re.sub(pattern=url_pattern, flags=re.IGNORECASE, repl=" ", string=str(text))
    return cleaned_text


def remove_repeating_char(text: str) -> str:
    # Sometimes we can have two repeating chars like look.
    # thus we replace more than two occurrence with two.
    # It may cause problem like word itself will not make sense.
    # But if we try to correct spelling, it may change the word accordingly.
    cleaned_text = re.sub(
        pattern=r"([\S])\1{3,}", flags=re.IGNORECASE, repl=r"\1\1", string=str(text)
    )
    return cleaned_text


def remove_twitter_handles(text: str, replace_with_token: bool) -> str:
    # if replace_with_token is True, replace all twitter handles with word "user"
    if replace_with_token:
        cleaned_text = re.sub(pattern=r"@[\w]+", repl="user", string=str(text), flags=re.IGNORECASE)
    else:
        cleaned_text = re.sub(pattern=r"@[\w]+", repl="", string=str(text), flags=re.IGNORECASE)

    return cleaned_text


def remove_hashtags(text: str) -> str:
    cleaned_text = " ".join([s[1:] if s.startswith("#") else s for s in text.split()])
    return cleaned_text


def decode_html(text: str) -> str:
    text = html.unescape(text)
    cleaned_text = BeautifulSoup(text, features="html.parser").get_text()

    return cleaned_text


def expand_contractions(text: str) -> str:
    # https://stackoverflow.com/a/19794953/6582814
    custom_contractions = {
        "ain't": "is not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "tthey would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have",
    }
    contractions_regex_pattern = re.compile("{}".format("|".join(custom_contractions.keys())))

    # https://stackoverflow.com/a/19790352/6582814
    def replace(match):
        return custom_contractions[match.group(0)]

    return contractions_regex_pattern.sub(replace, text)


def remove_punctuations(text: str) -> str:
    cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
    return cleaned_text


def decode_emojis(text: str) -> str:
    basic_emoticons = {
        ":-)": "happy",
        ":)": "happy",
        ":D": "happy",
        ":O": "surprised",
        ":-(": "sad",
        ":(": "sad",
    }
    for emoticon, translation in basic_emoticons.items():
        text = text.replace(emoticon, translation)

    text = emoji.demojize(text)
    cleaned_text = text.replace(":", "")
    return cleaned_text


# TODO: Function for unicode char handling. there was char like \x89 which means hexcode mark u+81 in utf-8 format. https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations
