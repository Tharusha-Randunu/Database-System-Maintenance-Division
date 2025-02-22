import mysql.connector
from mysql.connector import Error
from datetime import datetime

#connection to mysql     
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="maintenance"
    )
    if connection.is_connected():
        print("Connection to MySQL DB successful")
except Error as e:
    print(f"The error '{e}' occurred")
    




# Add a new asset
def add_asset(assetid,name,asset_type,asset_status,locid):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO asset (assetID,name,type,asset_status,locID) VALUES (%s,%s,%s,%s,%s)", (assetid,name,asset_type,asset_status,locid))
    connection.commit()
 
# Add a new issue
def add_issue(issueid,assetid,reportdate,description,issue_status):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO issue (issueID,assetID,reportdate,Description,issue_status) VALUES (%s,%s,%s,%s,%s)", (issueid,assetid,reportdate,description,issue_status))
    connection.commit()    

#Add new job
def add_job(jobid,issueid,startdate,enddate,job_status,remarks,cost):    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO job (jobID,issueID,startdate,enddate,job_status,remarks,Cost) VALUES (%s,%s,%s,%s,%s,%s,%s)", (jobid,issueid,startdate,enddate,job_status,remarks,cost))
    connection.commit() 


#Assign Employee to Job
def employee_assignment(jobid,empid,dateofassignment):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO emp_assignment (jobID,empID,date_of_assignment) VALUES (%s,%s,%s)", (jobid,empid,dateofassignment))
    connection.commit()




#Assign Tool to Job    
def assign_tools(jobid,toolid,dateborrowed,datereturned):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tool_usage (jobID,toolID,date_borrowed,date_returned) VALUES (%s,%s,%s,%s)", (jobid,toolid,dateborrowed,datereturned))
    connection.commit()



#Update Assets
def update_asset(current_assetid,new_assetid, new_name, new_type, new_status,new_locid):
    try:
        cursor = connection.cursor()
        sql = "UPDATE asset SET assetID = %s, name= %s, type = %s, asset_status = %s, locID = %s WHERE assetID = %s"
        values = (new_assetid, new_name, new_type, new_status,new_locid,current_assetid)
        cursor.execute(sql, values)
        connection.commit()
        print("\nAsset updated successfully.\n")
    except Error as e:
        #print(f"Error occurred: {e}")    
        print("\nThere was an error in updating.\n")



#Update Issue
def  update_issue(current_issueid,current_assetid,new_issueid,new_assetid, new_reportdate, new_description, new_status):
    try:
        cursor = connection.cursor()
        sql = "UPDATE issue SET issueID = %s,  assetID = %s, reportdate= %s, Description = %s, issue_status = %s WHERE issueID = %s AND assetid = %s"
        values = (new_issueid,new_assetid, new_reportdate, new_description, new_status,current_issueid,current_assetid)
        cursor.execute(sql, values)
        connection.commit()
        print("\nIssue updated successfully.\n")
    except Error as e:
        #print(f"Error occurred: {e}")    
        print("\nThere was an error in updating.\n")        

#Update Job
def update_job(current_jobid,current_issueid,new_jobid,new_issueid, new_startdate, new_enddate, new_status,new_remarks,new_cost):
    try:
        cursor = connection.cursor()
        sql = "UPDATE job SET jobID = %s, issueID=%s, startdate= %s, enddate=%s, job_status = %s,remarks= %s,Cost=%s  WHERE jobID = %s AND issueID = %s"
        values = (new_jobid,new_issueid, new_startdate, new_enddate, new_status,new_remarks,new_cost,current_jobid,current_issueid)
        cursor.execute(sql, values)
        connection.commit()
        print("\nJob updated successfully.\n")
    except Error as e:
        #print(f"Error occurred: {e}")    
        print("\nThere was an error in updating.\n")  

#update employee assignment
def  update_emp_assignment(current_jobid,current_empid,new_jobid, new_empid, new_dateofassignment):
    try:
        cursor = connection.cursor()
        sql = "UPDATE emp_assignment SET jobID = %s, empID=%s, date_of_assignment= %s WHERE jobID = %s AND empID=%s "
        values = (new_jobid,new_empid, new_dateofassignment, current_jobid, current_empid)
        cursor.execute(sql, values)
        connection.commit()
        print("\nEmployee assignment updated successfully.\n")
    except Error as e:
        #print(f"Error occurred: {e}")    
        print("\nThere was an error in updating.\n")  
        


