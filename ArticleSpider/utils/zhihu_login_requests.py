import requests
import http.cookiejar as cookielib
import re

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}

def get_xsrf():
    response = requests.get("https://www.zhihu.com", headers=header)
    print(response.text)
    return ""


def zhihu_login(account, password):
    if re.match('\d{10}', account):
        print("Cellphone login")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }

get_xsrf()