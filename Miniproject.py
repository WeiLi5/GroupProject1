import sqlite3
import datetime
import hashlib
import os.path
import getpass
import random
import sys


connection = None
cursor = None
is_login = False
is_end = False
user_type = None
user_id = None
basket = []


class Item:
    def __init__(self, store_name, store_id, product_name, product_id, unit, price, qty):
        self.store_name = store_name
        self.store_id = store_id
        self.product_name = product_name
        self.product_id = product_id
        self.unit = unit
        self.qty = qty
        self.price = price

    def set_qty(self, qty):
        self.qty = qty

    def get_tuple(self):
        return self.product_name, self.product_id, self.store_name, self.store_id, self.unit, self.price, self.qty

    def __eq__(self, other):
        return self.store_id == other.store_id and self.product_id == other.product_id


# Create hash function in here
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.create_function("hash", 1, encrypt)
    connection.commit()
    return


# Initialize table
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


# For hash function
def encrypt(password):
    alg = hashlib.sha256()
    password = password.encode('UTF-8')
    alg.update(password)
    return alg.hexdigest()


# Initialize testing data
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
                                (4, 'Save-on-food','7804004000', '9743 60Ave'),
                                (5, 'safeway', '7804336930', '10930 82 Ave NW'),
                                (6, 'Sobeys', '7804385064', '8225 112 St NW'),
                                (7, 'Liquor store', '7804331814', '11148 82 AVe'),
                                (8, 'IKEA', '8666664532', '1311 102 St NW');
                       '''

    insert_category = '''
                        INSERT INTO categories(cat, name) VALUES
                                ('fru', 'fruit'),
                                ('dai', 'daily'),
                                ('dri', 'drink'),
                                ('ach', 'alcohol'),
                                ('veg', 'vegetable'),
                                ('fur', 'furniture'),
                                ('kit', 'kitchen');
                        '''

    insert_product = '''
                        INSERT INTO products(pid, name, unit, cat) VALUES
                                ('000001', 'milk', 'bottle', 'dri'),
                                ('000002', 'icetea', 'bottle', 'dri'),
                                ('000003', 'coke', 'bottle', 'dri'),
                                ('100001', 'potato', 'lb', 'veg'),
                                ('100002', 'broccoli', 'lb', 'veg'),
                                ('200001', 'apple', 'lb', 'fru'),
                                ('200002', 'banana', 'lb', 'fru'),
                                ('300001', 'tissue', 'pack', 'dai'),
                                ('400001', 'vodka', 'bottle', 'ach'),
                                ('400002', 'brandy', 'bottle', 'ach'),
                                ('500001', 'sofa', 'piece', 'fur'),
                                ('500002', 'headboard', 'piece', 'fur'),
                                ('500003', 'table', 'piece', 'fur'),
                                ('500004', 'chair', 'piece', 'fur'),
                                ('600001', 'knife', 'piece', 'kit'),
                                ('600002', 'chopsticks', 'set', 'kit'),
                                ('600003', 'crisper', 'piece','kit'),
                                ('600004', 'mug', 'piece', 'kit');

                        '''

    insert_oline = '''
                        INSERT INTO olines(oid, sid, pid, qty, uprice) VALUES
                                (101, 1, '000001', 3, 0.1),
                                (102, 4, '000002', 5, 0.2),
                                (103, 2, '000003', 2, 0.3),
                                (104, 5, '100001', 1, 1.1),
                                (105, 5, '100002', 8, 1.2),
                                (106, 5, '100002', 9, 1.2),
                                (107, 5, '200001', 4, 2.1),
                                (201, 4, '200002', 3, 2.3),
                                (202, 6, '300001', 5, 3.0),
                                (203, 7, '400001', 2, 4.1),
                                (204, 7, '400002', 1, 4.2),
                                (205, 8, '500001', 8, 5.1),
                                (206, 8, '500002', 9, 5.2),
                                (301, 8, '600001', 3, 6.1),
                                (302, 8, '600003', 5, 6.3),
                                (401, 8, '600004', 2, 6.4);
                        '''

    insert_order = '''
                        INSERT INTO orders(oid, cid, odate, address) VALUES
                                (101, 'sss', '2015-06-27', '10239 Jasper Ave'),
                                (102, 'sss', '2016-10-21', '12123 123 st'),
                                (103, 'sss', '2017-07-06', '10239 Jasper Ave'),
                                (104, 'sss', '2017-07-08', '10239 Jasper Ave'),
                                (105, 'sss', '2017-09-27', '10239 Jasper Ave'),
                                (106, 'sss', '2017-10-27', '10239 Jasper Ave'),
                                (107, 'sss', '2017-10-30', '10239 Jasper Ave'),
                                (201, 'www', '2017-10-27', '9910 107 st'),
                                (202, 'www', '2017-10-28', '9910 107 st'),
                                (203, 'www', '2017-10-29', '9910 107 st'),
                                (204, 'www', '2017-10-30', '9910 107 st'),
                                (205, 'www', '2017-10-31', '9910 107 st'),
                                (206, 'www', '2017-11-01', '9910 107 st'),
                                (301, 'uuu', '2017-01-13', '10390 Whyte Ave'),
                                (302, 'uuu', '2017-02-27', '10390 Whyte Ave'),
                                (401, 'zzz', '2017-10-28', '8920 97 AVe');
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
                                (1, '000001', 10, 0.1),
                                (2, '000001', 11, 0.2),
                                (3, '000001', 12, 0.3),
                                (4, '000001', 13, 0.4),
                                (5, '000001', 14, 0.2),
                                (6, '000001', 15, 0.2),
                                (8, '000001', 16, 0.3),
                                (4, '000002', 9, 0.2),
                                (5, '000002', 22, 0.3),
                                (6, '000002', 14, 0.2),
                                (1, '000003', 11, 0.3),
                                (2, '000003', 12, 0.4),
                                (3, '000003', 13, 0.3),
                                (4, '000003', 14, 0.6),
                                (5, '000003', 15, 0.4),
                                (6, '000003', 6, 0.4),
                                (7, '000003', 1, 0.5),
                                (8, '000003', 9, 0.3),
                                (4, '100001', 28, 1.1),
                                (5, '100001', 12, 1.0),
                                (6, '100001', 7, 1.2),
                                (4, '100002', 31, 1.2),
                                (5, '100002', 12, 1.2),
                                (6, '100002', 13, 1.2),
                                (4, '200001', 4, 2.1),
                                (5, '200001', 3, 3.1),
                                (6, '200001', 11, 2.5),
                                (4, '200002', 5, 2.3),
                                (5, '200002', 1, 2.4),
                                (6, '200002', 7, 2.3),
                                (4, '300001', 8, 2.7),
                                (5, '300001', 7, 3.0),
                                (6, '300001', 15, 2.9),
                                (7, '400001', 10, 4.1),
                                (7, '400002', 11, 4.2),
                                (8, '500001', 12, 5.1),
                                (8, '500002', 2, 5.2),
                                (8, '600001', 2, 6.1),
                                (8, '600003', 1, 6.3),
                                (8, '600004', 7, 6.4);
                        '''

    insert_delivery = '''
                        INSERT INTO deliveries(trackingNo, oid, pickUpTime, dropOffTime) VALUES
                                (1001, 101, '2015-06-28', '2015-07-08'),
                                (1002, 102, '2016-10-22', '2016-10-31'),
                                (1003, 103, '2017-07-09', '2017-07-17'),
                                (1003, 104, '2017-07-09', '2017-07-17'),
                                (1005, 105, '2017-10-01', '2017-10-02'),
                                (1006, 106, '2017-10-29', '2017-10-31'),
                                (1007, 107, '2017-10-31', '2017-11-01'),
                                (2001, 201, '2017-10-29', '2017-11-01'),
                                (2001, 202, '2017-10-29', '2017-11-01'),
                                (2003, 203, '2017-11-01', NULL),
                                (2003, 204, '2017-11-01', NULl),
                                (2003, 205, '2017-11-01', NULL),
                                (2003, 206, '2017-11-01', NULL),
                                (3001, 301, '2017-01-14', '2017-01-16'),
                                (3002, 302, '2017-02-28', '2017-03-04'),
                                (4001, 401, '2017-10-29', '2017-10-31');
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


