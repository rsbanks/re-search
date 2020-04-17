from sys import argv, stderr
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from prof import Professor
from profsDB import profsDB
import csv

app = Flask(__name__, template_folder='.')

def getProfs(search_criteria, input_arguments):
    profsDB_ = profsDB()
    error_statement = profsDB_.connect()
    profs = []
    if error_statement == '':
        connection = profsDB_.conn
        try:
            if len(input_arguments) != 0:
                profs = profsDB_.displayProfessorsByFilter(connection, search_criteria, input_arguments)
            else:
                profs = profsDB_.displayAllProfessors(connection)
            #sqlite only
            # profsDB_.disconnect()
            profs = profsDB_.return_profs_list(profs)
        except Exception as e:
            error_statement = str(e)
    else:
        print(error_statement)
    return profs, error_statement

def getSearchCriteria(netid):
    input_arguments = []
    name = ''
    area = ''

    search_criteria = ''

    name = name.strip()
    name = name.replace('%', r'\%')
    names = name.split()

    if len(names)==1:
        search_criteria += 'first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s' + ' AND '
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[0]+'%')
    elif len(names) > 1:
        search_criteria += '(first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s' + ') AND '
        search_criteria += '(first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s' + ') AND '
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[1]+'%')
        input_arguments.append('%'+names[1]+'%')

    area = area.strip()
    area = area.replace('%', r'\%')

    search_criteria += 'area' + ' ILIKE ' + '%s' + ' AND '
    input_arguments.append('%'+area+'%')

    if netid is None:
        netid = ''
    netid = netid.strip()
    netid = netid.replace('%', r'\%')

    search_criteria += 'netid' + ' ILIKE ' + '%s' + ' AND '
    input_arguments.append('%'+netid+'%')

    if search_criteria != '' and search_criteria != None:
        search_criteria = search_criteria[:-5]
    return search_criteria, input_arguments

def getUpdateString(netid):
    update_string = "UPDATE profs SET firstname = '" + request.args.get('firstname') 
    update_string += "', lastname = '" + request.args.get('lastname')
    update_string += "', phone = '" + request.args.get('phone')
    update_string += "', email = '" + request.args.get('email')
    update_string += "', title = '" + request.args.get('title')
    update_string += "', website = '" + request.args.get('website')
    update_string += "', rooms = '" + request.args.get('rooms')
    update_string += "', department = '" + request.args.get('department')
    update_string += "', area = '" + request.args.get('area')
    update_string += "', bio = '" + request.args.get('bio')
    update_string += "' WHERE netid = '" + netid + "'"
    return update_string


def overwriteProf(update_string):
    profsDB_ = profsDB()
    error_statement = profsDB_.connect()
    if error_statement == '':
        connection = profsDB_.conn
        try:
            result = connection.execute(update_string)
        except Exception as e:
            error_statement = str(e)
    else:
        print(error_statement)
    return error_statement

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    html = render_template('index_tara.html')
    response = make_response(html)
    return response

@app.route('/profinfo', methods=["GET"])
def profinfo():
    netID = request.args.get('netid')
    search_criteria, input_arguments = getSearchCriteria(netID)
    profs, error_statement = getProfs(search_criteria, input_arguments)

    if error_statement == '':
        html = \
            render_template('profinfo_tara.html', profs=profs, netid=netID)
    else:
        html = render_template('profinfo_tara.html', error_statement=error_statement)
        print(error_statement, file=stderr)
    response = make_response(html)
    response.set_cookie('netid', netID)
    return response

@app.route('/displayprof', methods=["GET"])
def displayprof():
    netID = request.cookies.get('netid')
    update_string = getUpdateString(netID)
    print(update_string)
    error_statement = overwriteProf(update_string)
    search_criteria, input_arguments = getSearchCriteria(netID)
    profs, error_statement = getProfs(search_criteria, input_arguments)

    if error_statement == '':
        html = \
            render_template('displayprof_tara.html', profs=profs, netid=netID)
    else:
        html = render_template('displayprof_tara.html', error_statement=error_statement)
        print(error_statement, file=stderr)

    response = make_response(html)
    return response

if __name__ == '__main__':
    if (len(argv) != 2):
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)
    try:
        port = int(argv[1])
    except:
        print("Port must be an integer", file=stderr)
        exit(1) 
    app.run(host='0.0.0.0', port=port, debug=True)
