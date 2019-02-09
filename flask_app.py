from flask import Flask, render_template
from oboros import draw

app = Flask(__name__)

@app.route('/graphs')
def graphs():
    graph1_url = draw();

    return render_template('graphs.html',
    graph1=graph1_url)

if __name__ == '__main__':
    app.debug = True
    app.run()