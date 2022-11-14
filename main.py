import datetime
import requests
import time
import tabulate
import format
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='********',
                               port='3306', database='employee', autocommit=True)
if mydb.is_connected():
    print("Successfully Connected\n")
else:
    print("Error while connecting to DB\n")

username = 'User'
userid = '0000'

city = "mumbai"
url = "https://www.google.com/search?q=" + "weather" + city
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
data = str.split('\n')
crr_time = data[0]
sky = data[1]
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text
pos = strd.find('Wind')
other_data = strd[pos:]


def choose_module():
    format.star("Employee Management System", 3)
    print("Project by: Pratyush, Aadil, Vedanshi, Vidit")

    print("\n>>>>Howdy!<<<<"
          "\nToday is ", datetime.date.today(),
          "\nCurrent time", crr_time,
          "\nIt is currently", temp, " & ", sky, "in Mumbai")

    time.sleep(2)

    choice = int(input("\n>>Choose a module<<\n1. User\n2. Admin\n3. Exit\nEnter: "))
    if choice == 1:
        print("\nWelcome", username, "!")
        id = int(input("\n>>Enter your Employee ID: "))
        r = check_user(id)
        if r:
            user_menu()
        else:
            choose_module()
    elif choice == 2:
        password = input("\n>> Enter a wachtwoord: ")
        if password == 'banana':
            admin_menu()
        else:
            print("\n\n!!!!!!!!! Invalid Password !!!!!!!!!")
            time.sleep(2)
            choose_module()
    elif choice == 3:
        exit("Quiting Module....Sayonara!")
    else:
        choose_module()


def admin_menu():
    print("\nWelcome Admin!")
    print("\n>>ADMIN MODULE<<".center(50))
    choice2 = int(input("1. Add Employee\n2. Delete Employee\n3. Search"
                        "\n4. Disburse Salary\n5. Promote Employee\n6. View Employee Holidays"
                        "\n7. Logout\n\n>> "))

    if choice2 == 1:
        add_employee()
    if choice2 == 2:
        remove_employee()
    elif choice2 == 3:
        display_employee(2)
    elif choice2 == 4:
        disb_sal()
    elif choice2 == 5:
        promote()
    elif choice2 == 6:
        emp_leaves(2)
    elif choice2 == 7:
        format.star("Logging out.... Goodbye!", 3)
        print("\n")
        time.sleep(2)
        choose_module()


def user_menu():
    global username
    global userid

    format.star("Logged in as: " + username + " " + userid.__str__(), 3)
    print("\n>>USER MODULE<<".center(50))
    choice3 = int(input("1. See your Info\n2. Search Colleagues\n3. Apply for leave"
                        "\n4. View Salary info\n5. View Assigned Assets\n6. Logout\n\n>> "))

    if choice3 == 1 or choice3 == 2:
        display_employee(1)
    elif choice3 == 3:
        emp_leaves(1)
    elif choice3 == 4:
        view_sal()
    elif choice3 == 5:
        view_assets()
    elif choice3 == 6:
        username = "User"
        userid = "0000"
        format.star("Logging out.... Goodbye!", 3)
        print("\n")
        time.sleep(2)
        choose_module()


def check_user(e_id):
    try:
        my_cursor = mydb.cursor(buffered=True)
        sql = 'select name from employee where emp_id=%s'

        my_cursor.execute(sql, (e_id,))
        record = my_cursor.fetchall()
        r = my_cursor.rowcount

        global username
        global userid
        if r >= 1:
            for i in record:
                # print("\nHello,", i[0], "!\n")
                username = i[0]
            userid = e_id
            return True
            # user_menu()

        else:
            # print("Uh oh! Employee does not exist in the database!")
            time.sleep(2)
            return False
            # choose_module()

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        time.sleep(2)
        return False


def check_dept(d_id):
    try:
        sql = 'select dept_id from department where dept_id=%s'

        my_cursor = mydb.cursor(buffered=True)

        my_cursor.execute(sql, (d_id,))
        r = my_cursor.rowcount

        if r >= 1:
            return True
        else:
            return False

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)


