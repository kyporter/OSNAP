import psycopg2
import psycopg2.extras
import sys


#active_dict = {'1' : 'True', '0' : 'False'}

def construct_name(dname, fname):
    '''concatenates directory with filename'''
    final_fname = dname + '/' + fname
    return final_fname

def write_info(infofile, header, infolist):
    '''
    writes information from infolist into infofile by sublist item, 
    first line, the column headers, is written from header
    '''
    with open(infofile, 'w') as f:
        f.write(header)
        for item in infolist:
            newrow = ','.join(item)
            newrow += '\n'
            f.write(newrow)

def main():
    if len(sys.argv)<3:
        print("Usage: python3 %s <dbname> <directory_name>"%sys.argv[0])
        return

    dbname = sys.argv[1]

#    print("starting database stuff exporting from %s", dbname)

    conn = psycopg2.connect(database=dbname, host="127.0.0.1", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
	##creating connection and cursor here hopefully makes it easier to locate and adjust as needed

#    print("Made database connection")

    #creates users_info
    cur.execute('''SELECT u.username, u.password, r.title, u.active FROM users u JOIN 
roles r ON u.role_fk=r.role_pk;''')
    users_info = cur.fetchall()
	#item in users_info: item[0]: username, item[1]: password, item[2]: role 
	#name, item[3]: integer 0 or 1 indicating inactive or active
    #make bools strings:
    for item in users_info:
        if item[3]:
            item[3] = 'True'
        else:
            item[3] = 'False'

#    print(users_info)

    #creates facs_info
    cur.execute('''SELECT fac_code, common_name FROM facilities WHERE common_name != 
'in transit';''')
    facs_info = cur.fetchall()
	#item in facs_info: item[0]: fcode, item[1]: common name

#    print(facs_info)

    #creates assets_info
	#create blank list
    assets_info = []

	#get asset tag, desc, acquisition date, primary key
    cur.execute('''SELECT asset_tag, description, acq_date, asset_pk FROM 
assets;''')
    asset_base = cur.fetchall()
	#item in asset_base: item[0]: asset tag, item[1]: description, item[2] 
	#acquired date as datetime object, item[3]: asset primary key(won't go 
	#in final list)

    for item in asset_base:
	#get fcode for each asset
        cur.execute('''SELECT f.fac_code FROM facilities f JOIN asset_history ah ON 
f.facility_pk=ah.facility_fk WHERE ah.asset_fk = (%s) AND ah.arrive_dt=(%s);''', (item[3], item[2]))
        faccode = cur.fetchone()[0] #since no asset can be disposed of on arrival, 
				    #fetchone() will never return None

	#get disposal date for each asset
        cur.execute('''SELECT arrive_dt FROM asset_history WHERE facility_fk IS 
NULL and asset_fk=(%s);''', (item[3],))
        disposal = cur.fetchone() #this may return unsubscriptable None
        if disposal != None:
            disposal_dt = disposal[0]
            disposal = disposal_dt.strftime("%m/%d/%Y")
        else:
	#if asset has not been disposed of, guidelines say to return 'NULL' as a string
            disposal = 'NULL'

	#put information to be transferred into a temporary variable
        temp_asset = [item[0], item[1], faccode, item[2].strftime('%m/%d/%Y'), disposal]
        assets_info.append(temp_asset)
	#item in assets_info: item[0]: asset tag, item[1]: description, 
	#item[2]: fcode, item[3]: acquired date, item[4]: disposal date or 
	#'NULL' if not disposed   

#    print(assets_info)

    #creates transfers_info
    cur.execute('''SELECT a.asset_tag, ur.username, tr.req_time, ua.username, 
tr.app_time, src.fac_code, dest.fac_code, tr.load_dt, tr.unload_dt FROM 
transfer_requests tr JOIN assets a ON a.asset_pk = tr.asset_fk JOIN facilities 
src ON src.facility_pk = tr.source JOIN facilities dest ON dest.facility_pk = 
tr.destination JOIN users ur ON ur.user_pk = tr.requester LEFT OUTER JOIN users ua ON 
tr.approver = ua.user_pk;''')
    transfers_info = cur.fetchall()
    #item in transfers_info: item[0]: asset tag, item[1]: requester 
    #username, item[2]: time of request, item[3]: approver username, 
    #item[4]: time of approval, item[5]: source fcode, item[6]: destination 
    #fcode, item[7]: load date, item[8]: unload date
    for item in transfers_info:
    #make datetime objects strings
        item[2] = item[2].strftime("%m/%d/%Y %H:%M")
        if item[3] == None:
            item[3] = 'NULL'
        if item[4] != None:
            item[4] = item[4].strftime("%m/%d/%Y %H:%M")
        else:
            item[4] = 'NULL'
        if item[7] != None:
            item[7] = item[7].strftime("%m/%d/%Y")
        else:
            item[7] = 'NULL'
        if item[8] != None:
            item[8] = item[8].strftime("%m/%d/%Y")
        else:
            item[8] = 'NULL'
	       
#    print(transfers_info)
	       
    dir_name = sys.argv[2]
#    print("Files will be written to: %s"%dir_name)

    user_fname = construct_name(dir_name, 'users.csv')
    fac_fname = construct_name(dir_name, 'facilities.csv')
    ast_fname = construct_name(dir_name, 'assets.csv')
    tran_fname = construct_name(dir_name, 'transfers.csv')

    user_header = 'username,password,role,active\n'
    fac_header = 'fcode,common_name\n'
    ast_header = 'asset_tag,description,facility,acquired,disposed\n'
    tran_header = 'asset_tag,request_by,request_dt,approve_by,approve_dt,source,destination,load_dt,unload_dt\n'

    write_info(user_fname, user_header, users_info)
    write_info(fac_fname, fac_header, facs_info)
    write_info(ast_fname, ast_header, assets_info)
    write_info(tran_fname, tran_header, transfers_info)


if __name__=='__main__':
    main()
