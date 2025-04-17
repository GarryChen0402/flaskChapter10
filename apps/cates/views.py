from flask import render_template, views, request, send_from_directory, redirect, url_for, jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import CombinedMultiDict

from apps.cates.models import GoodsCategory
from apps.cates.forms import GoodsCategoryForm
from apps.cates import cates_bp
from exts import db

import os

class GoodsCategoryView(views.MethodView):
    def get(self):
        cates = GoodsCategory.query.all()
        return render_template('shop/cates/index.html', cates=cates)

cates_bp.add_url_rule('/index', view_func=GoodsCategoryView.as_view('index'))

class ImgView(views.MethodView):
    def get(self):
        base_dir = os.path.abspath(os.path.dirname('media'))
        filepath = os.path.join(base_dir, 'media')
        filename = request.args.get('filename')
        return send_from_directory(filepath, filename)

cates_bp.add_url_rule('/show', view_func=ImgView.as_view('show'))


class GoodsCategoryAddView(views.MethodView):
    def __init__(self):
        self.alist = {}

    def binddata(self, id, n):
        datas = GoodsCategory.query.filter_by(parent_id=id)
        for data in datas:
            self.alist[data.cat_id] = self.spacelength(n) + data.name
            self.binddata(data.cat_id, n + 2)
        return self.alist

    def spacelength(self, i):
        space = ''
        for j in range(1, i):
            space += "&nbsp;&nbsp;"
        return space + "|--"

    def get(self):
        form_obj = GoodsCategoryForm()
        # cates_all=GoodsCategory.query.all()
        cates = self.binddata(0, 1)
        form_obj.parent_id.choices = cates
        return render_template("shop/cates/add.html", cates=cates, form_obj=form_obj)

    def post(self):
        # cates_all=GoodsCategory.query.all()
        cates = self.binddata(0, 1)
        f = GoodsCategoryForm(CombinedMultiDict([request.form, request.files]))
        if f.validate_on_submit():
            name = request.form.get("name", '')
            cate_obj = GoodsCategory.query.filter_by(name=name).first()
            if cate_obj:
                info = '分类已经存在'
                return render_template('shop/cates/add.html', form_obj=f, info=info, cates=cates)
            else:
                # 接收页面传递过来的参数，进行新增
                try:
                    cate = GoodsCategory()
                    cate.name = f.name.data
                    cate.parent_id = f.parent_id.data
                    file = f.logo.data  # 文件对象
                    print(file)
                    if file:
                        base_dir = os.path.abspath(os.path.dirname("media"))
                        filepath = os.path.join(base_dir, "media")
                        # print(filepath)
                        file.save(os.path.join(filepath, file.filename))
                        cate.logo = file.filename
                    cate.sort = f.sort.data
                    db.session.add(cate)
                    db.session.commit()
                except SQLAlchemyError as e:
                    print("err")
                    return render_template('shop/cates/add.html', form_obj=f, info="err", cates=cates)
                # 成功后，重定向到商品分类列表页面
                return render_template('shop/cates/index.html', form_obj=f, cates=cates)
        else:
            errors = f.errors
            return render_template("shop/cates/add.html", form_obj=f, info=errors, cates=cates)


cates_bp.add_url_rule("/add", view_func=GoodsCategoryAddView.as_view("add"))


class CategoryEditView(views.MethodView):
    def __init__(self):
        self.alist = {}

    def binddata(self, datas, id, n):
        datas = GoodsCategory.query.filter_by(parent_id=id)
        for data in datas:
            self.alist[data.cat_id] = self.spacelength(n) + data.name
            self.binddata(datas, data.cat_id, n + 2)
        return self.alist

    def spacelength(self, i):
        space = ''
        for j in range(1, i):
            space += "&nbsp;&nbsp;"
        return space + "|--"

    def get(self):
        cat_id = request.values.get("cat_id")
        cate_obj = GoodsCategory.query.filter_by(cat_id=cat_id).first()
        form_obj = GoodsCategoryForm()
        form_obj.name.data = cate_obj.name
        form_obj.logo.data = cate_obj.logo
        form_obj.sort.data = cate_obj.sort

        cates = self.binddata(0, 1)
        form_obj.parent_id.choices = cates
        return render_template("shop/cates/edit.html", cates=cates, form_obj=form_obj, cate=cate_obj)

    def post(self):
        cates = self.binddata(0, 1)
        f = GoodsCategoryForm(CombinedMultiDict([request.form, request.files]))
        if f.validate_on_submit():
            try:
                cat_id = request.values.get("cat_id")
                print(cat_id)
                cate = GoodsCategory.query.filter_by(cat_id=cat_id).first()
                print(cate)
                cate.name = f.name.data
                cate.parent_id = f.parent_id.data
                file = f.logo.data  # 原文件名
                if file:
                    base_dir = os.path.abspath(os.path.dirname("media"))
                    filepath = os.path.join(base_dir, "media")
                    file.save(os.path.join(filepath, file.filename))
                    cate.logo = file.filename
                cate.sort = f.sort.data
                db.session.commit()
                # 成功后，重定向到商品分类列表页面
                return redirect(url_for("cates.index"))
            except SQLAlchemyError as e:
                print("err")
                errors = f.errors
                return render_template('shop/cates/edit.html', form_obj=f, info=errors, cates=cates, cate=cate)
        else:
            errors = f.errors
            return render_template("shop/cates/edit.html", form_obj=f, info=errors, cates=cates, cate=cate)


cates_bp.add_url_rule("/edit", view_func=CategoryEditView.as_view("edit"))


class CategoryDelView(views.MethodView):

    def post(self):
        cat_id = request.values.get("cat_id")
        db.session.query(GoodsCategory).filter_by(cat_id=cat_id).delete()
        db.session.commit()
        data = {
            "msg": "数据删除成功",
            "code": "200"
        }
        return jsonify(data)


cates_bp.add_url_rule("/del", view_func=CategoryDelView.as_view("del"))


