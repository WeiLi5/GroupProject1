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
basket = []

class Item:
    def __init__(self,store_name,store_id,product_name,product_id,unit,price,qty):
        self.store_name = store_name
        self.store_id = store_id
        self.product_name = product_name
        self.product_id = product_id
        self.unit = unit
        self.qty = qty
        self.price = price
    def set_qty(self,qty):
        self.qty = qty

    def get_tuple(self):
        return(self.product_name,self.product_id,self.store_name,self.store_id,self.unit,self.price,self.qty)

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
                                    trackingNo  INTEGER,
                                    oid         INTEGER,
                                    pickUpTime  DATE,
                                    dropOffTime DATE,
                                    PRIMARY KEY (trackingNo,oid),
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
                                (101, 2, '234576', 3, 3.1),
                                (103, 2, '123456', 5, 2.0),
                                (103, 2, '234576', 5, 2.0),
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
                                (4, '234576', 1, 2.4),
                                (2, '234576', 0, 1.4),
                                (1, '234576', 0, 0.4),
                                (4, '234598', 8, 6.7),
                                (2, '000930', 9, 3.2),
                                (2, '666777', 4, 2.1);
                        '''

    insert_delivery = '''
                        INSERT INTO deliveries (trackingNo, oid, pickUpTime, dropOffTime) VALUES
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
    global uid

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


def place_order():
    global basket,cursor
    while 1:
        if not len(basket):
            print("You have no item in your basket")
            return
        all_checked = True
        for i in range(len(basket)):
            item = basket[i]
            row = item.get_tuple()
            pid = row[1]
            sid = row[3]
            qty = row[-1]

            query = "select qty from carries where sid =? and pid=?"
            data = (sid,pid)
            cursor.execute(query,data)
            result = cursor.fetchall()
            if not len(result):
                print("The store no longer carries this product!")
                return
            if result[0][0] < qty:
                print("The quantity for product(%s) in store(%s) is:\t%d"%(row[0],row[2],result[0][0]))
                print("The quantity for this product and this store in your basket is:\t%d"%(qty))
                print("Please change your quantity")
                modify_item({'index':i})
                qty = item.get_tuple()[-1]
                all_checked = False
                break
        if all_checked:
            # generate unique id
            print("\nSetting up the new delivery...\n")
            orderNo = random.randint(100,1000)
            cursor.execute("select oid from orders where oid = ?", (orderNo,))
            checkDup = cursor.fetchone()
            while checkDup:
                orderNo = random.randint(100,1000)
                cursor.execute("select oid from orders where oid = ?", (orderNo,))
                checkDup = cursor.fetchone()


            # get user address
            cursor.execute("select address from customers where cid = ?", (uid,))
            address=cursor.fetchone()

            now=datetime.datetime.today().strftime('%Y-%m-%d')
            print(now)



            #insert into order
            #bugs in here
            cursor.execute("Insert into orders (oid, cid, odate, address) VALUES (?,?,?,?)",(orderNo,uid,now,address))
            connection.commit()

            while (len(basket)):
                item = basket.pop()
                row = item.get_tuple()
                pid = row[1]
                sid = row[3]
                qty = row[-1]
                uprice=row[-2]

                #cursor.execute("Insert into orders (trackingNo, oid, pickUpTime, dropOffTime) VALUES (?,?,?,NULL)",
                          # (trackNo, o, pick_up_time))
                #connection.commit()
                

                # insert into olines
                cursor.execute("Insert into olines (oid, sid, pid, qty, uprice) VALUES (?,?,?,?,?)",
                           (orderNo, sid, pid, qty, uprice))
                connection.commit()

            break
            

#def list_order():
    # kwarg = {'function':table_row}

#def table_row(kwarg):
    # kwarg = {'row':[]}




