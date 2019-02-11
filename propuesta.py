import numpy as np
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
import nltk
from nltk.corpus import stopwords
import zipfile
import time
import io

logger = logging.getLogger('[' + __file__ + ']') 
def main(data):
  logger.info('Inicio del main')
  clean_data = transform_data(data)
  #clean_data = transform_text(clean_data)
  publications_vs_age = extract_publications(data)
  save_file(clean_data, "out_blog_data.csv")  
  save_file(publications_vs_age, 'out_publications_vs_age.csv')   

def transform_data(data):
  logger.info('Transformacion de los datos')
  output_df = data[data.topic != 'indUnk']
  dates_df = (output_df['date']
                  .str.rsplit(',',expand = True)
                  .rename(columns={0 : 'day', 1 : 'month', 2: 'year' }))
  dates_df = pd.concat([output_df, dates_df], axis=1).drop(columns = 'date')
  return dates_df[~dates_df["year"].isin(["2005","2006"])] 
    
def transform_text(data):
  logger.info('Transformacion del texto')
  stop_words = set(stopwords.words('english'))
  words = (data
            .apply(lambda row: nltk.word_tokenize(row['text']), axis = 1) # tokenizamos nuestra columna
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens))) # eliminamos todas las palabras que no sean alfanuméricas
            .apply(lambda tokens_list: list(map(lambda token: token.lower(), tokens_list))) # convertir tokens a lower_case para compararlas correctamente con stopwords
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list))) # eliminar palabras dentro de stopwords
            .apply(lambda valid_word_list: len(valid_word_list)) # obtenemos cuántas palabras son
          )
  return pd.concat([data, words], axis=1).rename(columns ={0: 'Words'}).drop(columns = 'text')

def extract_publications(data):
  lst_publications =  data.groupby(['age'])['id'].count().sort_values(ascending = False)
  return pd.DataFrame({"Age": lst_publications.index, "Publications": lst_publications.values })

def save_file(data, filename):
  logger.info('Archivo {} guardado correctamente.'.format(filename))
  data.to_csv(filename, index= True)

if __name__ == '__main__':
  start_time = time.time()
  logger.info('Inicio del proceso')
  zip = zipfile.ZipFile("blog-authorship-corpus.zip",)
  data = pd.read_csv(zip.open('blogtext.csv'))
  main(data)
  elapsed_time = time.time() - start_time
  logger.info("Proceso terminado: Duracion {} seconds.".format(elapsed_time))
  