def add_employee():
    # ADMIN ONLY
    my_cursor = mydb.cursor()

    format.star("ADD RECORDS", 3)
    print("\nTo input data into organisation's employee database\n")

    id = int(input("1. Enter Employee's ID: "))
    dept_id = int(input("2. Enter Employee's Department ID: "))

    if check_user(id):
        print("Employee already exists in the database!")
        time.sleep(2)
        x = int(input("\n>>Choose an option:\n1. Retry Input\n2. Go back\n"))
        if x == 1:
            add_employee()
        else:
            admin_menu()

    if not check_dept(dept_id):
        print("Department ID is invalid!")
        time.sleep(2)
        x = int(input("\n>>Choose an option:\n1. Retry Input\n2. Go back\n"))
        if x == 1:
            add_employee()
        else:
            admin_menu()

    else:
        name = input("3. Enter Employee Name: ")
        job_title = input("4. Enter Employee Job Title: ")
        gender = input("5. Enter Employee's gender: ")
        age = int(input("6. Enter Employee's age: "))
        add = input("7. Enter Employee's address : ")
        mail = input("8. Enter Employee's email address : ")
        phone = input("9. Enter Employee's phone number : ")

        sql2 = 'insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        inp_data = (id, name, job_title, gender, age, add, mail, phone, dept_id)
        my_cursor.execute(sql2, inp_data)

        print("\nEmployee details added Successfully!!")
        time.sleep(2)
        admin_menu()


def remove_employee():
    # ADMIN ONLY
    my_cursor = mydb.cursor()
    format.star("REMOVE RECORDS", 3)
    print("\nTo remove data into organisation's employee database\n")

    id = int(input("\n>> Enter Employee ID to be removed: "))

    if not check_user(id):
        print("Employee does not exist in the database!")
        time.sleep(2)
        x = int(input("\n>>Choose an option:\n1. Retry Input\n2. Go back\n"))
        if x == 1:
            remove_employee()
        else:
            admin_menu()

    else:
        sql1 = 'SET FOREIGN_KEY_CHECKS=0;'
        sql = 'delete from employee where emp_id=%s'
        sql2 = 'SET FOREIGN_KEY_CHECKS=0;'

        print("!!! Are you sure you want to delete data of employee", id, "from the database, forever?")
        ans = input("\nPress any key to abort or F to continue...\n>> ")
        if ans == 'F':
            print("Updating database....")
            my_cursor.execute(sql1)
            my_cursor.execute(sql, (id,))
            my_cursor.execute(sql2)

            print("\nEmployee details removed Successfully!")
            time.sleep(2)
            admin_menu()

        else:
            admin_menu()


def display_employee(choice):
    my_cursor = mydb.cursor()
    format.star("EMPLOYEE INFORMATION", 3)
    print("\nTo display organisation's employee information\n")

    if choice == 1:
        # USER
        global username
        global userid
        choice3 = int(input("\n>>>USER FILTERS<<<\n1. View your Info\n2. View a colleague's info\n3. Go back\n\n>> "))

        if choice3 == 1:
            sql = 'select * from employee where emp_id=%s'
            my_cursor.execute(sql, (userid,))
            res = my_cursor.fetchall()

            print(
                tabulate.tabulate(res, headers=['ID', 'Name', 'Job Title', 'Gender', 'Age', 'Address', 'Email',
                                                'Phone', 'Department'], tablefmt='psql'))

        elif choice3 == 2:
            try:
                id = int(input(">> Enter Employee's ID to search: "))
                sql = 'select emp_id, name, job_title, email, phone, dept_name, location from employee ' \
                      'natural join department where emp_id=%s;'
                my_cursor.execute(sql, (id,))
                res = my_cursor.fetchall()
                r = my_cursor.rowcount

                if r >= 1:
                    print(
                        tabulate.tabulate(res, headers=['ID', 'Name', 'Job Title', 'Email',
                                                        'Phone', 'Department', 'Location'], tablefmt='psql'))
                else:
                    print("Uh oh! Employee", id, "does not exist in the database!")

            except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)

        elif choice3 == 3:
            user_menu()

    elif choice == 2:
        # ADMIN
        choice2 = int(input("\n>>>ADMIN FILTER<<<"
                            "\n1. Display all employee details\n2. Display Particular Employee\n3. Go back\n\n>> "))

        if choice2 == 1:
            sql = 'select * from employee'
            my_cursor.execute(sql)

            res = my_cursor.fetchall()
            print(tabulate.tabulate(res, headers=['ID', 'Name', 'Job Title', 'Gender', 'Age', 'Address', 'Email',
                                                  'Phone', 'Department'], tablefmt='psql'))

        elif choice2 == 2:
            try:
                id = int(input(">>Enter your Employee ID: "))
                sql = 'select * from employee where emp_id=%s'
                my_cursor.execute(sql, (id,))
                res = my_cursor.fetchall()
                r = my_cursor.rowcount

                if r >= 1:
                    print(
                        tabulate.tabulate(res, headers=['ID', 'Name', 'Job Title', 'Gender', 'Age', 'Address', 'Email',
                                                        'Phone', 'Department'], tablefmt='psql'))
                else:
                    print("Uh oh! Employee", id, "does not exist in the database!")

            except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)

        elif choice2 == 3:
            admin_menu()

    time.sleep(3)
    display_employee(choice)