# place an order
# the stock will be updated when customer place an order
def place_order():
    global basket, cursor
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
            data = (sid, pid)
            cursor.execute(query, data)
            result = cursor.fetchall()
            stock = result[0][0]
            if not len(result):
                print("The store no longer carries this product!")
                return
            if stock < qty:
                print("The quantity for product(%s) in store(%s) is:\t%d" % (row[0], row[2], stock))
                print("The quantity for this product and this store in your basket is:\t%d" % qty)
                print("Please change your quantity")
                modify_item({'index': i})
                # qty = item.get_tuple()[-1] # assigned at while loop below
                all_checked = False
                break
        if all_checked:
            # generate unique id
            cursor.execute("select ifnull(max(oid),0) from orders")  # # if null ?
            oid = cursor.fetchone()[0] + 1
            print("\nYour order [%i] has been placed\n" % oid)
            # get user address
            cursor.execute("select address from customers where cid = ?", (user_id,))
            address = cursor.fetchone()[0]

            # insert into order
            cursor.execute("Insert into orders (oid, cid, odate, address) VALUES (?,?,date('now'),?)", (oid, user_id, address))
            connection.commit()

            while len(basket):
                item = basket.pop()
                row = item.get_tuple()
                pid = row[1]
                sid = row[3]
                qty = row[-1]
                uprice = row[-2]

                # insert into olines
                cursor.execute("Insert into olines (oid, sid, pid, qty, uprice) VALUES (?,?,?,?,?)", (oid, sid, pid, qty, uprice))

                # update stock
                cursor.execute("UPDATE carries set qty=? where sid=? AND pid=?", (stock - qty, sid, pid))

            connection.commit()
            break


