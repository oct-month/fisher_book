"""
http请求处理
"""
import requests

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        """从url 获取数据"""
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ""
        return r.json() if return_json else r.text

