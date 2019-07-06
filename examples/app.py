# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from examples.sparql import queryPublications,queryInfo,recommend
app = Flask(__name__)
app.secret_key = 'dev'

bootstrap = Bootstrap(app)

pub_types = {"电影": "Film", "图书": "Book", "游戏": "Game", "数据可视化": "data-analysis"}


@app.route('/', methods=['GET', 'POST'])
def index():
    form = request.values
    if len(form) > 0:
        return actionSearch(form)
    else:
        return render_template('index.html')

def actionSearch(form):
    keyword=form['keyword']
    data={}
    nums={}
    for type in pub_types.values():
        if type != 'data-analysis':
            rs =queryPublications(keyword, type)
            rows = reformatData(rs)
            if len(rows) > 0:
                is_plot=1
            data[type] = rows
            nums[type] = len(rows)
    return render_template("result.html", form=form, data=data, pub_type_dict=pub_types, is_plot=is_plot, nums=nums)
def reformatData(rs):
    result = []
    for line in rs:
        keys = line.keys()
        temp = {}
        temp['pub'] = line['pub']['value'] if 'pub' in keys else ""
        temp['url'] = line['uri']['value'] if 'uri' in keys else ""
        temp['name'] = line['name']['value'] if 'name' in keys else ""
        temp['abstract'] = line['abstract']['value'] if 'abstract' in keys else ""
        temp['pid'] = line['pid']['value'] if 'pid' in keys else ""
        result.append(temp)
    return result

@app.route('/getinfo/<pid>/<type>', methods=['GET'])
def getInfo(pid, type):
    info  = reformatData(queryInfo(pid, type))[0]
    name = info['name']
    recommends=[]
    lines = recommend(name,type)
    for row in lines:
        item={}
        tmp_url = row['callret-1']['value']
        item['url'] = tmp_url
        item['name'] = tmp_url.split('/')[-1].replace('_', ' ')
        recommends.append(item)
    return render_template('info.html',info=info,recommends=recommends)
@app.route('/data_analyses/<film>/<book>/<game>', methods=['GET'])
def data_analyses(film,book,game):
    nums={}
    nums['Film']  = film
    nums['Book'] = book
    nums['Game'] = game
    is_plot = 1
    return render_template("data_analysis.html", nums=nums,is_plot =is_plot)

app.run('127.0.0.1', port=5100, debug=True)
# if __name__ == '__main__':
#     app.run('127.0.0.1:5000',debug=True)