# list orders
def list_orders():
    query = '''
    select o.oid, o.odate, count(*), ROUND(sum(l.qty*l.uprice),2)
    from orders o, olines l
    where   o.cid =? and
            o.oid = l.oid
    group by o.oid
    order by o.odate DESC
        '''
    data = (user_id,)
    cursor.execute(query, data)
    result = cursor.fetchall()
    cols = ["Order ID", "   Order date   ", "#Products", "Total Price "]

    end = False
    page = 0
    while not end:
        print("*** Select an order to see more details ***")
        end, page = table_menu(result, cols, page, {'function':order_detail})


# check the details of an order
def order_detail(kwarg):
    oid = kwarg['row'][0]

    # Info of orders
    query = '''
        select d.trackingNo, d.pickUpTime, d.dropOffTime,o.address
        from deliveries d, orders o
        where  o.oid = ? AND o.oid = d.oid;
    '''
    data = (oid,)
    cursor.execute(query, data)
    orderInfo = cursor.fetchall()
    info = ""

    if not len(orderInfo):
        info += "Status: Not delivery yet"
    else:
        orderInfo = orderInfo[0]
        info += "Tracking#:\t{}\nPickupTime:\t{}\nDropOffTime:\t{}\nAddress:\t{}\n"
        info = info.format(orderInfo[0], orderInfo[1], orderInfo[2], orderInfo[3])

    query='''
    select s.sid, s.name, p.pid, p.name, l.qty, p.unit, l.uprice
    from stores s, products p, olines l, orders o
    where   o.oid= ? and
            o.oid =l.oid and
            l.sid=s.sid and
            l.pid=p.pid
    '''

    data = (oid,)
    cursor.execute(query, data)
    prodInfo = cursor.fetchall()
    cols = ['StoreID', '    Store Name    ', 'ProductID', '    Product Name    ', 'Quantity', '  Unit  ', 'Price']
    end = False
    page = 0
    while not end:
        print(info)
        end, page = table_menu(prodInfo, cols, page, {'function': None})


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
        global is_login, basket
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


# check the basket
def modify_basket():
    cols = ["Product Name", "Product ID", "    Store Name    ", "Store ID", "  Unit  ", "Price", "Quantity"]
    end = False
    page = 0
    result = []
    for item in basket:
        result.append(item.get_tuple())
    while not end:
        print("*** Select item to modify qty, set to 0 to delete it! ***")
        end, page = table_menu(result, cols, page, {'function': modify_item})


# change the quantity of the products
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
        except ValueError:
            print("\nInvalid Input!")
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
    on r1.pid = r4.pid

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
        end, page = table_menu(result, ["Product ID", "    Name    ", "  Unit  ", "#Stores", "Min Price", "#Stores On Stock",
                                        "Min Price On Stock", "#Orders Within 7 days"], page, {'function': product_detail})


