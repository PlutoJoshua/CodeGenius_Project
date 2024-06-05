def preprocess_and_train(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='extracted_data', task_ids='fetch_data')
    
    def preprocess_text(text):
        tokens = okt.nouns(text)
        return ' '.join(tokens)
    
    df['processed'] = df['user_input'].apply(preprocess_text)

    # TF-IDF 및 LDA 학습
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['processed'])
    
    lda = LatentDirichletAllocation(n_components = 4, random_state = 777)
    lda.fit(tfidf_matrix)
    
    df['lda_topic'] = lda.transform(tfidf_matrix).argmax(axis=1)
    kwargs['ti'].xcom_push(key='processed_data', value=df)