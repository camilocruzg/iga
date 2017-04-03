"""
Usage:
    curl -X POST localhost:1337/test -d "popsize=100&indsize=(2,3,4)&gens=5&problem=max"
"""

from flask import Flask, render_template, request, url_for
from Functions import evolve

app = Flask(__name__)

@app.route('/')
def form():
    return "hello,world"

@app.route('/hello', methods=['POST'])
def hello():
    name=request.form['yourname']
    return "Welcome, ", name

@app.route('/test',methods=['POST'])
def test():
    pop_size=request.form['popsize']
    ind_size=request.form['indsize']
    gens=request.form['gens']
    prob=request.form['problem']
    # return "the number is %s and %s"%(pop_size,ind_size)
    poplist = evolve(pop_size,ind_size,gens,prob)
    return str(poplist)


if __name__ == '__main__':
  app.run(
        host="",
        port=1337
  )

