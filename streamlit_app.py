from wordcloud import WordCloud
import streamlit as st
import matplotlib.pyplot as plt
import docx2txt
from collections import Counter
from nltk.stem import PorterStemmer
import pandas as pd




class WordAnalytics:
    stop_words=['en','des','qui','dans','je','mon','ma','mes','tes','ses','et','du','de','à','','tu','le','la','les','mes','ce','ces','un','est', 'me','te','une','que']
    raw_text =''
    doc_processed=''
    n=0
    data=[]
    
    def file_selector(self):
        file = st.sidebar.file_uploader("Upload Files",type=['docx'])
        if file !=None:
            self.raw_text=docx2txt.process(file)


    def nombre_mot_affiche(self):
        num_unique = self.count_words_fast()
        if 0<= num_unique and num_unique <=30:
            self.n=num_unique
        if 30< num_unique and num_unique <100:
             self.n= 20
        if num_unique>= 100:
             self.n= 25

    def count_words_fast(self):    
        text = self.doc_processed.lower()
        skips = [".", ", ", ":", ";", "'", '"']
        
        for ch in skips:
            text = text.replace(ch, "")
        word_counts = Counter(text.split(" "))
        self.data=word_counts
        return len(word_counts)

    def most_common_n(self):
        self.data= self.data.most_common(self.n)

    

    def preprocess(self):
        words = self.raw_text.lower().split()
        cleaned_words = []
        lemmatizer = PorterStemmer() #plug in here any other stemmer or lemmatiser you want to try out

        # remove stopwords
        for word in words:
            if word not in self.stop_words:
                cleaned_words.append(word)
        
        # stemm or lemmatise words
        stemmed_words = []
        for word in cleaned_words:
            word = lemmatizer.stem(word)   #dont forget to change stem to lemmatize if you are using a lemmatizer
            stemmed_words.append(word)
        
        # converting list back to string
        self.doc_processed=" ".join(stemmed_words)



    def word_cloud(self):
        #plot
        if self.raw_text !='':
            wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(self.raw_text)
            #wc.generate_from_frequencies(text)
            fig = plt.figure(figsize = (10, 10))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(fig)

    def visual(self):
        #plot 
        if self.n!=1:
            x_val = [x[0] for x in self.data]
            y_val = [x[1] for x in self.data]
            dictionary={'index':x_val,'word count':  y_val}
            data = pd.DataFrame(dictionary).set_index('index')
            st.bar_chart(data)