def disb_sal():
    # ADMIN ONLY
    format.star("SALARY MODULE", 3)
    print("\nTo calculate employee pay out's\n")

    id = int(input(">> Enter Employee's ID: "))

    if not check_user(id):
        print("Employee does not exist in the database!")
        time.sleep(2)
        x = int(input("\n>>Choose an option:\n1. Retry Input\n2. Go back\n"))
        if x == 1:
            disb_sal()
        else:
            admin_menu()
    else:
        try:
            sql = 'select max(amount), bonus from salary where emp_id=%s order by date_last_given desc'
            sql2 = 'select max(salary_id) from salary'
            sql3 = 'insert into salary values(%s,%s,%s,%s,%s)'
            sql4 = 'select count(leave_id) from leave_info where emp_id=%s'
            my_cursor = mydb.cursor(buffered=True)

            my_cursor.execute(sql, (id,))
            record = my_cursor.fetchall()
            r = my_cursor.rowcount

            sal = 0
            bonus = 0
            if r >= 1:
                for i in record:
                    bonus = int(i[1])
                    sal = int(i[0])
                print("\nPREVIOUS BASIC SALARY: ", sal, "\nPREVIOUS BONUS: ", bonus,
                      "\nPREVIOUS TOTAL SALARY: ", sal + bonus, "\n")
            else:
                print("\nPREVIOUS SALARY INFORMATION FOR EMP_ID", id, "UNAVAILABLE!\n")
                sal = int(input("Enter salary amount: "))

            my_cursor.execute(sql4, (id,))
            count = my_cursor.fetchall()
            c = 0
            for i in count:
                c = i[0]

            print("TOTAL LEAVES TAKEN: ", c)

            increase = int(input("Enter increase in Salary: "))
            bonus = int(input("Enter bonus amount: "))
            date = datetime.datetime.today().strftime('%Y-%m-%d')

            total = (sal + increase + bonus) - (int(c) * 1000)

            my_cursor.execute(sql2)
            prev_sal_id = my_cursor.fetchall()
            p = 0

            for i in prev_sal_id:
                p = int(i[0])

            d = (p + 1, total, bonus, date, id)
            my_cursor.execute(sql3, d)

            print("\nSalary disbursed!")
            time.sleep(2)
            admin_menu()

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)


