import psycopg2
from profsDB import profsDB

def writeImageLocation(conn, net_id, imagePath):
    try:
        image = open(imagePath, 'rb').read()
        cur = conn.cursor()
        stmt = ""
        stmt += "UPDATE profs"
        stmt += " SET image=%s"
        stmt += " WHERE netid=%s"
        cur.execute(stmt, (imagePath, net_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def read_Image(conn, net_id, path_to_dir):
    try:
        cur = conn.cursor()
        stmt = "SELECT image FROM profs WHERE netid = %s"
        cur.execute(stmt, (net_id, ))

        blob = cur.fetchone()
        print(blob[0])
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':

    hostname = 'ec2-52-200-119-0.compute-1.amazonaws.com'
    username = 'hmqcdnegecbdgo'
    password = 'c51235a04a7593a9ec0c13821f495f259a68d2e1ab66a93df947ab2f31970009'
    database = 'd99tniu8rpcj0o'

    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
    # replace netid with prof's netid
    netid = "wmassey"
    file_path = "static\profImages\\" + netid + ".jpg"
    writeImageLocation(conn, netid, file_path)
    conn.close()