from wtforms import StringField, widgets,BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField

class GoodsCategoryForm(FlaskForm):
    name = StringField(label="分类名称", validators=[DataRequired(message="分类名称不能为空"),
        Length(1, 30, message="长度1-30位")],
                       render_kw={'class': 'form-control', 'placeholder': "请输入分类名称"})

    parent_id = StringField(label="选择父类",validators=[
        DataRequired(message="请选择父类")],
                            render_kw={'class': 'form-control  custom-select', 'placeholder': "请选择父类"})

    sort = StringField(label="排序", validators=[
        DataRequired(message="排序值不能为空")],
                       render_kw={'class': 'form-control', 'placeholder': "请输入数字"})

    logo = FileField(label="分类图片", widget=widgets.FileInput(),
                       render_kw={'class': 'custom-file-input'})

    is_nav = BooleanField(label="导航显示",
                       render_kw={'class': 'form-control', 'placeholder': "请选择"})