def promote():
    # ADMIN ONLY
    format.star("EMPLOYEE PROMOTIONS", 3)
    print("\nTo promote an employee\n")

    id = int(input(">> Enter Employee's ID: "))

    if not check_user(id):
        print("Employee does not exist in the database!")
        time.sleep(2)
        x = int(input("\n>>Choose an option:\n1. Retry Input\n2. Go back\n"))
        if x == 1:
            promote()
        else:
            admin_menu()
    else:
        try:
            sql = 'select max(amount), bonus from salary where emp_id=%s order by date_last_given desc'
            my_cursor = mydb.cursor(buffered=True)

            my_cursor.execute(sql, (id,))
            record = my_cursor.fetchall()
            r = my_cursor.rowcount

            sal = 0
            bonus = 0

            if r >= 1:
                for i in record:
                    bonus = int(i[1])
                    sal = int(i[0])
                print("\nPREVIOUS BASIC SALARY: ", sal, "\nPREVIOUS BONUS: ", bonus,
                      "\nPREVIOUS TOTAL SALARY: ", sal + bonus, "\n")
            else:
                print("\nPREVIOUS SALARY INFORMATION FOR EMP_ID", id, "UNAVAILABLE!\n")

            title = input("Enter new job title: ")
            amount = int(input("Enter increase in Salary: "))
            t = sal + amount

            sql2 = 'update salary set amount=%s where emp_id=%s'
            d = (t, id)
            my_cursor.execute(sql2, d)

            sql3 = 'update employee set job_title=%s where emp_id=%s'
            d = (title, id)
            my_cursor.execute(sql3, d)

            print("\nEmployee has been promoted and it's information updated!")
            time.sleep(2)
            admin_menu()

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)


def emp_leaves(choice):
    format.star("HOLIDAY RECORDS", 3)
    print("\nTo view/ update employee's leave information\n")

    my_cursor = mydb.cursor()

    if choice == 1:
        # USER
        global username
        global userid

        sql2 = ' select max(salary_id) from salary;'
        my_cursor.execute(sql2)
        record = my_cursor.fetchall()

        reason = input("1. Reason for leave: ")
        from_d = input("2. Out from (format- yyyy-mm-dd): ")
        to_d = input("3. Out until (format- yyyy-mm-dd): ")

        sql2 = 'insert into leave_info values(%s,%s,%s,%s,%s)'

        prev_id = 0
        for i in record:
            prev_id = int(i[0])

        inp_data = (prev_id + 1, userid, reason, from_d, to_d)
        my_cursor.execute(sql2, inp_data)

        print("\nLeave details added Successfully!!")
        time.sleep(2)
        user_menu()

    elif choice == 2:
        # ADMIN
        try:
            id = int(input(">> Enter Employee ID: "))
            if not check_user(id):
                print("Employee does not exist in the database!")
                time.sleep(2)
                admin_menu()

            sql = 'select * from leave_info where emp_id=%s'
            my_cursor.execute(sql, (id,))
            res = my_cursor.fetchall()
            r = my_cursor.rowcount

            if r >= 1:
                print(
                    tabulate.tabulate(res, headers=['Leave ID', 'Emp ID', 'Reason', 'From', 'To'], tablefmt='psql'))
            else:
                print("Employee", id, "does not have any registered leaves!")

            time.sleep(3)
            admin_menu()

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)


def view_assets():
    # USER ONLY
    format.star("VIEW ASSETS", 3)
    print("\nTo view employee's allotted assets\n")

    my_cursor = mydb.cursor()
    time.sleep(2)

    try:
        global userid
        global username
        sql = 'select * from org_assets where emp_id=%s'
        my_cursor.execute(sql, (userid,))
        res = my_cursor.fetchall()
        r = my_cursor.rowcount

        if r >= 1:
            print(
                tabulate.tabulate(res, headers=['Asset Code', 'Type', 'Description', 'Emp Id', 'Allotment Date', 'Qty'],
                                  tablefmt='psql'))
        else:
            print("Uh oh! Employee", userid, "does not exist in the database!")

        time.sleep(3)
        user_menu()

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)


def view_sal():
    # USER ONLY
    format.star("VIEW SALARY", 3)
    print("\nTo view employee's salary record\n")

    my_cursor = mydb.cursor()

    try:
        global userid
        global username

        sql = 'select * from salary where emp_id=%s order by date_last_given desc'
        my_cursor.execute(sql, (userid,))
        res = my_cursor.fetchall()
        r = my_cursor.rowcount

        if r >= 1:
            print(
                tabulate.tabulate(res, headers=['Salary ID', 'Amount', 'Bonus', 'Date Given', 'Emp ID'],
                                  tablefmt='psql'))
        else:
            print("Uh oh! Employee", id, "does not exist in the database!")

        time.sleep(3)
        user_menu()

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)


choose_module()
