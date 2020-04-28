import psycopg2
from profsDB import profsDB
from prof import Professor

def updateDB(conn, prof):
    error_statement = ''
    returned = False
    
    # check if prof exists
    cur = conn.cursor()
    cur.execute("SELECT * FROM profs WHERE netid=%s", [prof.getNetId()])
    result = cur.fetchone()
    if result == None:
        return error_statement, returned
    try:
        cur = conn.cursor()
        stmt = ""
        stmt += "UPDATE profs"
        stmt += " SET email=%s,"
        stmt += " last=%s,"
        stmt += " first=%s,"
        stmt += " title=%s,"
        stmt += " phone=%s,"
        stmt += " website=%s,"
        stmt += " rooms=%s,"
        stmt += " department=%s,"
        stmt += " area=%s,"
        stmt += " bio=%s,"
        stmt += " image=%s"
        stmt += " WHERE netid=%s"
        
        prof_listing = []
        prof_listing.append(prof.getEmail())
        prof_listing.append(prof.getLastName())
        prof_listing.append(prof.getFirstName())
        prof_listing.append(prof.getTitle())
        prof_listing.append(prof.getPhoneNumber())
        prof_listing.append(prof.getWebsite())
        rooms = " ".join(prof.getRooms())
        prof_listing.append(rooms)
        prof_listing.append(prof.getDepartment())
        researchAreas = ", ".join(prof.getResearchAreas())
        prof_listing.append(researchAreas)
        prof_listing.append(prof.getBio())
        prof_listing.append(prof.getImagePath())
        prof_listing.append(prof.getNetId())

        cur.execute(stmt, prof_listing)
        conn.commit()
        cur.close()

        if conn is not None:
            conn.close()

        returned = True
        return error_statement, returned

    except (Exception, psycopg2.DatabaseError) as error:
        error_statement = str(error)
        print(error_statement)


def createProf(conn, prof):
    error_statement = ''
    try:
        cur = conn.cursor()
        stmt = "INSERT INTO profs(netid, email, last, first, title, phone, website, rooms, department, area, bio, image) VALUES"
        stmt += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        prof_listing = []
        prof_listing.append(prof.getNetId())
        prof_listing.append(prof.getEmail())
        prof_listing.append(prof.getLastName())
        prof_listing.append(prof.getFirstName())
        prof_listing.append(prof.getTitle())
        prof_listing.append(prof.getPhoneNumber())
        prof_listing.append(prof.getWebsite())
        rooms = " ".join(prof.getRooms())
        prof_listing.append(rooms)
        prof_listing.append(prof.getDepartment())
        researchAreas = ", ".join(prof.getResearchAreas())
        prof_listing.append(researchAreas)
        prof_listing.append(prof.getBio())
        prof_listing.append(prof.getImagePath())

        cur.execute(stmt, prof_listing)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        error_statement = str(error)
        print(error_statement)
    finally:
        if conn is not None:
            conn.close()
        return error_statement

def deleteProf(conn, netid):
    error_statement = ''
    try:
        cur = conn.cursor()
        stmt = "DELETE FROM profs WHERE netid=%s"

        cur.execute(stmt, (netid, ))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        error_statement = str(error)
        print(error_statement)
    finally:
        if conn is not None:
            conn.close()
        return error_statement

      
if __name__ == '__main__':

    ## testing 
    ## Warning: Calling this main method alters an entry in the 'profs' Database
    
    hostname = 'ec2-52-200-119-0.compute-1.amazonaws.com'
    username = 'hmqcdnegecbdgo'
    password = 'c51235a04a7593a9ec0c13821f495f259a68d2e1ab66a93df947ab2f31970009'
    database = 'd99tniu8rpcj0o'

    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)

    prof = Professor("aaa")
    prof.setTitle("Professor")
    prof.setFirstName("Amir Ali")
    prof.setLastName("Ahmadi")
    prof.setEmail("aaa@princeton.edu")
    prof.setPhoneNumber("(609) 258-6416")
    prof.setWebsite("http://aaa.princeton.edu/")
    prof.setRooms("Sherrerd Hall 329")
    prof.setDepartment("Operations Research and Financial Engineering")
    prof.setResearchAreas("Optimization, Operations Research")
    prof.setBio("""Development of computational tools for optimization
     of sociotechnical systems arising in operations research and 
     engineering, algebraic methods in optimization, semidefinite 
     programming, polynomial optimization, dynamical systems and control,
     Lyapunov methods for stability and robustness verification, 
     computational complexity in optimization, convex relaxations in
     combinatorial optimization, and applications of these tools to
     semialgebraic problems in statistics, economics, and systems theory.""")
    prof.setImagePath("static/profImages/aaa.png")
    conn.close()
    