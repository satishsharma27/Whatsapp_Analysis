
from urlextract import URLExtract
extract = URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud




def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())


    #fetch number of media messages

    num_media_message = df[df['message'] == '<Media omitted>'].shape[0]

    #fetch number of links
    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_message,len(links)


def most_busy_users(df):

    x = df['user'].value_counts().head()[1:]

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'count': "percent"})

    return x,df


def create_word_colud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


