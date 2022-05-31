import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def load_data(path, info=True):
    if len(path.split(".csv")) >1:
        read=pd.read_csv(path)
    elif len(path.split(".xlsx")) >1: 
        read=pd.read_csv(path)
    
    if info:
        if len(read) > 0:
            print(">>> Data imported sucessfully !!") 
            print(">>> Dimentions: ")
            print("------ rows:- ",read.shape[0], "columns:- ",read.shape[1]) 
            print(">>> Missing Value:")
            print(np.where(read.isnull().values.any()==False, "------ No Missing value found !", "------ Dataset contains Missing value !"))
            print(np.where(read.isnull().values.any()==True, f"------ missing values: \n{read.isnull().sum()}"," "))
            
        else:
            print(">>> Data didnot import :( ") 
        return read 

data=load_data('data/netflix_titles.csv') 
netflix_shows = data[data['type']=="TV Show"] 
netflix_movie = data[data['type']=="Movie"] 


class analyze:
   """ This contains analyze of data with different features of Netflix movies and Tv Shows 
   1. analyze_months_and_shows(self,data):- analyzed movie release date yearly and month wise. data=dataset  
   2. rating(df):- Visulized the type of rating and the amount of rating of the data. 
   3. release_year_yearly(df):- amount of movies and shows release yearwise. 
   4. country_analysis(df, graph=True):- Analyzed the countrywise release of movies and shows. 
   5. duration_analysis_movies(df):- Analyzed the duration of movies in Netflix. 
   6. duration_analysis_shows(df):- Analyzed the duration of TV Shows in Netflix. 
   7. generes_analysis(df):- WordCloud for Genres¶
   """
  
   def __init__(self):
      pass
   
   def show_graph(self, df):
      plt.figure(figsize=(8,7), dpi=200)
      plt.pcolor(df, cmap='afmhot_r')
      plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns,fontsize=7)
      plt.yticks(np.arange(0.5, len(df.index), 1), df.index,fontsize=7)
      plt.title("Netflix content update ", fontsize=12)

      cbar=plt.colorbar()
      cbar.ax.tick_params(labelsize=8) 
      cbar.ax.minorticks_on()
      plt.show()

   def analyze_months_and_shows(self,data):
      netflix_date = data[['date_added']].dropna() 
      netflix_date['year'] = netflix_date['date_added'].apply(lambda x : x.split()[-1])
      netflix_date['month'] = netflix_date['date_added'].apply(lambda x: x.split()[0]) 
      month_order=['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December'][::-1]
      df = netflix_date.groupby('year')['month'].value_counts().unstack().fillna(0)[month_order].T
      self.show_graph(df)

   def rating(df):
      plt.figure(figsize=(12,10))
      ax=sns.countplot(x='rating', data=df, order=df['rating'].value_counts().index[0:len(df['rating'].unique())])
      return ax 

   def release_year_yearly(df):
      plt.figure(figsize=(12,10))
      ax=sns.countplot(y='release_year', data=df, order=df['release_year'].value_counts().index[0:18]) 
   
   def country_analysis(df, graph=True):
      countries={}
      country = list(df['country'].fillna('Unknown'))
      for i in country:
         i=list(i.split(','))
         if len(i)==1:
               if i in list(countries.keys()):
                  print(i)
                  countries[i]+=1
               else:
                  countries[i[0]]=1
         else:
               for j in i:
                  if j in list(countries.keys()):
                     countries[j]+=1
                  else:
                     countries[j]=1
      final_countries={}

      for country, no in countries.items():
         country=country.replace(' ', '')
         if country in list(final_countries.keys()):
               final_countries[country]+=no
         else:
               final_countries[country]=no

      final_countries={k:v for k, v in sorted(final_countries.items(), key=lambda item : item[1] , reverse=True)}
      if graph==True:
         plt.figure(figsize=(12,10))
         ax=sns.barplot(x=list(final_countries.keys())[0:10], y=list(final_countries.values())[0:10])
      
      return final_countries
   
   def duration_analysis_movies(df):
      a=df['duration'].str.replace(' min','')
      a=a.fillna(0)
      a=a.astype(str).astype(int)
      sns.kdeplot(data=a, shade=True)
      return a

   def duration_analysis_shows(df):
      a=df['duration'].apply(lambda x: x.split(' ')[0])
      a=a.fillna(0)
      a=a.astype(str).astype(int)
      sns.kdeplot(data=a,shade=True)
      return a 

   def generes_analysis(df):
      generes = list(df['listed_in'])
      gen=[]
      for i in generes:
         i = list(i.split(','))
         for j in i:
               gen.append(j.replace(' ',''))

      g=Counter(gen)
      text = list(set(gen))
      plt.rcParams['figure.figsize'] = (13, 13)

      wordcloud = WordCloud(max_words=1000000,background_color="white").generate(str(text))

      plt.imshow(wordcloud,interpolation="bilinear")
      plt.axis("off")
      plt.show()
      return g
   
 

