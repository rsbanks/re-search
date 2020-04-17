from sys import argv, stderr
from flask import Flask, request, redirect, make_response, url_for
from flask import render_template
from prof import Professor
from profsDB import profsDB
from CASClient import CASClient

app = Flask(__name__, template_folder='.')

# Generated by os.urandom(16)
app.secret_key = b'8\x04h\x0f\x08U0\xde\x1a\x92V\xe3\xd3\x9b5\xfa'

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
            profs = profsDB_.return_profs_list(profs)
        except Exception as e:
            error_statement = str(e)
    else:
        print(error_statement)
    return profs, error_statement

@app.route('/')
@app.route('/index')
def index():

    html = render_template('templates/index.html')
    response = make_response(html)
    return response

@app.route('/search')
def search():

    # username = CASClient().authenticate()

    html = render_template('templates/profs.html')
    response = make_response(html)
    return response

@app.route('/login')
def login():

    # username = CASClient().authenticate()
    
    html = render_template('templates/login.html')
    response = make_response(html)
    return response

@app.route('/logout', methods=['GET'])
def logout():
    
    # casClient = CASClient()
    # casClient.authenticate()
    # casClient.logout()

    html = render_template('templates/index.html')
    response = make_response(html)
    return response

@app.route('/button')
def button():

    # username = CASClient().authenticate()

    html = render_template('templates/search.html')
    response = make_response(html)
    return response

@app.route('/about')
def about():

    html = render_template('templates/about.html')
    response = make_response(html)
    return response

@app.route('/searchResults', methods=['GET'])
def searchResults():   

    # username = CASClient().authenticate()

    search_criteria, input_arguments = getSearchCriteria()

    profs, error_statement = getProfs(search_criteria, input_arguments)

    html = ''
    if error_statement == '':

        if len(profs) == 0:
            html += '<div class="no-search-results">' + \
                        '<h2>No search results. Please try use different keywords.</h2>' + \
                    '</div>'

        i = 0
        for prof in profs:
            html += '<div class="row">' + \
                        '<div class="prof-image">' + \
                            '<img src="' + prof[11] + '"/>' + \
                        '</div>' + \
                        '<div class="prof-info">' + \
                            '<p class="prof-name">' + prof[1] + ' ' + prof[2] + '</p>' + \
                            '<p class="prof-more-info">' + prof[3] + '</p>' + \
                            '<p class="prof-more-info">' + prof[8] + '</p>' + \
                            '<p class="prof-more-info">' + prof[5] + '</p>' + \
                            '<p class="prof-more-info">' + prof[7] + '</p>' + \
                            '<a href="mailto:' + prof[4] + '"><img class="icon" src="static/email-icon.png"></a>' + \
                            '<a href="' + prof[6] + '"><img class="icon" src="static/website-icon.png"></a>' + \
                            '<button type="button" onclick=' + '"collapse(' + str(i) + ')"><img class="icon" src="static/plus.png"></button>' + \
                        '</div>' + \
                    '</div>'+ \
                    '<div class="panel" id =bio-' + str(i) + '>' + \
                        '<p class = prof-more-info>' + prof[10] + '</p>' + \
                    '</div>'
            i+=1
    else:
        html = render_template('templates/profs.html', error_statement=error_statement)
        print(error_statement, file=stderr)
    response = make_response(html)
    return response

def getSearchCriteria():
    input_arguments = []

    name = request.args.get('nameNetid')
    area = request.args.get('area')

    search_criteria = ''

    # search name/netid
    if name is None:
        name = ''
    name = name.strip()
    name = name.replace('%', r'\%')
    names = name.split()

    if len(names)==1:
        search_criteria += '(first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'netid' + ' ILIKE ' + '%s)' + ' AND '
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[0]+'%')
    elif len(names) > 1:
        search_criteria += '((first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s' + ') AND '
        search_criteria += '(first' + ' ILIKE ' + '%s' + ' OR '
        search_criteria += 'last' + ' ILIKE ' + '%s))' + ' AND '
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[0]+'%')
        input_arguments.append('%'+names[1]+'%')
        input_arguments.append('%'+names[1]+'%')

    # search research area/ bio
    if area is None:
        area = ''
    area = area.strip()
    area = area.replace('%', r'\%')
    areas = area.split(",")

    if len(areas) == 1:
        search_criteria += '(area' + ' ILIKE ' + '%s' + ' OR '
        input_arguments.append('%'+areas[0]+'%')
        search_criteria += 'bio' + ' ILIKE ' + '%s)' + ' AND '
        input_arguments.append('%'+areas[0]+'%')
    else:
        for i in range(len(areas)):
            search_criteria += '(area' + ' ILIKE ' + '%s' + ' OR '
            input_arguments.append('%'+areas[i]+'%')
            search_criteria += 'bio' + ' ILIKE ' + '%s)' + ' AND '
            input_arguments.append('%'+areas[i]+'%')

    if search_criteria != '' and search_criteria != None:
        search_criteria = search_criteria[:-5]
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
