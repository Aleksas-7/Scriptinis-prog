
import os
import sqlite3
from datetime import datetime, date
# call_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
from re import search
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable

class DeadlineTracker:
    def __init__(self):
        self.deadline = None
        self.deadline_list = []

        self.db_connection = None
        self.db_cursor = None
        self.db_path = "deadlines.db"
        self.db_insert_query = """
            INSERT INTO deadlines 
            (name, record_date, due_date, status) 
            VALUES (?, ?, ?, ?)
        """
        self.db_setup()
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # name TEXT NOT NULL,
        # record_date TIMESTAMP NOT NULL,
        # due_date TIMESTAMP NOT NULL,
        # status INTEGER DEFAULT 1    #  'Pending' | 'Completed' | 'Overdue' # overdue was removed

        # self.statuses = {1: "Pending", 2: "Completed", 3: "Overdue"}
        



    def db_setup(self):

        if os.path.exists(self.db_path):
            self.db_connection = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.db_cursor = self.db_connection.cursor()
        else:
            response = input("Database not located, if you wish to create a new one type 'y': ")
            if response == 'y' or response == 'Y':
                self.db_connection = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
                self.db_cursor = self.db_connection.cursor()
            else:
                exit()
        

        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS deadlines 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                record_date TIMESTAMP NOT NULL,
                due_date TIMESTAMP NOT NULL,
                status INTEGER DEFAULT 1
            )
        """)

    def db_insert(self, name, due):
        # Query values (name, record_date, due_date, status)
        self.db_cursor.execute(self.db_insert_query, (name, datetime.now(), self.parse_date(due), 1))

        self.db_connection.commit()


    def parse_date(self, date_:str) -> datetime:
        # need to acount for:
        # Xy for X amount of years...
        # --
        # XH for X amount of hours...
        def extract_value(pattern, text):
            match_ = search(pattern, text)
            return int(match_.group(1)) if match_ else 0
        
        def clamp(n, smallest, largest): 
            return max(smallest, min(n, largest))
        
        def day_count(year, month) -> int:
            # Returns the amount of days in this month
            if month == 12:
                return int((date(year+1, 1, 1) - date(year, 12, 1)).days)
            return int((date(year, month, 1) - date(year, month, 1)).days)

        
        # print(f'From {date_}')

        # match_ = search("\d+y", date).group(1)
        
        y = clamp(extract_value(r"(\d+)y", date_), 0, 2050)
        m = clamp(extract_value(r"(\d+)m", date_), 0, 100)
        d = clamp(extract_value(r"(\d+)d", date_), 0, 1000)
        H = clamp(extract_value(r"(\d+)H", date_), 0, 500)
        M = clamp(extract_value(r"(\d+)M", date_), 0, 10000)
        S = clamp(extract_value(r"(\d+)S", date_), 0, 1000)
    
        #print(f'Given date is: {y}-{m}-{d} {H}:{M}:{S}')


        # need to figure out if the date is a specific one
        # or did the person intend for say a month from now.

        date_type = "specific" if y >= 2025 else "additive"
        
        if date_type == "specific":
            return datetime(
                clamp(y, datetime.now().year, 2050), 
                clamp(m, 1, 12), 
                clamp(d, 1, day_count(clamp(y, datetime.now().year, 2050), clamp(m, 1, 12))), 
                clamp(H, 0, 23), 
                clamp(M, 0, 59), 
                clamp(S, 0, 59))

        else:
            return datetime.now() + relativedelta(years=y, months=m, days=d, hours=H, minutes=M, seconds=S)

 


    def db_get_deadlines(self, flag:str = "important") -> list:
        
        table = PrettyTable()

        if flag == "-a":
            self.db_cursor.execute("""
                SELECT id, name, record_date, due_date, status
                FROM deadlines
                WHERE status IN(1, 2)
                ORDER BY due_date ASC
            """)
            # 1 - Pending, 3 - Overdue
            table.field_names = ["Id", "Name", "Record date", "Due date", "Status"]

        else: # flag == "important":
            self.db_cursor.execute("""
                SELECT name, strftime('%Y-%m-%d %H:%M:%S', due_date), status
                FROM deadlines
                WHERE status IN(1)
                ORDER BY due_date ASC
                LIMIT 50
            """)
            # 1 - Pending, 3 - Overdue
            table.field_names = ["Name", "Due date", "Status"]

        rows = self.db_cursor.fetchall()
        for row in rows:

            table.add_row(row)
        
        print(table)



    def db_remove(self, id_:int):
        self.db_cursor.execute("""
            SELECT id
            FROM deadlines
        """)
        ids = self.db_cursor.fetchall()

        # print(ids)
        # print([i[0] for i in ids])

        ids = [i[0] for i in ids]
        if id_ not in ids:
            print(f'Given id: {id_} does not exists amongst deadlines')
        else:
            # id exists within db, so delete it
            self.db_cursor.execute("""
                DELETE
                FROM deadlines
                WHERE id=?
            """, (id_,))
            self.db_connection.commit()


        
    def db_deadline_history(self):

        self.db_cursor.execute("""
            SELECT id, name, record_date, due_date, status
            FROM deadlines
            WHERE status=2
            ORDER BY due_date DESC
        """)
        # 2 - Completed

        table = PrettyTable()
        table.field_names = ["Id", "Name", "Record date", "Due date", "Status"]
        rows = self.db_cursor.fetchall()
        for row in rows:
            table.add_row(row)
        
        print(table)


    def db_get_completables(self):
        
        
        self.db_cursor.execute("""
            SELECT id, name, record_date, due_date, status
            FROM deadlines
            WHERE status=1
            ORDER BY due_date DESC
        """)
        # 2 - Completed

        table = PrettyTable()
        table.field_names = ["Id", "Name", "Record date", "Due date", "Status"]
        rows = self.db_cursor.fetchall()
        for row in rows:
            if row[3] < datetime.now():
                table.add_row(row)
        
        print(table)

    
    def db_change_status(self, id_:int, status:int = 2):
    
        self.db_cursor.execute("""
            SELECT id
            FROM deadlines
            WHERE status=1
        """)
        ids = self.db_cursor.fetchall()


        ids = [i[0] for i in ids]
        if id_ not in ids:
            print(f'Given id: {id_} does not exists amongst deadlines')
        else:
            # id exists within db, so delete it
            self.db_cursor.execute("""
                UPDATE deadlines
                SET status=2
                WHERE id=?
            """, (id_,))
            self.db_connection.commit()





            
















































    # def close(self):
    #     print(f'Deconstructor called!')
    #     self.db_connection.close()
    #     self.db_connection = None



    
        

