import requests
import http.cookiejar as cookielib
import re
import json

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookie.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('Cookie cannot be loaded!')

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}

def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match(".*name='_xsrf' value='(.*?)'", response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open('index_page.html', 'wb') as f:
        f.write(response.text.encode('utf-8'))
    print('ok')

def is_login():
    inbox_url = 'https://www.zhihu.com/inbox'
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={}&type=login&lang=cn".format(t)
    t = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(t.content)
        f.close()
    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = eval(input("input captcha\n>"))
    return captcha

def zhihu_login(account, password):
    if re.match('\d{10}', account):
        print("Cellphone login")
        # captcha = get_captcha()
        # captcha_dict = {"img_size": [200, 44], "input_points": []}
        # for x in captcha:
        #     captcha_dict['input_points'].append(x)
        # print(captcha_dict)
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha(),
            'captcha_type': 'cn'
        }

        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()
        print(response_text.text)
        print(response_text.status_code)

zhihu_login('6472159987', 'dsh20462046')

