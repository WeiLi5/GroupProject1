import sqlite3
import datetime
import hashlib
import os.path
import getpass
import random

connection = None
cursor = None
is_login = False
is_end = False
user_type = None
user_id = None

# class User:
#     def __init__(self,user_id):
#         self.user_id = user_id
#     def get_id(self):
#         return self.user_id
# class Customer(User):
#     def __init__(self):
#         super(self,Customer).__init__()
#         self.basket = []


# Create hash function in here
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.create_function("hash", 1, encrypt)
    connection.commit()
    return


#Initialize table
def init_tables():
    global connection, cursor


    agent_query =   '''
                        CREATE TABLE agents (
                                    aid         TEXT,
                                    name        TEXT,
                                    pwd         TEXT,
                                    PRIMARY KEY (aid)
                                    );
                    '''

    store_query =   '''
                        CREATE TABLE stores (
                                    sid         INTEGER,
                                    name        TEXT,
                                    phone       TEXT,
                                    address     TEXT,
                                    PRIMARY KEY (sid)
                                    );
                    '''

    category_query ='''
                        CREATE TABLE categories (
                                    cat         CHAR(3),
                                    name        TEXT,
                                    PRIMARY KEY (cat)
                                    );
                    '''
    product_query = '''
                        CREATE TABLE products (
                                    pid         CHAR(6),
                                    name        TEXT,
                                    unit        TEXT,
                                    cat         CHAR(3),
                                    PRIMARY KEY (pid),
                                    FOREIGN KEY (cat) REFERENCES categories(cat)
                                    );
                    '''

    oline_query =   '''
                        CREATE TABLE olines (
                                    oid         INTEGER,
                                    sid         INTEGER,
                                    pid         CHAR(6),
                                    qty         INTEGER,
                                    uprice      REAL,
                                    PRIMARY KEY (oid, sid, pid),
                                    FOREIGN KEY (oid) REFERENCES orders(oid),
                                    FOREIGN KEY (sid) REFERENCES stores(sid),
                                    FOREIGN KEY (pid) REFERENCES products(pid)
                                    );
                    '''
    order_query =   '''
                        CREATE TABLE orders (
                                    oid         INTEGER,
                                    cid         TEXT,
                                    odate       DATE,
                                    address     TEXT,
                                    PRIMARY KEY (oid),
                                    FOREIGN KEY (cid) REFERENCES customers(cid)
                                    );
                    '''

    customer_query ='''
                        CREATE TABLE customers (
                                    cid         TEXT,
                                    name        TEXT,
                                    address     TEXT,
                                    pwd         TEXT,
                                    PRIMARY KEY (cid)
                                    );
                    '''

    carry_query =   '''
                        CREATE TABLE carries (
                                    sid         INTEGER,
                                    pid         CHAR(6),
                                    qty         INTEGER,
                                    uprice      REAL,
                                    PRIMARY KEY (sid,pid),    
                                    FOREIGN KEY (sid) REFERENCES stores(sid),
                                    FOREIGN KEY (pid) REFERENCES products(pid));
                    '''

    delivery_query = '''
                        CREATE TABLE deliveries (
                                    trackingno  INTEGER,
                                    oid         INTEGER,
                                    pickUpTime  DATE,
                                    dropOffTime DATE,
                                    PRIMARY KEY (trackingno,oid),
                                    FOREIGN KEY (oid) REFERENCES orders(oid));
                    '''

    cursor.execute(agent_query)
    cursor.execute(store_query)
    cursor.execute(category_query)
    cursor.execute(product_query)
    cursor.execute(oline_query)
    cursor.execute(order_query)
    cursor.execute(customer_query)
    cursor.execute(carry_query)
    cursor.execute(delivery_query)
    connection.commit()

    return

#For hash function
def encrypt(password):
    alg = hashlib.sha256()
    password = password.encode('UTF-8')
    alg.update(password)
    return alg.hexdigest()

