import psycopg2
import psycopg2.extras
import sys


def read_info(inputfile, templist):
    '''
    writes information from infolist into infofile by sublist item, 
    first line, the column headers, is written from header
    '''
    firstline = True
    with open(inputfile, 'r') as f:
        for line in f:
            if firstline:
                firstline = False
            else:
                line_info = line.strip().split(',')
                for i in range(len(line_info)):
                    if line_info[i] == 'NULL':
                        line_info[i] = None
                templist.append(line_info)
    return templist

def main():
    if len(sys.argv)<3:
        print("Usage: python3 %s <dbname> <directory_name>"%sys.argv[0])
        return

    dbname = sys.argv[1]

    print("starting database connection to ", dbname)

    conn = psycopg2.connect(database=dbname, host="127.0.0.1", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    print("Made database connection")

    dir_name = sys.argv[2]
    print("Files will be read from: %s"%dir_name)

    #gets user info
    userfile = dir_name + '/users.csv'
    users_info = []
    users_info = read_info(userfile, users_info)

#    print(users_info)

    #gets facs info
    facsfile = dir_name + '/facilities.csv'
    facs_info = []
    read_info(facsfile, facs_info)

#    print(facs_info)

    #gets asset info
    assetfile = dir_name + '/assets.csv'
    assets_info = []
    read_info(assetfile, assets_info)

#    print(assets_info)

    #gets transfers info
    transferfile = dir_name + '/transfers.csv'
    transfers_info = []
    read_info(transferfile, transfers_info)
	       
#    print(transfers_info)
	       
    #read user info into database
    for user in users_info:
        cur.execute('''INSERT INTO users (username, password, role_fk, active) 
VALUES ((%s), (%s), (SELECT role_pk FROM roles WHERE title=(%s)), (%s));''', (user[0], user[1], user[2], user[3])) 
    conn.commit()

    #read facility info into database
    for facility in facs_info:
        while len(facility) > 2:
            facility[1] = facility[1] + ',' + facility[2]
            facility.remove(facility[2])
        cur.execute('''INSERT INTO facilities (fac_code, common_name) VALUES 
((%s), (%s));''', (facility[0], facility[1]))
    conn.commit()

    #read asset info into database
    for asset in assets_info:
        cur.execute('''INSERT INTO assets (asset_tag, description, acq_date) 
VALUES ((%s), (%s), (%s));''', (asset[0], asset[1], asset[3]))
        cur.execute('''INSERT INTO asset_history (asset_fk, facility_fk, 
arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=(%s)), (SELECT 
facility_pk FROM facilities WHERE fac_code=(%s)), (%s));''', (asset[0], asset[2], asset[3]))
    conn.commit()

    #read transfer info into database
    for transfer in transfers_info:
        #insert requests
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=(%s);", (transfer[0],))
        a_pk = cur.fetchone()[0]
        
        cur.execute('''INSERT INTO transfer_requests (asset_fk, requester, 
req_time, approver, app_time, source, destination, load_dt, unload_dt) VALUES 
((%s), (SELECT user_pk FROM users WHERE username=(%s)), (%s), (SELECT user_pk 
FROM users WHERE username=(%s)), (%s), (SELECT facility_pk FROM facilities 
WHERE fac_code=(%s)), (SELECT facility_pk FROM facilities WHERE fac_code=(%s)), 
(%s), (%s));''', (a_pk, transfer[1], transfer[2], transfer[3], transfer[4], 
transfer[5], transfer[6], transfer[7], transfer[8]))
        #update asset history
        if transfer[7] != None:
            cur.execute('''UPDATE asset_history SET depart_dt=(%s) WHERE 
asset_fk=(%s) AND facility_fk=(SELECT facility_pk FROM facilities WHERE 
fac_code=(%s)) AND depart_dt IS NULL;''', (transfer[7], a_pk, transfer[5]))
            if transfer[8] != None:
                cur.execute('''INSERT INTO asset_history (asset_fk, facility_fk, arrive_dt) VALUES ((%s), (SELECT facility_pk FROM facilities WHERE fac_code=(%s)), (%s));''', (a_pk, transfer[6], transfer[8]))
    conn.commit()


    #deal with asset disposal
    for asset in assets_info:
        if asset[4] != None:
            #set last known facility's departure date
            cur.execute('''UPDATE asset_history SET depart_dt=(%s) WHERE asset_fk = 
(SELECT asset_pk FROM assets WHERE asset_tag=(%s)) AND depart_dt IS NULL AND 
facility_fk IS NOT NULL;''', (asset[4], asset[0]))
            #set disposal entry
            cur.execute('''INSERT INTO asset_history (asset_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=(%s)), (%s));''', (asset[0], asset[4]))
    conn.commit()

if __name__=='__main__':
    main()
