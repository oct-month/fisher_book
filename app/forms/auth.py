from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from app.models.user import User

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱地址不符合规范")])
    password = PasswordField(validators=[DataRequired(message="密码不能为空"), Length(6, 23)])


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱地址不符合规范")])
    password = PasswordField(validators=[DataRequired(message="密码不能为空"), Length(6, 23)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称需要2~10个字符")])

    def validate_email(self, field):                # 自定义验证器（被自动调用）
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮件已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("昵称已存在")


