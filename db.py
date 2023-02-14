import sqlite3

#FindByStuId
def get_user_by_stuId(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM userData WHERE stuId == '{stuId}';")
    rows = cur.fetchall()
    db.close()
    if rows == []:
        return False
    else:
        return rows[0][:3]

#Update
def update_user_token(stuId:str, token:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"UPDATE userData SET token='{token}' WHERE stuId='{stuId}';")
    db.commit()
    get_user_by_stuId(stuId)
    db.close()

#checkToken
def check_token(stuId:str,token:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM userData WHERE stuId == '{stuId}';")
    rows = cur.fetchall()
    if rows[0][3] == token:
        return True
    else:
        return False



#Delete
def delete_user(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"DELETE FROM userData WHERE stuId = '{stuId}';")
    cur.execute("SELECT * FROM userData;")
    db.commit()
    db.close()
    return True

#bookData

#Create
def add_book(bookId:str, bookName:str, bookSubject:str, bookDetails:str, bookPrice:int, bookImg:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO book_data VALUES ('{bookId}', '{bookName}', '{bookSubject}', '{bookDetails}', '{bookPrice}', '{bookImg}');")
    cur.execute("SELECT * FROM book_data;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#ReadAll
def get_book():
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM bookData;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#getBookName
def get_book_name():
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute("SELECT bookId FROM bookData;")
    rows = cur.fetchall()
    db.close()
    data = []
    for i in rows:
        data.append(i[0][0:])
    return data


#orderData

#Create
def add_order(orderId:str, orderUser:str, chinese:int, math:int, programmingDesign:int, electric:int, MobileApplication:int, biology:int, digitalLogicDesignExperience:int, electricExperience:int, english:int,paid:bool):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO orderData VALUES ('{orderId}', '{orderUser}', '{chinese}', '{math}', '{programmingDesign}', '{electric}', '{MobileApplication}', '{biology}', '{digitalLogicDesignExperience}', '{electricExperience}', '{english}', '{paid}');")
    cur.execute("SELECT * FROM orderData;")
    data = f"用戶{orderUser}下了一筆訂單 編號為: {orderId} 訂購了: 國文{chinese}本\n數學{math}本\n程式設計{programmingDesign}本\n電子學{electric}本\nApp程式應用{MobileApplication}本\n生物{biology}本\n數位邏輯設計實習{digitalLogicDesignExperience}本\n電子學實習{electricExperience}本\n英文{english}本\n"
    db.commit()
    db.close()
    return data


#ReadAll
def get_order():
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM orderData;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows


#FindByOrderId
def get_order_by_orderId(orderId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM orderData WHERE orderId == '{orderId}';")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#Delete
def delete_order(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"DELETE FROM orderData WHERE orderUser = '{stuId}';")
    cur.execute("SELECT * FROM orderData;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#FindByStuId
def get_order_by_stuId(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    # cur.execute(f"SELECT * FROM orderData WHERE orderUser == '{stuId}';")
    if stuId == "":
        cur.execute(f"SELECT userData.name,orderData.* FROM orderData , userData WHERE userData.stuId = orderData.orderUser;")
    else:
        cur.execute(f"SELECT userData.name,orderData.* FROM orderData , userData WHERE userData.stuId = orderData.orderUser AND orderData.orderUser ='{stuId}';")

    rows = cur.fetchall()
    name = get_user_by_stuId(stuId)
    db.close()
    return rows

#UpdatePaidStatus
def update_paid_status(orderUser:str, paid:bool):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"UPDATE orderData SET paid = '{paid}' WHERE orderUser = '{orderUser}';")
    cur.execute("SELECT * FROM orderData;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#GetPaidStatus
def get_paid_status(orderUser:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT paid FROM orderData WHERE orderUser = '{orderUser}';")
    rows = cur.fetchall()
    db.commit()
    db.close()
    try:
        if rows[0][0] == "True" or "False":
            return rows[0][0]
        else:
            return None
    except:
        pass
    




#UserData

#Create
def add_user(stuId:str, name:str, role:str, token:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO userData VALUES ('{stuId}', '{name}', '{role}', '{token}');")
    cur.execute("SELECT * FROM userData;")
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows

#ReadAll
def get_user():
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM userData;")
    rows = cur.fetchall()
    db.close()
    return rows



#cadresData

#RealByStuId
def get_cadres_by_stuId(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM cadresData WHERE stuId == '{stuId}';")
    rows = cur.fetchall()
    role = ""
    if rows == []:
        role = "學生"
    else:
        role = rows[0][1]
    db.close()
    return role
#checkCadres
def check_cadres(stuId:str):
    db = sqlite3.connect('static/data/data.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM cadresData WHERE stuId == '{stuId}';")
    rows = cur.fetchall()
    db.close()
    if rows == []:
        return False
    else:
        return True

print(check_cadres("s1111032015"))

#Else

