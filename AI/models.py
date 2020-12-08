import pandas as pd
from textslack.textslack import TextSlack
from gensim.models import doc2vec
import os

os.chdir(r'C:\Users\sriva\Desktop\edu.usf.sas.pal.muser\SpotifyDataExtractor')

class NLPModel:
    def __init__(self, sp, conn, max_epochs=100, vec_size=50, alpha=0.025):
        self.sp = sp
        self.conn = conn
        self.slack = TextSlack(variety='BrE', lang='english')
        self.max_epochs = max_epochs
        self.vec_size = vec_size
        self.alpha = alpha
        self.df = pd.read_sql_table('SPOTIFY_DATA', con=self.conn)

    def _create_tagged_document(self, list_of_list_of_words):
        for i, list_of_words in enumerate(list_of_list_of_words):
            yield doc2vec.TaggedDocument(list_of_words, [i])

    def _training_data(self):
        key_features = (self.df['album'] + ' ' + self.df['name'] + ' ' + self.df['artist']).tolist()
        cleaned_key_features = self.slack.transform(key_features)
        list_list_words = [sent.split() for sent in cleaned_key_features]
        return list_list_words

    def build_model(self):
        list_list_words = self._training_data()
        train_data = list(self._create_tagged_document(list_list_words))
        model = doc2vec.Doc2Vec(size=self.vec_size,
                                alpha=self.alpha,
                                min_alpha=0.00025,
                                min_count=1,
                                dm=1)
        model.build_vocab(train_data)
        for epoch in range(self.max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(train_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha
        model.save('d2v.model')
        print("Model Saved")

    def most_similar_doc(self, target):
        model = doc2vec.Doc2Vec.load('d2v.model')
        model.random.seed(95)
        cleaned_target = self.slack.transform(target).split()
        pred_vector = model.infer_vector(cleaned_target)
        sim_vector = model.docvecs.most_similar([pred_vector])
        pred_index = sim_vector[0][0]
        return self.df.loc[pred_index, self.df.columns[6:-1]]