#update tool usage
def update_tool_usage(current_jobid,current_toolid,new_jobid, new_toolid,new_dateborrowed,new_datereturned):
    try:
        cursor = connection.cursor()
        sql = "UPDATE tool_usage SET jobID = %s, toolID=%s,date_borrowed=%s, date_returned=%s WHERE jobID = %s AND toolID=%s "
        values = (new_jobid,new_toolid,new_dateborrowed, new_datereturned,current_jobid,current_toolid)
        cursor.execute(sql, values)
        connection.commit()
        print("\nTool usage updated successfully.\n")
    except Error as e:
        #print(f"Error occurred: {e}")    
        print("\nThere was an error in updating.\n")  


#search job
def search_job() :
    while True:
        print("\nSearch Job \n")
        print("1. Search by Job ID and Issue ID")
        print("2. Search by Date Range")
        print("3. Search by Status")
        print("4. Report Jobs with highest cost")
        print("5. Report All Jobs")
        print("6. Return to Main Menu\n")

        choice = input("Enter your choice: ")
        print()
        
        try:
            cursor = connection.cursor(dictionary=True)
            results = []

            #search by ID
            if choice == '1':
                job_id = int(input("Enter Job ID: "))
                issue_id = int(input("Enter Issue ID: "))
                sql = """
                    SELECT j.jobID, j.issueID, j.job_status,j.Cost, i.assetID
                    FROM job j
                    JOIN issue i ON j.issueID = i.issueID 
                    WHERE j.jobID = %s AND j.issueID = %s
                """
                cursor.execute(sql, (job_id,issue_id))
                results = cursor.fetchall()
            
            #search by date
            elif choice == '2':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                sql = """
                    SELECT j.jobID, j.issueID, j.job_status,j.Cost, i.assetID
                    FROM job j
                    JOIN issue i ON j.issueID = i.issueID
                    WHERE j.startdate >= %s AND j.enddate <= %s
                """
                cursor.execute(sql, (start_date, end_date))
                results = cursor.fetchall()    
                
            #search by status
            elif choice == '3':
                status = input("Enter status (finished/ongoing): ")
                sql = """
                    SELECT j.jobID, j.issueID, j.job_status,j.Cost, i.assetID
                    FROM job j
                    JOIN issue i ON j.issueID = i.issueID
                    WHERE j.job_status = %s
                """
                cursor.execute(sql, (status,))
                results = cursor.fetchall()
                
            #search by cost
            elif choice == '4':
             
                sql = """
                    SELECT j.jobID, j.issueID, j.job_status,j.Cost, i.assetID
                    FROM job j
                    JOIN issue i ON j.issueID = i.issueID
                    ORDER BY j.Cost DESC
                    LIMIT 5
                """
                cursor.execute(sql)
                results = cursor.fetchall()








            #search all
            elif choice == '5':
                sql = """
                    SELECT j.jobID, j.issueID, j.job_status,j.Cost, i.assetID
                    FROM job j
                    JOIN issue i ON j.issueID = i.issueID
                """
                cursor.execute(sql)
                results = cursor.fetchall()


            elif choice == '6':
                print("Returning to main menu")
                return



            print("")
            if results:
                for row in results:
                    print(f"Job ID: {row['jobID']}, Issue ID: {row['issueID']}, Asset ID: {row['assetID']}, Job Status: {row['job_status']}")
            else:
                print("No results found.")
                
        #except ValueError as ve:
            #print(f"Value error: {ve}")
        except Error as e:
           # print(f"An error occurred: {e}")
           print("There was an error while searching.")


