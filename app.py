from flask import Flask,render_template
from flask import request
import pandas
import numpy as np
import os
import pickle

PEOPLE_FOLDER = os.path.join('static', 'image')
popular_rating = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
song_df_2 = pickle.load(open('song_df_2.pkl','rb'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'music.jpg')
    return render_template('index.html',
                           song = list(popular_rating['title'].values),
                           artist_name = list(popular_rating['artist_name'].values),
                           rank = list(popular_rating['Rank'].values),user_image = full_filename
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_songs',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = song_df_2[song_df_2['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['artist_name'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)