from urllib.parse import urlencode
import requests
import os

from flask import Flask, redirect, render_template, request


SECRET = os.environ['SECRET']

ACCESS_TOKEN = ''
USER_ID = ''
CLIENT_ID = os.environ['CLIENT_ID']
URL_GET_CODE = f"https://oauth.vk.com/authorize?{{}}"
URL_GET_ACCESS_TOKEN = f"https://oauth.vk.com/access_token?{{}}"
METHOD = "https://api.vk.com/method/{}&access_token={}&v=5.95"
METHOD_USERS_GET = f"https://api.vk.com/method/users.get?{{}}"
METHOD_FRIENDS_GET = f"https://api.vk.com/method/friends.get?{{}}"
REDIRECT_URI = r'http://127.0.0.1:5000/vk_auth'


app = Flask(__name__)


@app.route('/')
def index():
    if USER_ID:
        params = {
            'user_ids': USER_ID,
            'access_token': ACCESS_TOKEN,
            'v': '5.95',
        }
        url = METHOD_USERS_GET.format(urlencode(params))
        request_vk = requests.get(url)
        result = request_vk.json()
        result = result['response']
        return render_template('main_1.html', user=result[0])
    else:
        return render_template('main_0.html')


@app.route('/user/<int:user_id>')
def vk_access(user_id):
    params = {
        'user_id': user_id,
        'count': '5',
        'order': 'random',
        'fields': 'nickname',
        'access_token': ACCESS_TOKEN,
        'v': '5.95',
    }
    url = METHOD_FRIENDS_GET.format(urlencode(params))

    request_vk = requests.get(url)
    result = request_vk.json()
    result = result['response']['items']

    params_user = {
        'user_ids': USER_ID,
        'access_token': ACCESS_TOKEN,
        'v': '5.95',
    }
    url_user = METHOD_USERS_GET.format(urlencode(params_user))
    request_vk_user = requests.get(url_user)
    result_user = request_vk_user.json()
    result_user = result_user['response']
    return render_template("page.html", user=result, login_user=result_user[0])


@app.route('/vk_auth', methods=['POST', 'GET'])
def vk_auth():
    global USER_ID
    global ACCESS_TOKEN
    code = request.args.get('code')
    params = {
        'client_id': CLIENT_ID,
        'client_secret': SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,

    }

    url = URL_GET_ACCESS_TOKEN.format(urlencode(params))
    request_vk = requests.get(url)
    result = request_vk.json()
    ACCESS_TOKEN = result['access_token']
    USER_ID = result['user_id']

    return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        params = {
            'client_id': CLIENT_ID,
            'display': 'page',
            'redirect_uri': REDIRECT_URI,
            'response_type': 'code',
            'v': '5.95',
        }
        url = URL_GET_CODE.format(urlencode(params))
        return redirect(url)

    return render_template('login.html', error=error)
