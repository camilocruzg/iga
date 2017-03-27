from flask import Flask, render_template, request, url_for
from Functions import evolve

app = Flask(__name__)

@app.route('/')
def form():
    return "hello,world"

@app.route('/hello', methods=['POST'])
def hello():
    name=request.form['yourname']
    return name

@app.route('/test',methods=['POST'])
def test():
    pop_size=request.form['popsize']
    ind_size=request.form['indsize']

    return evolve(pop_size, ind_size)


# Run the app :)
if __name__ == '__main__':
  app.run(
        host="",
        port=1337
  )