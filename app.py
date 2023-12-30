import matplotlib.pyplot as plt
import streamlit as st

import peprocessor
import funfiles
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Enter your Whatsapp chat in Strict 24 hour time")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = peprocessor.preprocess(data)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove("notification")
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("show analysis with respect to", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, num_media, num_links = funfiles.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Total Attachments")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        if selected_user == 'overall':
            st.title("most busy users")
            x, new_df = funfiles.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='Green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.title("Wordcloud")
        df_wc = funfiles.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.title("common word")
        most_common_df = funfiles.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df['word'], most_common_df['frequency'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Emoji analysis")
        emoji_df = funfiles.emoji_count(selected_user, df).head()
        col1, col2 = st.columns(2)
        fig, ax = plt.subplots(figsize=(8, 8))
        with col1:
            st.dataframe(emoji_df)

        with col2:
            ax.pie(emoji_df['number'], labels=emoji_df.index, autopct="%0.1f")
            st.pyplot(fig)
        st.title("Monthly Timeline")
        timeline = funfiles.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = funfiles.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = funfiles.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = funfiles.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = funfiles.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
