
##################################################### HTML 별 접속 그래프 (access_count) #####################################################
def plot_html_access(df, batch_date):
    """
    html 별 접속기록 lineplot
    df: access_count
    batch_date: five_days_ago
    """
    _df = df[df['date'] >= batch_date]
    _else = _df[_df['html'] != "Homepage"]
    _home = _df[_df['html'] == "Homepage"]
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    sns.lineplot(data=_home, x='date', y='count', hue='html', marker='o', palette='Set1', ax=axes[0])
    axes[0].set_title('Home access from the last 5 days')
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Count')
    axes[0].legend(title='HTML')
    axes[0].set_ylim(bottom=0)

    sns.lineplot(data=_else, x='date', y='count', hue='html', marker='o', ax=axes[1])
    axes[1].set_title('HTML access from the last 5 days')
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('Count')
    axes[1].legend(title='HTML')
    axes[1].set_ylim(bottom=0)

    plt.tight_layout()
    st.pyplot(fig)


def plot_chat_history_access(df, batch_date):
    """
    히스토리, 채팅 페이지 접속 비율
    df: access_count
    batch_date: now() - 1day
    """
    chat_his = df[df["date"] == batch_date]
    chat_his = chat_his[(chat_his['html'] == 'chatting') | (chat_his['html'] == 'History')]

    fig = px.pie(data_frame=chat_his, names='html', values='count', hole=0.33)
    fig.update_layout(title=f"{batch_date} / History access", width=600, height=400)

    st.plotly_chart(fig)

################################################# 시간별 이용량 변화 그래프(time_distribution) #################################################

def plot_hourly_behavioral_data(df, batch_date):
    """
    전 일 기준 시간대 별 이용량
    df: time_distribution
    batch_date: now() - 1day
    """
    _df = df[df["date"] == batch_date]
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=_df, x='time', y='data', marker='o', color='b')
    plt.title('Hourly behavioral data Line Plot')
    plt.xlabel('Time')
    plt.ylabel('Data')
    st.pyplot()

################################################### LDA Topic Visualization(lda_userInput) ###################################################

def generate_wordcloud(df, batch_date):
    """
    wordcloud
    df: lda_userInput
    batch_date: now() - 1day
    """
    _df = df[df["date"] = batch_date]
    combined_topics = ' '.join(_df['lda_topic'])
    wordcloud = WordCloud(background_color='white', width=800, height=400).generate(combined_topics)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

def plot_non_service_user_keywords(df, batch_date):
    """
    pie plot
    df: lda_userInput
    batch_date: now() - 1day
    """
    _df = df[df["date"] == batch_date]
    count_df = _df["lda_topic"].value_counts().reset_index().sort_values(by='count', ascending=False).head(5)
    
    fig = px.pie(names=count_df["index"], values=count_df["lda_topic"], hole=0.33)
    fig.update_layout(title=f"{batch_date} / Non-service user input keywords ratio", width=600, height=400)

    st.plotly_chart(fig)

def plot_non_service_user_keywords_count(df, batch_date):
    _df = df[df["date"] == batch_date]
    count_df = _df["lda_topic"].value_counts().reset_index().sort_values(by='count', ascending=False).head(5)
    
    plt.figure(figsize=(10, 6))
    plt.barh(count_df["index"], count_df["lda_topic"])
    plt.xlabel('Count')
    plt.ylabel('Keyword')
    plt.title('Non-service user input keywords count')
    plt.gca().invert_yaxis()
    st.pyplot()