import sys
import os
from DeadlineTracker import DeadlineTracker



# Run the application
if __name__ == "__main__":

    dt = DeadlineTracker()
    
    # Figure out if app is running graphicly in terminal or through system args

    if sys.argv[1] is None:
        # Graphicly in terminal
        print("Not implemented yet")
        pass

    elif sys.argv[1] == "date":
        try:
            date = sys.argv[2]
            if sys.argv[2] is None: print(f'Provide a date parameter like this: 2025y-8m-5d_15H:0M:0S')
            print(f'Script would have understood it as: {dt.parse_date(date)}')
        except IndexError:
            print("No date given to test")

        
    elif sys.argv[1] == "add":
        try:
            name = sys.argv[2]
            time = sys.argv[3]
            if name is None or time is None:
                print(f'Incorrectly given parameters')
                exit()
            
            dt.db_insert(name, time)
            print(f'New Deadline has been added!')
        except IndexError:
            print("Parameters not provided", sys.argv[2])

        except:
            print("Error within script")

    
    elif sys.argv[1] == "show":
        try:
            dt.db_get_deadlines(sys.argv[2])
        except IndexError:
            dt.db_get_deadlines()

    
    elif sys.argv[1] == "complete":
        try:
            n = int(sys.argv[2])
            dt.db_change_status(n)
            print(f'Provided ids status was changed')
        except ValueError:
            print(f'Error: Provided id is NaN')
        except IndexError:
            dt.db_get_completables()
            


    
    elif sys.argv[1] == "remove":
        
        n:int = -1
        try:
            n = int(sys.argv[2])
            dt.db_remove(n)
        except ValueError:
            print(f'Error: Provided id is NaN')
        except IndexError:
            print(f'Error: You need to provide an id of the deadline you what to remove as the parameter after remove')

    
    elif sys.argv[1] == "history":
        dt.db_deadline_history()

    elif sys.argv[1] in ["help", "-h", "-help", "--help"]:
        print(f"""          
Usage:
    python main.py <command> [other parameters]

Commands:
    {"help, -h":20}Shows help.
    {"add":20}Add deadline, requires 2 parameters, name and time, in this order
    \t1. name\t\"name of the deadline in between quotes\" 
    \t2. time\tTime of when to call this deadline
    \t\tPossible time notations: 2025y7m24d
    \t\tIf year is not given, time is added to current day: 7d; means 7 days from now
    {"remove":20}Delets the deadline, requires 1 parameter, id
    \t1. id\tYou can get this number with 'show' command
    {"history":20}Show history of completed deadlines
    {"show":20}Shows deadlines sorted with soonest first, has optional parameters
    \t-a\tDisplays all information of deadlines 
    {"date":20}Shows how a given date will be interpreted by script
    \t1. date\tWhatever date you want in format: XyXmXdXH
    \t\tX can be any number, the date cant have spaces.
    {"complete":20}Show deadlines that have passed due date, has optional parameter
    \tid\tMarks given deadline as completed.
    """)

    