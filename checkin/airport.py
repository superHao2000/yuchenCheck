import json

import requests
import urllib3

from utils.config import Conf
from utils.logger import log
from utils.util import sleep_random

urllib3.disable_warnings()

config_AirPort = Conf.Account["AirPort"]
name = "飞机场"


class AirPort(object):
    def __init__(self, account):
        self.base_url = account["base_url"]
        self.email = account["email"]
        self.password = account["password"]

    def checkin(self):
        """
        主程序：实现登录和签到操作
        :return:
        """
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        session = requests.session()
        # 获取主页面
        session.get(self.base_url, verify=False)
        # 登录
        login_url = self.base_url + '/auth/login'
        headers = {
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        login_data = {
            'email': self.email,
            'passwd': self.password,
            'code': ''
        }
        session.post(url=login_url, headers=headers, data=login_data, verify=False)
        # 签到
        check_url = self.base_url + '/user/checkin'
        headers = {
            'User-Agent': user_agent,
            'Referer': self.base_url + '/user',
        }
        response = session.post(url=check_url, headers=headers, verify=False)
        response = json.loads(response.text)
        log.info(response["msg"])


def exam_account(account):
    if account['base_url'] == "" or account['email'] == "" or account['password'] == "":
        log.info("账号信息不完整,跳过此账号")
        return False

    return True


def main():
    log.info(f"{name}签到开始执行")
    log.info(f"检测到{len(config_AirPort)}个账号")
    for i in range(len(config_AirPort)):
        account = config_AirPort[i]
        if exam_account(account):
            account = AirPort(account)
            account.checkin()
            sleep_random()
        continue


if __name__ == '__main__':
    main()