#search employee assignment
def search_emp_assignment():
    while True:
        try:
            cursor = connection.cursor(dictionary=True)
            results = []
    
            job_id = int(input("\nEnter Job ID: "))
            sql = """
                SELECT a.jobID, a.empID, a.date_of_assignment, e.name, e.role
                FROM emp_assignment a
                JOIN employee e ON a.empID = e.empID
                WHERE a.jobID = %s
                """
            cursor.execute(sql, (job_id,))
            results = cursor.fetchall()
            

            print("")
            if results:
                for row in results:
                    print(f"Job ID: {row['jobID']}, Employee ID: {row['empID']}, Employee Name: {row['name']}, Employee Role: {row['role']}, Date of Assignment: {row['date_of_assignment']}")
            else:
                print("No results found.")

 
        #except ValueError as ve:
            #print(f"Value error: {ve}")
        except Error as e:
           # print(f"An error occurred: {e}")
            print("There was an error while searching.")
    
        retry = input("\nPress Enter to Try again or 1 to go back to Main menu.")
        if retry == '1':
            break        



#search tool usage
def search_tool_usage():        
    while True:
        try:
            cursor = connection.cursor(dictionary=True)
            results = []
    
            job_id = int(input("\nEnter Job ID: "))
            sql = """
                SELECT u.jobID, u.toolID, u.qty, u.date_borrowed, u.date_returned, t.name
                FROM tool_usage u
                JOIN tools t ON u.toolID = t.toolID
                WHERE u.jobID = %s
                """
            cursor.execute(sql, (job_id,))
            results = cursor.fetchall()
            

            print("")
            if results:
                for row in results:
                    print(f"Job ID: {row['jobID']}, Tool ID: {row['toolID']}, Tool Name: {row['name']}, Quantity: {row['qty']}, Date Borrowed: {row['date_borrowed']}, Date Returned: {row['date_returned']}")
            else:
                print("No results found.")

 
        #except ValueError as ve:
            #print(f"Value error: {ve}")
        except Error as e:
           # print(f"An error occurred: {e}")
            print("There was an error while searching.")
    
        retry = input("\nPress Enter to Try again or 1 to go back to Main menu.")
        if retry == '1':
            break











