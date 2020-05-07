from os import environ
from os import path, stat
from sys import argv, stderr
from prof import Professor
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

class profsDB:

    def __init__(self):
        self.conn = None

    def connect(self):
        error_statement = ''

        try:
            engine = create_engine('postgresql://hmqcdnegecbdgo:c51235a04a7593a9ec0c13821f495f259a68d2e1ab66a93df947ab2f31970009@ec2-52-200-119-0.compute-1.amazonaws.com:5432/d99tniu8rpcj0o', poolclass=NullPool)
            # engine = create_engine(environ.get('DATABASE_URL'), poolclass=NullPool)
            self.conn = engine.connect()
        except Exception as e:
            error_statement = e
            print(error_statement, file=stderr)

        return error_statement

    def disconnect(self):
        self.conn.close()

    def displayAllProfessors(self, connection):
        stmtStr = 'SELECT profs.netid, profs.title, profs.first, profs.last, profs.email,' + \
                ' profs.phone, profs.website, profs.rooms, profs.department, profs.area,' + \
                ' profs.bio, profs.image, profs.image_actual, profs.image_extension, profs.past_papers' + \
                ' FROM profs ' + \
                ' ORDER BY profs.last ASC'
        result = connection.execute(stmtStr)
        return self.return_profs(result)

    def displayProfessorsByFilter(self, connection, search_criteria, input_arguments):
        stmtStr = 'SELECT profs.netid, profs.title, profs.first, profs.last, profs.email,' \
                ' profs.phone, profs.website, profs.rooms, profs.department, profs.area,' \
                ' profs.bio, profs.image, profs.image_actual, profs.image_extension, profs.past_papers' + \
                ' FROM profs' + \
                ' WHERE ' + search_criteria + \
                ' ORDER BY profs.last ASC'
        result = connection.execute(stmtStr, input_arguments)
        return self.return_profs(result)

    def return_profs(self, result): 
        profs = []
        for row in result:
            prof = Professor(row[0])
            prof.setTitle(row[1])
            prof.setFirstName(row[2])
            prof.setLastName(row[3])
            prof.setEmail(row[4])
            prof.setPhoneNumber(row[5])
            prof.setWebsite(row[6])
            prof.setRooms(row[7])
            prof.setDepartment(row[8])
            prof.setResearchAreas(row[9])
            prof.setBio(row[10])
            prof.setImagePath(row[11])
            prof.setActualImage(row[12])
            prof.setImageExtension(row[13])
            prof.setPastPapers(row[14])
            profs.append(prof)
        result.close()
        return profs

    def return_profs_list(self, profs):
        profs_list = []
        for prof in profs:
            prof_listing = []
            prof_listing.append(prof.getNetId())
            prof_listing.append(prof.getFirstName())
            prof_listing.append(prof.getLastName())
            prof_listing.append(prof.getTitle())
            prof_listing.append(prof.getEmail())
            prof_listing.append(prof.getPhoneNumber())
            prof_listing.append(prof.getWebsite())
            rooms = " ".join(prof.getRooms())
            prof_listing.append(rooms)
            prof_listing.append(prof.getDepartment())
            researchAreas = ", ".join(prof.getResearchAreas())
            prof_listing.append(researchAreas)
            prof_listing.append(prof.getBio())
            prof_listing.append(prof.getImagePath())
            prof_listing.append(prof.getActualImage())
            prof_listing.append(prof.getImageExtension())
            prof_listing.append(prof.getPastPapers())
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
        connection = profsDB.conn
        profs = profsDB.displayAllProfessors(connection)
        profsDB.print_profs(profs)
    else:
        print(error_statement)
    profsDB.disconnect()
        

