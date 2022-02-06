#!/usr/bin/env python


from flask import Flask, render_template, request, jsonify
import constraint as cs


app = Flask(__name__)
broj_ogranicenja = ""
broj_varijabli = ""
min_max = ""


@app.route('/')
def index():
    return render_template('stranica.html')


@app.route('/variables', methods=["POST"])


def variables():
    global broj_ogranicenja
    broj_ogranicenja = request.form["broj_ogranicenja"]
    global broj_varijabli
    broj_varijabli = request.form["broj_varijabli"]
    global min_max
    min_max = request.form["min_max"]
    print(request.form)
    return render_template('stranica.html')
    

@app.route("/program", methods=["POST"])

def program():

   
    if request.method == 'POST':
        polje = ""
        polje = request.form.to_dict() 
        print(polje) 
        li = list(polje.items())[int(broj_varijabli):] 
        li_cilja = list(polje.items())[:int(broj_varijabli)] 
        chunked_list = [] 
        for i in range(0, len(li), int(broj_varijabli)+2):
            chunked_list.append(li[i:i+int(broj_varijabli)+2])
        data = (provjera_ogranicenja(chunked_list, li_cilja))
        print(data["varijable"])
    return render_template('rjesenje.html', data=data)



izrazi = []
izrazi_cilj = []
def provjera_ogranicenja(lista, li_cilja):
    
    izrazi.clear()
    izrazi_cilj.clear()
    problem = cs.Problem() 
    for i in range (int(broj_varijabli)):
        problem.addVariable('X'+ str(i+1),  range(i+1,)) 
    
    for i in lista:
        list_arg = i[:int(broj_varijabli)] 
        list_end = i[-2:]
        operator = ""
        num = ""
        for i in list_end[0]:
            operator = i
        for i in list_end[1]:
            num = i

        izraz = ""
        izraz_cilj = ""

        for i in li_cilja:
            if i != li_cilja[-1]:
                izraz_cilj = izraz_cilj + i[1] + '*' + i[0] + " " + "+" + " "
            else:
                izraz_cilj = izraz_cilj + i[1] + '*' + i[0]
        
        izrazi_cilj.append(izraz_cilj) 
        
        for i in list_arg:
            if i != list_arg[-1]:
                izraz = izraz + i[1] + '*' + i[0][:-2] + " " + "+" + " "
            else:
                izraz = izraz + i[1] + '*' + i[0][:-2] + " " + operator + " " + num
                izrazi.append(izraz)
                problem.addConstraint(boolean_provjera, [i[0][:-2] for i in list_arg])
    
    rjesenja = problem.getSolutions()        
    print(f"Constraints: {problem._constraints}")
    for i in izrazi:
        print(i)
        
    print(f"Rjesenje: {rjesenja}")

    print(f"Tip rjesenja: {type(rjesenja)}")
    print(f"Velicina rjesenja: {len(rjesenja)}")
    for r in rjesenja:
        print(f"Ovo je r: {r}")

    optimalan_broj = 0
    if (min_max == 'max'):
        optimalan_broj = max([evaluacija( r, li_cilja ) for r in rjesenja ])
    if (min_max == 'min'):
        optimalan_broj = min([evaluacija( r, li_cilja ) for r in rjesenja ])
    optimalno_rjesenje = [ r for r in rjesenja if evaluacija( r, li_cilja ) == optimalan_broj ][ 0 ]
    data = {"funkcija_cilja": izrazi_cilj[0], "izrazi": izrazi, "rjesenje":str(optimalan_broj), "varijable":  str(optimalno_rjesenje)}
    return data             
     
def evaluacija( rjesenje, li_cilja ):
    rj = 0
    for i in li_cilja:
        rj = rj + rjesenje[ str(i[0]) ] * int(i[1])
    return rj

newlist = []
def provjera(izraz,*args):
    newlist.clear()
    for i in izraz:
        if 'X1' in i:
            i=i.replace('X1',str(args[0]))
        if 'X2' in i:
            i=i.replace('X2',str(args[1]))
        if 'X3' in i:
            i=i.replace('X3',str(args[2]))
        if 'X4' in i:
            i=i.replace('X4',str(args[3]))
        if 'X5' in i:
            i=i.replace('X5',str(args[4]))
        if 'X6' in i:
            i=i.replace('X6',str(args[5]))
        if 'X7' in i:
            i=i.replace('X7',str(args[6]))
        if 'X8' in i:
            i=i.replace('X8',str(args[7]))
        if 'X9' in i:
            i=i.replace('X9',str(args[8]))
        if 'X10' in i:
            i=i.replace('X10',str(args[9]))
        print(i)
        newlist.append(i)

    return newlist

def boolean_provjera(*args):
    list = provjera(izrazi,*args)
    r = True
    for i in list:
        r = r and eval(i)
    return r
    