# Initialize data
def init_data():
    global connection, cursor

    insert_agent = '''
                        INSERT INTO agents(aid, name, pwd) VALUES
                                ('qqq','wtq',hash('sss')),
                                ('abcde', 'Jack', hash('zxcvb')),
                                ('122dj', 'Mary', hash('d1290')),
                                ('dhaiw', 'Leo', hash('2312.4')),
                                ('ewyui', 'Anna', hash('www.123'));
                        '''

    insert_store = '''
                        INSERT INTO stores(sid, name, phone, address) VALUES
                                (1, '7-11', '7801001000', '103 78st'),
                                (2, 'aw', '7802002000', '10934 Whyte'),
                                (3, 'Tim', '7803003000', '103 & 111A st'),
                                (4, 'Save-on-food','7804004000', '9743 60Ave');
                       '''

    insert_category = '''
                        INSERT INTO categories(cat, name) VALUES
                                ('fru', 'fruit'),
                                ('dai', 'daily'),
                                ('dri', 'drink'),
                                ('ach', 'alcohol'),
                                ('veg', 'vegetable');
                        '''

    insert_product = '''
                        INSERT INTO products(pid, name, unit, cat) VALUES
                                ('123456', 'milk', 'bottle', 'dri'),
                                ('002390', 'broccoli', 'lb', 'veg'),
                                ('234576', 'apple', 'lb', 'fru'),
                                ('234598', 'banana', 'lb', 'fru'),
                                ('000930', 'Tissue', 'pack', 'dai'),
                                ('752894', 'vodka', 'bottle', 'ach'),
                                ('666777', 'potato', 'lb', 'veg');
                        '''

    insert_oline = '''
                        INSERT INTO olines(oid, sid, pid, qty, uprice) VALUES
                                (101, 1, '123456', 3, 3.1),
                                (103, 2, '123456', 5, 2.0),
                                (102, 2, '002390', 2, 6.2),
                                (203, 3, '234576', 1, 5.4),
                                (503, 4, '234598', 8, 6.7),
                                (782, 2, '000930', 9, 3.2),
                                (321, 2, '666777', 4, 2.1);
                        '''

    insert_order = '''
                        INSERT INTO orders(oid, cid, odate, address) VALUES
                                (101, 'sss', '2017-10-27', '10239 Jasper Ave'),
                                (103, 'sss', '2017-10-21', '12123 123 st'),
                                (102, 'www', '2017-10-27', '9910 107 st'),
                                (203, 'www', '2017-10-28', '9910 107 st'),
                                (503, 'uuu', '2017-10-28', '10390 Whyte Ave'),
                                (782, 'zzz', '2017-10-28', '8920 97 AVe'),
                                (321, 'www', '2017-10-29', '9910 107 st');
                        '''

    insert_customer = '''
                        INSERT INTO customers(cid, name, address, pwd) VALUES
                                ('aaa', 'wtq', 'No where', hash('123')),
                                ('sss', 'Amy', '10239 Jasper Ave', hash('sadqwe')),
                                ('www', 'Edward', '9910 107 st', hash('rye76y3')),
                                ('uuu', 'Osmar', '10390 Whyte Ave', hash('10003sw')),
                                ('zzz', 'Alex', '8920 97 Ave', hash('uuuio90.'));
                        '''

    insert_carry = '''
                        INSERT INTO carries(sid, pid, qty, uprice) VALUES
                                (1, '123456', 3, 3.1),
                                (2, '123456', 5, 2.6),
                                (2, '002390', 2, 6.2),
                                (3, '234576', 1, 5.4),
                                (4, '234598', 8, 6.7),
                                (2, '000930', 9, 3.2),
                                (2, '666777', 4, 2.1);
                        '''

    insert_delivery = '''
                        INSERT INTO deliveries (trackingno, oid, pickUpTime, dropOffTime) VALUES
                                (1345, 101, NULL , '2017-10-12'),
                                (1345, 103, '2017-10-29', '2017-10-12'),
                                (2468, 102, '2017-10-29', '2017-10-03'),
                                (2468, 203, '2017-10-29', '2017-10-03'),
                                (2390, 503, '2017-10-29', '2017-10-02'),
                                (2903, 782, '2017-10-29', '2017-10-11'),
                                (4420, 321, '2017-10-30', '2017-10-21');
                        '''
    cursor.execute(insert_agent)
    cursor.execute(insert_category)
    cursor.execute(insert_customer)
    cursor.execute(insert_product)
    cursor.execute(insert_store)
    cursor.execute(insert_order)
    cursor.execute(insert_delivery)
    cursor.execute(insert_carry)
    cursor.execute(insert_oline)

    connection.commit()
    return

# User will login as agent or customer
def login(table):

    uid = input(table[0].upper()+table[1:-1]+" ID: ")
    password = getpass.getpass()
    data = (uid, password)
    query = "SELECT * FROM {} WHERE {} = (?) AND pwd = hash(?)"\
            .format(table, table[0]+'id')
    cursor.execute(query, data)
    result = cursor.fetchall()
    if len(result):
        global is_login, user_type, user_id
        is_login = True
        user_type = table
        user_id = uid
    else:
        print("Username or password is incorrect!")

