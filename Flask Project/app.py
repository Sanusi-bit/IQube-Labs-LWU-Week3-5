from flask import Flask, render_template, redirect,request,url_for
import logging
import numpy as np
import sys
from Model import wordcloud_gen

app = Flask(__name__)

#app.Logger.addHandler(logging.StreamHandler(sys.stdout))
#app.logger.setLevel(logging.ERROR)

@app.route('/',METHODS=['POST','GET'])
def index():
    if request.method == 'POST':
        search_query = request.form['Search Query']
    
        image = wordcloud_gen(search_query)


        return render_template('index.html',image=image)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    