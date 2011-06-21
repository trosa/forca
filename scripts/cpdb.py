"""
Usage:

   python web2py.py -S app -M -N -R scripts/cpdb.py -A 'sqlite://other_db.sqlite'

It will copy all data from current db to other_db (sqlite or not)

The -A argument can be any URI string for example

   'mysql://username:password@localhost/dbname'

The new records may have a different 'id' than the original but
it will fix all references automatically.
"""

import sys, os

def main():
    other_db = DAL(sys.argv[1])
    print 'creating tables...'
    for table in db:
        other_db.define_table(table._tablename,*[field for field in table])
        # uncomment to erase all previous records
        # other_db[table._tablename].truncate()
    print 'exporting data...'
    tmpfile = open('tmp.sql','wb')
    try:
        db.export_to_csv_file(tmpfile)
    finally:
        tmpfile.close()
    print 'importing data...'
    tmpfile = open('tmp.sql','rb')
    try:
        other_db.import_from_csv_file(tmpfile)
    finally:
        tmpfile.close()
    other_db.commit()
    print 'done!'
    print 'Attention: do not run this program again or you end up with duplicate records'

if __name__=='__main__': main()


