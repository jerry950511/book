from flask import Flask, render_template, request, redirect, url_for, flash , jsonify , make_response , session, Response
import json,uuid, time
import eportal
from db import *
app = Flask(__name__, static_folder='static/assets')

        

@app.route('/')
def index_page():
    return redirect(url_for("page", pageName="home")) #預設導向 /home

def eachPageLogin(stuId, token, route):
    resp = make_response(render_template(str(route)))
    if get_user_by_stuId(stuId): # 檢查資料庫是否有此用戶資料
        if check_token(stuId,token): # 檢查token是否正確
            return resp
        else:
            resp.set_cookie('token', '', expires=0)
            resp.set_cookie('stuId', '', expires=0)
            return resp
    else:
        resp.set_cookie('token', '', expires=0)
        resp.set_cookie('stuId', '', expires=0)
        return resp

@app.route('/<pageName>') #各大頁面 home news ...
def page(pageName):
    stuId = request.cookies.get('stuId')
    token = request.cookies.get('token')

    if stuId != None and token != None:
        if pageName == "home": # 訂書網首頁
            return eachPageLogin(stuId,token,"index.html")
        elif pageName == "order": # 訂書頁面
            return eachPageLogin(stuId,token,"order.html")
        elif pageName == "signup": # 註冊頁面
            return eachPageLogin(stuId,token,"signup.html")
        elif pageName == "redirect": # 重新導向頁面
            return eachPageLogin(stuId,token,"redirect.html")
        elif pageName == "query": # 訂書頁面
            return eachPageLogin(stuId,token,"query.html")
        elif pageName == "account": # 訂書頁面
            return eachPageLogin(stuId,token,"account.html")
        elif pageName == "terms-of-use": # 使用條款
            return eachPageLogin(stuId,token,"terms-of-use.html")
        elif pageName == "privacy-policy": # 隱私政策
            return eachPageLogin(stuId,token,"privacy-policy.html")
        elif pageName == "legal-notice": # 官方布告
            return eachPageLogin(stuId,token,"legal-notice.html")
        elif pageName == "edit": # 編輯訂單
            return eachPageLogin(stuId,token,"editOrder.html")
        elif pageName == "loginError": #登入失敗
            return eachPageLogin(stuId,token,"loginError.html")
        elif pageName == "logout": #登入成功
            resp = make_response(redirect("/"))
            resp.set_cookie('token', '', expires=0)
            resp.set_cookie('stuId', '', expires=0)
            return resp
        else: # 查無此頁面
            return eachPageLogin(stuId,token,"404.html")

    else:
        if pageName == "home": # 訂書網首頁
            return render_template("index.html")
        elif pageName == "order": # 訂書頁面
            return render_template("order.html")
        elif pageName == "signin": # 登入頁面
            return render_template("signin.html")
        elif pageName == "signup": # 註冊頁面
            return render_template("signup.html")
        elif pageName == "redirect": # 重新導向頁面
            return render_template("redirect.html")
        elif pageName == "query": # 訂書頁面
            return render_template("query.html")
        elif pageName == "account": # 訂書頁面
            return render_template("account.html")
        elif pageName == "terms-of-use": # 使用條款
            return render_template("terms-of-use.html")
        elif pageName == "privacy-policy": # 隱私政策
            return render_template("privacy-policy.html")
        elif pageName == "legal-notice": # 官方布告
            return render_template("legal-notice.html")
        elif pageName == "edit": # 編輯訂單
            return render_template("editOrder.html")
        elif pageName == "loginError": #登入失敗
            return render_template("redirect.html")
        elif pageName == "logout": #登入成功
            resp = make_response(redirect("/"))
            resp.set_cookie('token', '', expires=0)
            resp.set_cookie('stuId', '', expires=0)
            return resp
        else: # 查無此頁面
            return render_template("404.html")

    

@app.route("/signin", methods=['GET']) # 登入頁面
def signin():
    stuId = request.cookies.get('stuId') # 從cookie取得stuId
    token = request.cookies.get('token') # 從cookie取得token
    resp = make_response(render_template("signin.html"))
    if (stuId == None) and (token == None): # 檢查cookie是否存在
        return render_template("signin.html") # 不存在 => 顯示登入頁面
    else: # cookies存在
        if get_user_by_stuId(stuId): # 檢查資料庫是否有此用戶資料
            if check_token(stuId,token): # 檢查token是否正確
                return redirect("/") # 正確 => 重新導向首頁
            else: # token不正確 => 顯示登入頁面 並清除cookie
                resp.set_cookie('token', '', expires=0)
                resp.set_cookie('stuId', '', expires=0)
                return resp
        else: # 資料庫沒有此用戶資料 => 顯示登入頁面 並清除cookie
            resp.set_cookie('token', '', expires=0)
            resp.set_cookie('stuId', '', expires=0)
            return resp



