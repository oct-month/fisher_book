#-*- utf-8 -*-

"""
flask 主程序
"""
from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])   # 读取配置文件中的参数