# After the user login as a customer
# The customer menu will be displayed
def customer_menu():
    instruction = "\n"+"-"*20+"\n"
    instruction += "1.\tSearch for products\n"
    instruction += "2.\tPlace an order\n"
    instruction += "3.\tList orders\n"
    instruction += "4.\tModify Basket\n"
    instruction += "5.\tLog Out\n"
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
        modify_basket()
    elif option == '5':
        global is_login,basket
        is_login = False
        basket = []
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

def modify_basket():
    cols = ["Product Name","Product ID","Store Name","Store ID","  Unit  ","Price","Quantity"]
    end = False
    page = 0
    result = []
    for item in basket:
        result.append(item.get_tuple())
    while not end:
        print("*** Select item to modify qty, set to 0 to delete it! ***")
        end,page = table_menu(result,cols,page,{'function':modify_item})

def modify_item(kwarg):
    global basket
    index = kwarg['index']
    item = basket[index]
    while 1:
       qty = input("You want change quantity to(set to 0 to delete it): ")
       if not len(qty):
           qty = 1
           break
       try:
           qty = int(qty)
       except:
           continue
       else:
           break
    if qty <= 0:
        basket.pop(index)
    else:
        item.set_qty(qty)
        
# Customer can enter keyword(s) to search products
def search_products():
    keywords = input("Please input one or more keywords: ").split()
    if not len(keywords):
        print("Enter At Least One Keyword!")
        return
    query = '''
    select r1.pid,r1.name,r1.unit,ifnull(r2.num_stores,0) as number_of_stores,
    ifnull(r2.min_price,0) as minmum_price,
    ifnull(r3.num_stores,0) as number_of_on_stock_stores,ifnull(r3.min_price,0) as minmum_on_stock_price,
    ifnull(r4.num_orders,0) as number_of_orders_within_7_days
    from
    '''
    query += "(SELECT * from ("
    for i in range(len(keywords)):
        if i != 0:
            query += "union all "
        query += "select * from products where name like '%{}%'".format(keywords[i])
    query += ")group by pid order by count(*) DESC) as r1"
    query += '''
    left outer join
    (
	select p.pid,count(*) as num_stores,min(c.uprice) as min_price
	from products p,carries c
	where p.pid = c.pid
	group by p.pid
	
    ) as r2
    on r1.pid = r2.pid
    left outer join
    (
	select p.pid,count(*) as num_stores,min(c.uprice) as min_price
	from products p,carries c
	where p.pid = c.pid and c.qty > 0
	group by p.pid
	
    ) as r3
    on r2.pid = r3.pid
    left outer join
    (
       select l.pid,count(*) as num_orders
       from olines l, orders o
       where l.oid = o.oid and o.odate > datetime('now','-7 days')
       group by l.pid
    )r4
    on r3.pid = r4.pid

    '''
    cursor.execute(query)
    result = cursor.fetchall()

    if not len(result):
        print("No Result Found!")
        return
    end = False
    page = 0
    while not end:
        print("*** Select product to see more details ***")
        end,page = table_menu(result,["Product ID","    Name    ","  Unit  ","#Stores","Min Price","#Stores On Stock",\
                                      "Min Price On Stock","#Orders Within 7 days"],page,{'function':product_detail})


def product_detail(kwarg):
    global cursor
    pid = kwarg['row'][0]
    query = '''
    select  r2.sid,r2.name,r2.phone,r2.address,r1.uprice,r1.qty,ifnull(r3.num_orders,0) from
    (
       select *
       from carries
       where pid = ?
       order by
       case when qty = 0 then uprice end,
       case when qty > 0 then uprice end
    )as r1
    left outer join
    (
	select *
	from stores
    )as r2
    on r2.sid = r1.sid
    left outer join
    (
	select sid,count(*) as num_orders
	from orders o, olines l
	where odate > datetime('now','-7 days') and
	      l.pid = ? and
	       o.oid = l.oid
	group by l.sid
    ) as r3
    on r2.sid = r3.sid
'''

    data = (pid,pid)
    cursor.execute(query,data)
    result = cursor.fetchall()
    cols = ["Store ID","   Store Name   "," Store Contact ","    Store Address    ","Price"\
            ,"Quantity","# of orders within 7 days"]

    query = '''
    select * from products where pid = ?
    '''
    data = (pid,)
    cursor.execute(query,data)
    info = cursor.fetchone()

    query = '''select name from categories where cat = ?'''
    data = (info[3],)
    cursor.execute(query,data)
    category = cursor.fetchone()[0]
    

    end = False
    page = 0
    while not end:
        print("--------------------------------------")
        print("Product ID\t\t: "+str(info[0]))
        print("Product Name\t\t: "+str(info[1]))
        print("Product Unit\t\t: "+str(info[2]))
        print("Product Category\t: "+category)
        print("*** Select store to add to your basket ***")
        end,page = table_menu(result,cols,page,{'function':add_basket,'product':kwarg['row']})