#UI
if __name__ == "__main__":
    while True:
        print("\nDAS Apparels - Maintenance Management System\n")
        print("Input Data                           Update Data                               Generate Reports\n")
        print("1. Add Asset                         9.  Update Asset                          17. Search Job")
        print("2. Add Location                      10. Update Location                       18. Search Employee Assignment")
        print("3. Add Employee                      11. Update Employee                       19. Search Tool Usage")
        print("4. Add Tool                          12. Update Tool"                                                   )
        print("5. Add Issue                         13. Update Issue"                                                   )
        print("6. Add Job                           14. Update Job                            20. Exit Program")
        print("7. Assign Employee to Job            15. Update Employee Assignment"                                             )
        print("8. Assign Tools for Job              16. Update Tools Usage                                                  \n")
        
   
        
        #Getting User Input
        choice = input("\nEnter your choice:")
        
        #Adding Data to Tables
        if choice == '1':
            while True:
                try:
                    assetid=int(input("\nEnter asset id: "))
                    name = input("Enter asset name: ")
                    asset_type = input("Enter asset type: ")
                    asset_status = input("Enter asset status: ")
                    locid = int(input("Enter location id: "))
                    add_asset(assetid,name,asset_type,asset_status,locid)
                    print("\nAsset added successfully.\n")
                #except ValueError as ve:
                #  print(f"Value error: {ve}")
                except Exception as e:
                # print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break
                
        elif choice == '5':
            while True:
                try:
                    issueid=int(input("\nEnter issue id: "))
                    assetid = int(input("Enter asset id: "))
                    reportdate = input("Enter issue reprtdate(YYYY-MM-DD): ")
                    description = input("Enter issue description: ")
                    issue_status = input("Enter issue status: ")
                    
                    add_issue(issueid,assetid,reportdate,description,issue_status)
                    print("\nIssue added successfully.\n")
                #except ValueError as ve:
                #  print(f"Value error: {ve}")
                except Exception as e:
                # print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break
        
        elif choice == '6':
            while True:
                try:
                    jobid=int(input("\nEnter job id: "))
                    issueid = int(input("Enter issue id: "))
                    startdate = input("Enter start date(YYYY-MM-DD): ")
                    enddate = input("Enter end date(YYYY-MM-DD): ")
                    job_status = input("Enter job status: ")
                    remarks= input("Enter remarks: ")
                    cost=float(input("Enter Cost:"))
                    add_job(jobid,issueid,startdate,enddate,job_status,remarks,cost)
                    print("\nJob added successfully.\n")
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break        
            
        elif choice == '7':
            while True:
                try:
                    jobid=int(input("\nEnter job id: "))
                    empid = int(input("Enter employee id: "))
                    dateofassignment = input("Enter date of assignment(YYYY-MM-DD): ")
                    employee_assignment(jobid,empid,dateofassignment)
                    print("\nEmployee assigned to job successfully.\n")
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break
             
        elif choice == '8':
            while True:
                try:
                    jobid=int(input("\nEnter job id: "))
                    toolid = int(input("Enter tool id: "))
                    dateborrowed = input("Enter borrowed date(YYYY-MM-DD): ")
                    datereturned = input("Enter returned date(YYYY-MM-DD): ")
                    assign_tools(jobid,toolid,dateborrowed,datereturned)
                    print("\nTool assigned to Job successfully.\n")
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break       


        #Updating tables
        elif choice == '9':
            while True:
                try:
                    current_assetid = int(input("Enter current asset id: "))
                    new_assetid = int(input("Enter new asset id: "))
                    new_name = input("Enter new asset name: ")
                    new_type = input("Enter new asset type: ")
                    new_status = input("Enter new asset status: ")
                    new_locid = int(input("Enter new location id: "))
                    update_asset(current_assetid,new_assetid, new_name, new_type, new_status,new_locid)
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break

        
        


        elif choice == '13':
            while True:
                try:
                    print()
                    current_issueid = int(input("Enter current issue id: "))
                    current_assetid = int(input("Enter current asset id: "))
                    new_issueid = int(input("Enter new issue id: "))
                    new_assetid = int(input("Enter new asset id: "))
                    new_reportdate = input("Enter new report date(YYYY-MM-DD): ")
                    new_description = input("Enter new description: ")
                    new_status = input("Enter new issue status: ")
                    
                    update_issue(current_issueid,current_assetid,new_issueid,new_assetid, new_reportdate, new_description, new_status)
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break
                
        elif choice == '14':
            while True:
                try:
                    current_jobid = int(input("Enter current job id: "))
                    current_issueid = int(input("Enter current issue id: "))
                    new_jobid = int(input("Enter new job id: "))
                    new_issueid = int(input("Enter new issue id: "))
                    new_startdate = input("Enter new start date(YYYY-MM-DD): ")
                    new_enddate = input("Enter new end date(YYYY-MM-DD): ")
                    new_status = input("Enter new job status: ")
                    new_remarks = input("Enter new remarks: ")
                    new_cost= float(input("Enter new cost: "))
                    update_job(current_jobid,current_issueid,new_jobid,new_issueid, new_startdate, new_enddate, new_status,new_remarks,new_cost)
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break

        elif choice == '15':
            while True:
                try:
                    current_jobid = int(input("Enter current job id: "))
                    current_empid = int(input("Enter current employee id: "))
                    new_jobid = int(input("Enter new job id: "))
                    new_empid = int(input("Enter new employee id: "))
                    new_dateofassignment = input("Enter new date of assignment(YYYY-MM-DD): ")
                    update_emp_assignment(current_jobid,current_empid,new_jobid, new_empid, new_dateofassignment)
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break

        elif choice == '16':
            while True:
                try:
                    current_jobid = int(input("Enter current job id: "))
                    current_toolid = int(input("Enter current tool id: "))
                    new_jobid = int(input("Enter new job id: "))
                    new_toolid = int(input("Enter new tool id: "))
                    new_dateborrowed = input("Enter new date borrowed(YYYY-MM-DD): ")
                    new_datereturned = input("Enter new date returned(YYYY-MM-DD): ")
                    update_tool_usage(current_jobid,current_toolid,new_jobid, new_toolid,new_dateborrowed,new_datereturned)
                #except ValueError as ve:
                    #print(f"Value error: {ve}")
                except Exception as e:
                    #print(f"An error occurred: {e}")  
                    print("\nEntered data does not match the required format.\n")
                    
                
                retry = input("Press Enter to Try again or 1 to go back to Main menu.")
                if retry == '1':
                    break

        elif choice == '17':
               search_job() 

        elif choice == '18':
            search_emp_assignment()

        elif choice == '19':
            search_tool_usage()
        
        elif choice == '20':
            print("\nYou have Excited the Program ")
            break

        
connection.close()