@app.route("/auth", methods=['POST']) # eportal 登入
def eportal_login():
    account = request.form['account']
    password = request.form['password']
    login = eportal.login(account, password)

    if login.get_info()["status"] == "success": # 檢查帳號密碼是否正確
        role = get_cadres_by_stuId(login.get_info()["stId"]) # 檢查是否為幹部
        info = login.get_info() # 取得學生資料
        stuId = info["stId"] # 學號
        info["role"] = role # 身分
        token = "token-"+str(uuid.uuid4()) # 產生token
        if get_user_by_stuId(stuId):
            update_user_token(stuId,token)
        else:
            add_user(stuId,info["stName"],role,token) # 將資料加入資料庫
        resp = make_response(redirect("/")) #  導向到首頁
        resp.set_cookie('stuId', f'{stuId}', max_age=60*60*24) #把stuId加到cookie 並設定過期時間為一天
        resp.set_cookie('token', f'{token}', max_age=60*60*24) #把token加到cookie 並設定過期時間為一天
        return resp
    else:
        return redirect("/loginError") # redirect /loginError


@app.route("/api/get_user_info", methods=['GET'])
def get_user_info():
    stuId = request.cookies.get('stuId')
    token = request.cookies.get('token')
    if check_token(stuId,token):
        return jsonify({"status":"success","data":get_user_by_stuId(stuId)})
    else:
        return jsonify({"status":"error","data":"token error"})


@app.route("/api/order", methods=['GET','POST'])
def get_order():
    #學生確定訂單
    if request.method == 'POST':
        pass
    #幹部查詢訂單
    elif request.method == 'GET':
        getAllOrder = get_order()
        return jsonify({"data":getAllOrder})


@app.route("/api/get_book_info", methods=['GET'])
def get_book_info():
    return get_book()

@app.route("/place_order", methods=['POST'])
def place_order():
    orderId = "order-"+str(uuid.uuid4())
    stuId = request.cookies.get('stuId')
    token = request.cookies.get('token')
    chinese = request.form.get('programmingDesign')
    math = request.form.get('electric')
    programmingDesign = request.form.get('math')
    electric = request.form.get('mobileApplication')
    mobileApplication = request.form.get('biology')
    biology = request.form.get('digitalLogicDesignExperience')
    digitalLogicDesignExperience = request.form.get('electricExperience')
    electricExperience = request.form.get('english')
    english = request.form.get('chinese')

    if stuId != None and token != None:
        if check_token(stuId,token):
            if get_paid_status(stuId) == "True":
                return jsonify({"status":"error","message":"已付款"})
            else:
                pass
            delete_order(stuId)
            data = add_order(orderId,stuId,chinese,math,programmingDesign,electric,mobileApplication,biology,digitalLogicDesignExperience,electricExperience,english,False)
            return jsonify({"data":data , "status":"success"})
        else:
            return jsonify({"status":"error","message":"token error"})
    else:
        return jsonify({"status":"error","message":"no cookie"})

@app.route("/api/get_order_by_stuId", methods=['GET'])
def get_order_stuid():
    stuId = request.cookies.get('stuId')
    token = request.cookies.get('token')
    if stuId != None and token != None:
        if check_token(stuId,token):
            return jsonify({"data":get_order_by_stuId("") , "status":"success" , "bookName":get_book()})
        else:
            return jsonify({"data":get_order_by_stuId("") , "status":"success" , "bookName":get_book()})
    else:
        return jsonify({"data":get_order_by_stuId("") , "status":"success" , "bookName":get_book()})

@app.route("/api/update_paid_status", methods=['POST'])
def update_status_of_paid():
    orderUser = request.form.get('orderUser')
    stuId = request.cookies.get('stuId')
    token = request.cookies.get('token')
    if stuId != None and token != None:
        if check_token(stuId,token):
            if check_cadres(stuId):
                return jsonify({"data":update_paid_status(orderUser,True) , "status":"success"})
            else:
                return jsonify({"status":"error","message":"not cadres"})
        else:
            return jsonify({"status":"error","message":"token error"})
    else:
        return jsonify({"status":"error","message":"no cookie"})

@app.route("/api/get_paid_status", methods=['GET'])
def get_status_of_paid():
    orderUser = request.form.get('orderUser')
    return jsonify(get_paid_status(orderUser))

#run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