def add_basket(kwarg):
    global basket
    pid = kwarg['product'][0]
    pname = kwarg['product'][1]
    unit = kwarg['product'][2]
    sid = kwarg['row'][0]
    sname = kwarg['row'][1]
    price = kwarg['row'][4]
    while 1:
        qty = input("How many this product you want put in basket(press enter for default 1):\t")
        if not len(qty):
            qty = 1
            break
        try:
            qty = int(qty)
        except:
            continue
        else:
            break
    if qty >  0:
        item = Item(sname,sid,pname,pid,unit,price,qty)
        basket.append(item)
    
def table_menu(table,cols,page,kwarg):
    header = "|Option|"
    length = [len(header)-2]
    for col in cols:
        header += "{}|".format(col)
        length.append(len(col))
    spliter = "-"*len(header)
    print(spliter)
    print(header)
    print(spliter)

    start = page*5
    end = min(page*5+5,len(table))
    choice = ""
    for i in range(start,end):
        content = str(i-start+1)
        row_string = "|{}{}|".format(content,(length[0]-len(content))*" ")
        row = table[i]
        for j in range(len(row)):
            content = str(row[j])
            row_string += "{}{}|".format(content,(length[j+1]-len(content))*" ")
        print(row_string)
        print(spliter)
        choice += str(i-start+1)
    print("6.\tBack to Main Menu")
    if page != 0:
        print("<.\tPrevious 5 items")
    if end < len(table):
        print(">.\tNext 5 items")

    option = input("Please enter an option ->")
    if len(option)==1 and option in choice:
        func = kwarg['function']
        kwarg['row'] = table[start+int(option)-1]
        kwarg['index'] = start+int(option)-1
        func(kwarg)
        return True,page
    elif option == "6":
        return True,page
    elif option == "<" and page != 0:
        return False,page-1
    elif option == ">" and end < len(table):
        return False,page+1
    else:
        print("Invalid option!")
        return False,page
            

# set up delivery
def setup_delivery():
    print("\nSetting up the new delivery...\n")
    trackNo = random.randint(1000,10000)
    cursor.execute("select trackingNo from deliveries where trackingNo = ?", (trackNo,))
    result = cursor.fetchone()
    while result:
        trackNo = random.randint(1000,10000)
        cursor.execute("select trackingNo from deliveries where trackingNo = ?", (trackNo,))
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
                cursor.execute("Insert into deliveries (trackingNo, oid, pickUpTime, dropOffTime) VALUES (?,?,?,NULL)",
                           (trackNo, o, pick_up_time))
                connection.commit()
                print("\nSuccessfully set up delivery for [ %s ] with tracking number: [" % o, trackNo, '] .\n')
            except sqlite3.Error as err: # no help :(
                print("Action Failed: " + str(err))
                print("Setup was not processed!")
                return

def update_delivery():
    trackNo = input("\nPlease enter the trackingNo [empty to cancel]: ")
    if not trackNo:
        return
    try:
        int(trackNo)
    except ValueError:
        print("\nInvalid Input!")
        return
    trackNo = int(trackNo)
    cursor.execute("select * from deliveries where trackingNo = ?", (trackNo,))
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
    global uid
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

    #path = ":memory:"
    path = "test.db"
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