# check the detail of products
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

    data = (pid, pid)
    cursor.execute(query, data)
    result = cursor.fetchall()
    cols = ["Store ID", "   Store Name   ", " Store Contact ", "    Store Address    ", "Price", "Quantity",
            "# of orders within 7 days"]

    query = '''
    select * from products where pid = ?
    '''
    data = (pid,)
    cursor.execute(query,data)
    info = cursor.fetchone()

    query = '''select name from categories where cat = ?'''
    data = (info[3],)
    cursor.execute(query, data)
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
        end, page = table_menu(result, cols, page, {'function': add_basket, 'product': kwarg['row']})


# customer can add products into their basket
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
        except ValueError:
            print("\nInvalid Input!")
        else:
            break
    if qty > 0:
        item = Item(sname, sid, pname, pid, unit, price, qty)
        if item in basket:
            basket[basket.index(item)].qty += qty
        else:
            basket.append(item)


# this part is for table menu,
# which is related to showing 5 items
# and choose next page or last page
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
    end = min(page*5+5, len(table))
    choice = ""
    for i in range(start, end):
        content = str(i-start+1)
        row_string = "|{}{}|".format(content, (length[0]-len(content))*" ")
        row = table[i]
        for j in range(len(row)):
            content = str(row[j])
            row_string += "{}{}|".format(content, (length[j+1]-len(content))*" ")
        print(row_string)
        print(spliter)
        choice += str(i-start+1)
    print("6.\tBack to Main Menu")
    if page != 0:
        print("<.\tPrevious 5 items")
    if end < len(table):
        print(">.\tNext 5 items")

    option = input("Please enter an option ->")
    if len(option) == 1 and option in choice:
        func = kwarg['function']
        if not func:
            print("Invalid option!")
            return False, page
        else:
            kwarg['row'] = table[start+int(option)-1]
            kwarg['index'] = start+int(option)-1
            func(kwarg)
            return True, page
    elif option == "6":
        return True, page
    elif option == "<" and page != 0:
        return False, page-1
    elif option == ">" and end < len(table):
        return False, page+1
    else:
        print("Invalid option!")
        return False, page


# set up delivery
def setup_delivery():
    print("\nSetting up the new delivery...\n")
    trackNo = random.randint(1000, 10000)
    cursor.execute("select trackingNo from deliveries where trackingNo = ?", (trackNo,))
    result = cursor.fetchone()
    while result:
        trackNo = random.randint(1000, 10000)
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
            except sqlite3.Error as err:  # no help :(
                print("Action Failed: " + str(err))
                print("Setup was not processed!")
                return


# update the delivery including PickUpTime, DropOffTime and removal of the order
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
    print("-"*48)
    print('|Index |TrackingNo|Order|PickUpTime|DropOffTime| ')
    for entry in result:
        index += 1
        print("|%i.    |" % index + "%-10i" % entry[0] + '|' + "%-5s" % str(entry[1]) + '|' + "%-10s" % str(entry[2])+'|'
              + "%-11s" % str(entry[3])+'|')
    print("-"*48+'\n')
    while True:
        choice = input("Select an order to modify -> ")
        try:
            if int(choice) > index or int(choice) <= 0:
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
                cursor.execute("delete from deliveries where oid = ? and trackingNo = ?", (oid, trackNo,))
                connection.commit()
                print("\nOrder %i has been removed from deliveries!\n" % oid)
                return
            else:
                print("\nAction has been aborted!")
        elif action == '4':
            return
        else:
            print("\nInvalid Input!\n")