# The main screen to be displayed
# Ask user to login as Customer or Agent
# User can also sign up as new customer

def login_screen():

    instruction = "\n"+"-"*20+"\n"
    instruction += "1.\tCustomer Login\n"
    instruction += "2.\tAgent Login\n"
    instruction += "3.\tNew Customer Sign Up\n"
    instruction += "4.\tQuit\n"
    instruction += "-"*20

    print(instruction)
    option = input("Please enter an option -> ")
    if option == '1':
        login("customers")
    elif option == '2':
        login("agents")
    elif option == '3':
        signup()
    elif option == '4':
        global is_end
        is_end = True
    else:
        print("Invalid Option!")

# After the user login as a customer
# The customer menu will be displayed

def customer_menu():
    instruction = "\n"+"-"*20+"\n"
    instruction += "1.\tSearch for products\n"
    instruction += "2.\tPlace an order\n"
    instruction += "3.\tList orders\n"
    instruction += "4.\tLog Out\n"
    instruction += "-"*20

    print(instruction)
    option = input("Please enter an option -> ")
    if option == '1':
        search_products()
    elif option == '2':
        place_order()
    elif option == '3':
        list_orders()
    elif option == '4':
        global is_login
        is_login = False
    else:
        print("Invalid Option!")

# After the user login as a agent
# The agent menu will be displayed

def agent_menu():
    instruction = "\n"+"-"*20+"\n"
    instruction += "1.\tSet up a delivery\n"
    instruction += "2.\tUpdate a delivery\n"
    instruction += "3.\tAdd to stock\n"
    instruction += "4.\tLog Out\n"
    instruction += "-"*20

    print(instruction)
    option = input("Please enter an option -> ")
    if option == '1':
        setup_delivery()
    elif option == '2':
        update_delivery()
    elif option == '3':
        add_stock()
    elif option == '4':
        global is_login
        is_login = False
    else:
        print("Invalid Option!")


# Customer can enter keyword(s) to search products
def search_products():
    keywords = input("Please input one or more keywords: ").split()
    if not len(keywords):
        print("Enter At Least One Keyword!")
        return
    query = "SELECT pid from ("
    for i in range(len(keywords)):
        if i != 0:
            query += "union all "
        query += "select pid from products where name like '%{}%'".format(keywords[i])
    query += ")group by pid order by count(pid) DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    print (result)

# set up delivery
def setup_delivery():
    print("\nSetting up the new delivery...\n")
    trackNo = random.randint(1000,10000)
    cursor.execute("select trackingno from deliveries where trackingno = ?", (trackNo,))
    result = cursor.fetchone()
    print(result)
    while result:
        trackNo = random.randint(1000,10000)
        cursor.execute("select trackingno from deliveries where trackingno = ?", (trackNo,))
        result = cursor.fetchone()
    oid = input("Enter order ID: ")
    oid = oid.split()
    for o in oid:
        try:
            int(o)
        except ValueError:
            print("Invalid Input!")
            return

        cursor.execute("select oid from orders where oid = ?", (int(o),))
        result = cursor.fetchone()
        if not result:
            print("Order ID %s does not exist!" % o)
            return
        else:
            while True:
                pick_up_time = input("Adding pick up time for order %s [empty for null] " % o)
                if not pick_up_time:
                    pick_up_time = None
                    break
                else:
                    if not check_date(pick_up_time):
                        print("\nInvalid Time! \n")
                    else:
                        break
            try:
                cursor.execute("Insert into deliveries trackingno, oid, pickUpTime, dropOffTime) VALUES (?,?,?,NULL)",
                           (trackNo, o, pick_up_time))
                connection.commit()
                print("\nSuccessfully set up delivery for [ %s ] with tracking number: [" % o, trackNo, '] .\n')
            except sqlite3.Error as err: # no help :(
                print("Action Failed: " + str(err))
                print("Setup was not processed!")
                return

