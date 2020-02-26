from flask import Flask,abort,jsonify,render_template,url_for,request,send_from_directory,redirect
import numpy as np 
import pandas as pd 
import json 
import requests
import pickle


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommendation', methods=['POST','GET'])
def recommendation():
    if request.method == 'POST':
        body  = request.form
        anime = body['name'] #.capitalize()
        if anime not in list(dfAnime['title']):
            return redirect('/notfound')
        index = dfAnime[dfAnime['title'] == anime].index.values[0]

        anim_reco = sorted(list(enumerate(cos_score1[index])), key=lambda x:x[1], reverse=True) 
        anim_find = dfAnime.iloc[index][col1]
        
        anim_list = []
        anim_box  = []
        for i in anim_reco:
            anime_dic = {}
            if i[0] == index:
                continue
            else:
                anime_dic['title']  = dfAnime.iloc[i[0]]['title']
                anime_dic['genre']  = dfAnime.iloc[i[0]]['genre']
                anime_dic['age']    = dfAnime.iloc[i[0]]['rating']
                anime_dic['image']  = dfAnime.iloc[i[0]]['img_url']
                anime_dic['airing'] = dfAnime.iloc[i[0]]['premiered']
                anime_dic['score']  = dfAnime.iloc[i[0]]['score']
                anime_dic['id']     = dfAnime.iloc[i[0]]['anime_id']
                anime_dic['syno']   = dfAnime.iloc[i[0]]['synopsis']
                anime_dic['jpn']    = dfAnime.iloc[i[0]]['title_japanese']
                anime_dic['studio'] = dfAnime.iloc[i[0]]['studio']
                anime_dic['link']   = dfAnime.iloc[i[0]]['link']
            anim_box.append(anime_dic)
            if len(anim_list) < 6:
                anim_list.append(anime_dic)
            if len(anim_box) == 30:
                break
        # anim_m = sorted(anim_box, key = lambda k: k['score'])
        # anim_m = anim_box[anim_box['studio']]
    return render_template('result.html', rekomen = anim_list, favoritku = anim_find, movie = anim_box)

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == "__main__":
    dfAnime = pd.read_csv('DataAnime.csv')
    col1 = ['title', 'genre', 'rating', 'img_url', 'premiered', 'ranked', 'score', 'synopsis', 'title_japanese', 'studio', 'link']
    with open("modelPickle1", "rb") as modPick1:
        cos_score1 = pickle.load(modPick1)
    app.run(debug=True)