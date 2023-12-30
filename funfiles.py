from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

f = open("stop_hinglish.txt")
stopwords = f.read()


def removestopwords(tem):
    words = []
    for message in tem['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    return tem


extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    num_words = []
    for message in df['message']:
        num_words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(num_words), num_media_messages, len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'User', 'count': 'Percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'notification']
    temp = removestopwords(temp)
    temp = temp[temp['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    commondf = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'frequency'])
    return commondf


def emoji_count(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=["emoji", 'number'])

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='Period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
