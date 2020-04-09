from os import path
from sys import argv, stderr
from sqlite3 import connect
from prof import Professor

class profsDB:

    def __init__(self):
        self.conn = None

    def connect(self):
        DATABASE_NAME = 'profs.sqlite'
        error_statement = ''

        if not path.isfile(DATABASE_NAME):
            error_statement = 'database profs.sqlite not found'
            print(error_statement, file=stderr)
        else:
            self.conn = connect(DATABASE_NAME)

        return error_statement

    def disconnect(self):
        self.conn.close()

    def displayAllProfessors(self, cursor):
        stmtStr = 'SELECT profs.netid, profs.title, profs.first, profs.last, profs.email,' + \
                ' profs.phone, profs.website, profs.rooms, profs.department, profs.area,' + \
                ' profs.bio' + \
                ' FROM profs ' + \
                ' ORDER BY profs.last ASC'
        cursor.execute(stmtStr)
        return self.return_profs(cursor)

    def displayProfessorsByFilter(self, cursor, search_criteria, input_arguments):
        stmtStr = 'SELECT profs.netid, profs.title, profs.first, profs.last, profs.email,' \
                ' profs.phone, profs.website, profs.rooms, profs.department, profs.area,' \
                ' profs.bio' + \
                ' FROM profs' + \
                ' WHERE ' + search_criteria + \
                ' ORDER BY profs.last ASC'
        cursor.execute(stmtStr, input_arguments)
        return self.return_profs(cursor)

    def return_profs(self, cursor): 
        profs = []
        row = cursor.fetchone()
        while row is not None:
            prof = Professor(row[0])
            prof.setTitle(row[1])
            prof.setName(row[2], row[3])
            prof.setEmail(row[4])
            prof.setPhoneNumber(row[5])
            prof.setWebsite(row[6])
            prof.setRooms(row[7])
            prof.setDepartment(row[8])
            prof.setResearchAreas(row[9])
            prof.setBio(row[10])
            profs.append(prof)
            row = cursor.fetchone()
        return profs

    def return_profs_list(self, profs):
        profs_list = []
        for prof in profs:
            prof_listing = []
            prof_listing.append(prof.getNetId())
            prof_listing.append(prof.getName())
            prof_listing.append(prof.getTitle())
            prof_listing.append(prof.getEmail())
            prof_listing.append(prof.getPhoneNumber())
            prof_listing.append(prof.getWebsite())
            rooms = " ".join(prof.getRooms())
            prof_listing.append(rooms)
            prof_listing.append(prof.getDepartment())
            researchAreas = " ".join(prof.getResearchAreas())
            prof_listing.append(researchAreas)
            prof_listing.append(prof.getBio())
            profs_list.append(prof_listing)
        return profs_list

    def print_profs(self, profs):
        profs_list = self.return_profs_list(profs)
        for prof in profs_list:
            prof_ = ''
            for item in prof:
                prof_ +=  ' ' + item
            print(prof_) 


if __name__ == '__main__':
    profsDB = profsDB()
    error_statement = profsDB.connect()
    if error_statement == '':
        cursor = profsDB.conn.cursor()
        profs = profsDB.displayAllProfessors(cursor)
        profsDB.print_profs(profs)
        profsDB.disconnect()
    else:
        print(error_statement)
        

