from flask import Flask, redirect, render_template, request
import requests


SECRET = 'AzIgdi8l7n7PlpThoeVo'
ACCESS_TOKEN = ''
USER_ID = ''
METHOD = "https://api.vk.com/method/{}&access_token={}&v=5.95"

app = Flask(__name__)


@app.route('/')
def index():
    global USER_ID
    global ACCESS_TOKEN
    if USER_ID:
        method = "users.get?user_ids={}".format(USER_ID)
        req = METHOD.format(method, ACCESS_TOKEN)
        request_vk = requests.get(req)
        dic = request_vk.json()
        dic = dic['response']
        return render_template('main_1.html', user=dic[0])
    else:
        return render_template('main_0.html', user_id=USER_ID)


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath


@app.route('/user/<int:user_id>')
def vk_access(user_id):
    global ACCESS_TOKEN
    global METHOD
    method = "friends.get?user_id={}&count=5&order=random&fields=nickname".format(user_id)
    req = METHOD.format(method, ACCESS_TOKEN)
    request_vk = requests.get(req)
    dic = request_vk.json()
    dic = dic['response']['items']

    method = "users.get?user_ids={}".format(USER_ID)
    req = METHOD.format(method, ACCESS_TOKEN)
    request_vk = requests.get(req)
    dic_user = request_vk.json()
    dic_user = dic_user['response']
    return render_template("page.html", user=dic, login_user=dic_user[0])


@app.route('/vk_auth', methods=['POST', 'GET'])
def vk_auth():
    global USER_ID
    global ACCESS_TOKEN

    code = request.args.get('code')
    l = "https://oauth.vk.com/access_token?client_id=6952806&client_secret={}&redirect_uri=http://127.0.0.1:5000/vk_auth&code={}".format(SECRET, code)
    req = requests.get(l)
    dic = req.json()
    ACCESS_TOKEN = dic['access_token']
    USER_ID = dic['user_id']
    l2 = "https://api.vk.com/method/friends.get?user_id={}&count=5&order=random&access_token={}&v=5.95".format(USER_ID, ACCESS_TOKEN)
    req = requests.get(l2)
    dic = req.json()

    return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        return redirect("https://oauth.vk.com/authorize?client_id=6952806&display=page&redirect_uri=http://127.0.0.1:5000/vk_auth&response_type=code&v=5.95")

    return render_template('login.html', error=error)
