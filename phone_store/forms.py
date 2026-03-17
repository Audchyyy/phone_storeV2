from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, BooleanField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from phone_store.models import User
from phone_store.extensions import db

class RegisterForm(FlaskForm):
    username         = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=50)])
    email            = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    password         = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit           = SubmitField(label='Register')

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('Username นี้ถูกใช้งานแล้ว')

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user:
            raise ValidationError('Email นี้ถูกใช้งานแล้ว')

class LoginForm(FlaskForm):
    email    = StringField(label='Email / Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Keep me signed in')
    submit   = SubmitField(label='Sign In')

class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=50)],
                           render_kw={'readonly': 'readonly'})
    email    = EmailField(label='Email', validators=[DataRequired(), Email()],
                          render_kw={'readonly': 'readonly'})
    fullname = StringField(label='Fullname', render_kw={'placeholder': 'Enter Fullname'})
    avatar   = FileField(label='Update Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit   = SubmitField(label='Update Account')

class ProductForm(FlaskForm):
    name        = StringField(label='ชื่อสินค้า', validators=[DataRequired(), Length(max=100)])
    subtitle    = StringField(label='Subtitle', validators=[Optional(), Length(max=255)])
    description = TextAreaField(label='คำอธิบาย', validators=[Optional()])
    price       = FloatField(label='ราคา (฿)', validators=[DataRequired()])
    category    = SelectField(label='หมวดหมู่', choices=[
                      ('mac', 'Mac'), ('ipad', 'iPad'),
                      ('iphone', 'iPhone'), ('watch', 'Watch')
                  ], validators=[DataRequired()])
    image_url   = StringField(label='URL รูปภาพ', validators=[Optional()])
    model_url   = StringField(label='URL 3D Model (.glb)', validators=[Optional()])
    badge       = StringField(label='Badge', validators=[Optional(), Length(max=50)])
    submit      = SubmitField(label='บันทึก')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(label='รหัสผ่านปัจจุบัน', validators=[DataRequired()])
    new_password     = PasswordField(label='รหัสผ่านใหม่', validators=[DataRequired()])
    confirm_password = PasswordField(label='ยืนยันรหัสผ่านใหม่', validators=[DataRequired(), EqualTo('new_password')])
    submit           = SubmitField(label='เปลี่ยนรหัสผ่าน')