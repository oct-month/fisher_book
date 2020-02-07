"""
涉及到内部机密的配置文件
"""
# 调试
DEBUG = True
# 启动时重置表
NEW_TABLE = False
# 数据库
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://test:test@localhost:3306/fisher?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# session密钥
SECRET_KEY = "session key"
