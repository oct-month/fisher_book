from . import web       # 使用相对路径导入，父模块应被优先加载
from flask import render_template, flash

@web.route("/login")
def login():
    return "login"

@web.route("/")
def index():
    flash("1、你好", category='error')
    flash("2、搞事", category='warning')
    return render_template("test.html")
