from sys import argv, stderr
from flask import Flask, request, redirect, make_response, url_for
from flask import render_template
from prof import Professor
from profsDB import profsDB

app = Flask(__name__, template_folder='.')

def getProfs(search_criteria, input_arguments):
    profsDB_ = profsDB()
    error_statement = profsDB_.connect()
    profs = []
    if error_statement == '':
        cursor = profsDB_.conn.cursor()
        try:
            if len(input_arguments) != 0:
                profs = profsDB_.displayProfessorsByFilter(cursor, search_criteria, input_arguments)
            else:
                profs = profsDB_.displayAllProfessors(cursor)
            profsDB_.disconnect()
            profs = profsDB_.return_profs_list(profs)
        except Exception as e:
            error_statement = str(e)
    else:
        print(error_statement)
    return profs, error_statement

@app.route('/')
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/search')
def search():
    html = render_template('search.html')
    response = make_response(html)
    return response

@app.route('/login')
def login():
    html = render_template('login.html')
    response = make_response(html)
    return response

@app.route('/button')
def button():
    html = render_template('search.html')
    response = make_response(html)
    return response

@app.route('/about')
def about():
    html = render_template('about.html')
    response = make_response(html)
    return response

@app.route('/profs')
def profs():   
    search_criteria, input_arguments = getSearchCriteria()

    profs, error_statement = getProfs(search_criteria, input_arguments)

    if error_statement == '':
        html = \
            render_template('profs.html', profs=profs)
    else:
        html = render_template('profs.html', error_statement=error_statement)
        print(error_statement, file=stderr)
    response = make_response(html)
    return response

def getSearchCriteria():
    input_arguments = []

    name = request.args.get('name')
    area = request.args.get('area')
    netid = request.args.get('netid')

    search_criteria = ''
    if name != '' and name != None:
        search_criteria += '' + 'first' + ' LIKE ' + '?' + ' OR '
        search_criteria += '' + 'last' + ' LIKE ' + '?' + ' AND '
        input_arguments.append('%'+name+'%')
        input_arguments.append('%'+name+'%')
    if area != '' and area != None:
        search_criteria += 'area' + ' LIKE ' + '?' + ' AND '
        input_arguments.append('%'+area+'%')
    if netid != '' and netid != None:
        search_criteria += 'netid' + ' LIKE ' + '?' + ' AND '
        input_arguments.append('%'+netid+'%')

    if search_criteria != '' and search_criteria != None:
        search_criteria = search_criteria[:-5]
    print(search_criteria)
    return search_criteria, input_arguments

if __name__ == '__main__':
    
    if (len(argv) != 2):
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[1])
    except:
        print("Port must be an integer", file=stderr)
        exit(1) 

    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