def update_delivery():
    trackNo = input("\nPlease enter the trackingno [empty to cancel]: ")
    if not trackNo:
        return
    try:
        int(trackNo)
    except ValueError:
        print("\nInvalid Input!")
        return
    trackNo = int(trackNo)
    cursor.execute("select * from deliveries where trackingno = ?", (trackNo,))
    result = cursor.fetchall()
    if not result:
        print("\n"+"-"*25)
        print("Tracking Number Not Found!")
        print("-"*25+"\n")
        return
    index = 0
    print("-"*50)
    for entry in result:
        index += 1
        print("%i.\t" % index, entry)
    print("-"*50+'\n')
    while True:
        choice = input("Select an order to modify -> ")
        try:
            if int(choice) > index:
                print("\nIndex Out of Range!\n")
            else:
                break
        except ValueError:
            print("\nInvalid Input!\n")
    while True:
        print("-"*45)
        print("1.\t Update Pick Up Time")
        print("2.\t Update Drop Off Time")
        print("3.\t Remove From Delivery")
        print("4.\t Cancel\t")
        print("-" * 45+'\n')
        action = input("Select an Operation -> ")
        oid = result[index - 1][1]
        if action == '1':
            while True:
                new_time = input("\nEnter the pick up time [empty for NULL]: ")
                if not new_time:
                    new_time = None
                    break
                elif check_date(new_time):
                    break
                else:
                    print("\nInvalid Time! \n")
            cursor.execute("update deliveries set PickUpTime = ? where oid = ?", (new_time, oid,))
            connection.commit()
            print("\nSuccessfully update the pick up time for order %i!\n" % oid)
        elif action == '2':
            while True:
                new_time = input("\nEnter the drop off time [empty for NULL]: ")
                if not new_time:
                    new_time = None
                    break
                elif check_date(new_time):
                    break
                else:
                    print("\nInvalid Time! \n")
            cursor.execute("update deliveries set dropOffTime = ? where oid = ?", (new_time, oid,))
            connection.commit()
            print("\nSuccessfully update the drop off time for order %i!\n" % oid)
        elif action == '3':
            confirm = input("Are you sure to remove the order from delivery? ['y' for confirmation] ")
            if confirm.upper() == 'Y':
                cursor.execute("delete from deliveries where oid = ?", (oid,))
                connection.commit()
                print("\nOrder %i has been removed from deliveries!\n" % oid)
                return
            else:
                print("\nAction has been aborted!")
        elif action == '4':
            return
        else:
            print("\nInvalid Input!\n")


def add_stock():
    

    query = "SELECT sid,c.pid,name,qty,uprice FROM carries c, products p WHERE c.pid = p.pid"
    cursor.execute(query)
    result = cursor.fetchall()
    for entry in result:
        print(entry)
    instruction = "\n" + "-" * 20 + "\n"
    instruction += "1.\tAdd to stock\n"
    instruction += "2.\tChange the unit price\n"
    instruction += "-" * 20

    print(instruction)
    option = input("Please enter an option ->")
    if option[0] == '1':
        sid = input("Enter store id : ")
        pid = input("Enter product id: ")
        qty = input("Enter the number of products to be added to the stock: ")
        change_qty = "UPDATE carries SET qty = qty + " + qty
        change_qty += " WHERE sid=" + sid + " and pid=" + pid
        cursor.execute(change_qty)
        connection.commit()
    elif option[0] == '2':
        sid = input("Enter store id : ")
        pid = input("Enter product id: ")
        uprice = input("Enter the unit price: ")
        change_price = "UPDATE carries SET uprice =" + uprice
        change_price += " WHERE sid=" + sid + " and pid=" + pid
        cursor.execute(change_price)
        connection.commit()
    else:
        print("Invalid option!")

def check_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def signup():
    uid = input("Customer ID: ")
    name = input("Customer Name: ")
    addr = input("Address: ")
    password = getpass.getpass()
    data = (uid, name, addr, password)
    query = "INSERT INTO customers VALUES(?,?,?,hash(?))"
    try:
        cursor.execute(query, data)
    except sqlite3.IntegrityError:
        print("Customer Id already exists!")
    else:
        global is_login, user_type, user_id, connection
        is_login = True
        user_type = "customers"
        user_id = uid
        connection.commit()


# Main function
def main():
    global connection, cursor

    path = ":memory:"
    # Check if the .db exist
    # If not exist, initialize the table and data
    if not os.path.isfile(path):
        connect(path)
        init_tables()
        init_data()
    else:
        connect(path)
    while not is_end:
        if not is_login:
            login_screen()
        elif user_type == "agents":
            agent_menu()
        else:
            customer_menu()
    connection.close()
    return

if __name__ == "__main__":
    main()