# add stock and new products
def add_stock():
    query = "SELECT sid,c.pid,name,qty,uprice FROM carries c, products p WHERE c.pid = p.pid"
    cursor.execute(query)
    result = cursor.fetchall()
    print("*** Select a store and a product to add stock ***")
    line = "-" * 54
    print(line)
    print("|Store ID|Product ID|    Name    |Quantity|Unit price|")
    print(line)
    for item in result:
        print("|" + "%-8s" % item[0] + "|" + "%-10s" % item[1] +
              "|" + "%-12s" % item[2] + "|" + "%-8s" % item[3] +
              "|" + "%-10s" % item[4] + "|")
        print(line)
    instruction = "\n" + "-" * 20 + "\n"
    instruction += "1.\tAdd to stock\n"
    instruction += "2.\tChange the unit price\n"
    instruction += "3.\tAdd new product into store\n"
    instruction += "4.\tAdd new product information\n"
    instruction += "-" * 20

    print(instruction)
    option = input("Please enter an option ->")
    if option == '1':
        sid = input("Enter store id : ")
        pid = input("Enter product id: ")
        cursor.execute("select sid, pid from carries where sid = ? and pid = ? ", (sid, pid,))
        result = cursor.fetchone()
        if not result:
            print("The store or product you entered not exists.")
            return
        qty = input("Enter the number of products to be added to the stock: ")
        try:
            int(qty)
        except ValueError:
            print("Input qty is not valid.")
            return
        if int(qty) <= 0:
            print("qty must be positive.")
            return
        change_qty = "UPDATE carries SET qty = qty + " + qty
        change_qty += " WHERE sid=" + sid + " and pid=?;"
        cursor.execute(change_qty, (pid,))
        connection.commit()
    elif option == '2':
        sid = input("Enter store id : ")
        pid = input("Enter product id: ")
        cursor.execute("select sid, pid from carries where sid = ? and pid = ? ", (sid, pid,))
        result = cursor.fetchone()
        if not result:
            print("The store or product you entered not exists.")
            return
        uprice = input("Enter the unit price: ")
        try:
            float(uprice)
        except ValueError:
            print("Input price is not valid.")
            return
        change_price = "UPDATE carries SET uprice =" + uprice
        change_price += " WHERE sid=" + sid + " and pid=?"
        cursor.execute(change_price, (pid,))
        connection.commit()
    elif option == '3':
        sid = input("Enter store id: ")
        pid = input("Enter product id: ")
        qty = input("Enter quantity of the product: ")
        uprice = input("Enter unit price: ")
        try:
            int(qty) and float(uprice)
        except ValueError:
            print("Input qty or price is not valid.")
            return
        if int(qty) <= 0:
            print("qty must be positive.")
            return
        query = "SELECT sid, pid FROM carries WHERE sid=" + sid + " and pid =" + pid
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            add_product = "INSERT INTO carries(sid, pid, qty, uprice)"
            add_product += " VALUES (" + sid + ", '" + pid + "', " + qty + ", " + uprice + ");"
            try:
                cursor.execute(add_product)
            except sqlite3.IntegrityError:
                print("The store or product you entered not exists.")
                print("Want to create a new product? Choose add new product information instead.\n")
                return
            connection.commit()
        else:
            print("\nThis product already exists in this store, please choose ADD TO STOCK.")
    elif option == '4':
        pid = input("Enter product id: ")
        query = "SELECT pid FROM products WHERE pid=" + pid
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            name = input("Enter product name: ")
            unit = input("Enter unit name: ")
            print("*** Select a category ***")
            query = "SELECT * FROM categories"
            cursor.execute(query)
            result = cursor.fetchall()
            line = "-" * 18
            print(line)
            print("|Abb|  Category  |")
            print(line)
            for item in result:
                print("|" + "%-3s" % item[0] + "|" + "%-12s" % item[1] + "|")
                print(line)
            cat = input("Enter the categories (3 characters abbreviation): ")
            new_product = "INSERT INTO products(pid, name, unit, cat)"
            new_product += " VALUES (" + "?" + ",'" + name + "', '" + unit + "','" + cat + "');"
            try:
                cursor.execute(new_product, (pid,))
            except sqlite3.IntegrityError:
                print("The category your entered not exists.")
                return
            connection.commit()
        else:
            print("\nInformation of this product already exists.")
    else:
        print("\nInvalid option!")


def check_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# new customer register
def signup():
    uid = input("Customer ID: ")
    while not uid:
        print("\n****Customer ID cannot be empty! **** ")
        uid = input("Customer ID: ")
    name = input("Customer Name: ")
    address = input("Address: ")
    while not address:
        print("\n***Please enter a address for delivery!***")
        address = input("Address: ")
    password = getpass.getpass()
    while not password:
        print("\n***Please enter a password!***")
        password = getpass.getpass()
    data = (uid, name, address, password)
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

    if len(sys.argv) == 1:
        print("-> No path is given, using memory instead!")
        path = ':memory:'
    else:
        path = sys.argv[1]

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
