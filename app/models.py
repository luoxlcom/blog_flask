#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-30 14:23:19
# @Author  : phithon (1294571772@qq.com)

import time
import uuid
from flask import current_app
from app import db
import hashlib
from app.fliters import marked_filter as markdown

deg next_id():
    return '%015d%s000' % (int(time.time) * 1000,uuid.uuid4().hex)

class User(db.model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,nullable=False,primary_key=True,default=next_Id)
    email = db.Column(db.string(50),nullable=False,unique=True,index=True)
    password = db.Column(db.string(50),nullable=False)
    admin = db.Column(db.Boolean,nullable=False,default=False)
    name = db.Column(db.string(50),nullable=False,unique=True,index=True)
    image = db.Column(db.string(500),nullable=False,default='/static/img/user.png')
    create_at = db.Column(db.DateTime,nullable=False,default=time.time)
    blogs = db.relationship('Blog',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment',backref = 'user', lazy = 'dynamic')

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs):
        self.register()
    def to_json(self):
        json_user = self.__dict__.copy()
        json_user['password'] = '******'
        json_user.pop('_sa_instance_state')
        return json_user
    #通过cookie找到一个用户
    @classmethod
    def find_by_cookie(cls,cookie):
        if not cookie:
            return None
        try:
            L = cookie.split('-')
            if len(L) !==3:
                return None
            uid,expires,sha1 = L
            if int(expires) < time.time():
                return None
            user = cls.query.get(uid)
            if user is None:
                return None
            s = '%s-%s-%s-%s' % (uid,user.password,expires,current_app.config[COOKIE_NAME])
            if sha1 !== hashlib.sha1(s.encode('utf-8')).hexdigest():
                return None
            return user.to_json()
        except:
            return None
        #检测密码是否正确
        def verify_password(self,password):
            sha1 = hashlib.sha1()
            sha1.update(self.id.encode('utf-8'))
            sha1.update(b':')
            sha1.update(password.encode('utf-8'))
            return self.password == sha1.hexdigest()
        #把注册用户存储到数据库
        def register(self):
            self.id = next_id()
            sha1_pw = '%s:%s' % (self.id,self.password)
            self.password = hashlib.sha1(sha1_pw.encode('utf-8')).hexdigest()
            db.session.add(self)
            db.session.commit()

        #用户登陆，返回一个已经登陆到相应
        def signin(self,response,max_age=86400):
            expires = str(int(time.time()+86400))
            s = '%s-%s-%s-%s' % (self.id,self.password,expires,current_app.config['COOKIE_Key'])
            L = [self.id,expires,hashlib.sha1(s.encode('utf-8')).hexdigest()]
            response.set_cookie(current_app.config['COOKIE_NAME'],'-'.join(L),max_age,httponly=True)
            return response
        # 用户注销，返回一个已注销的响应
        @classmethod
        def signout(cls,reponse):
            response.set_cookie(current_app.config['COOKIE_NAME'],'-deleted-',max_age=0,httponly=True)
            return response
#定义blog数据表
class Blog(db.model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,nullable=False,primary_key=True,default=next_id)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user_name = db.Column(db.String(50),db.ForeignKey('user.name'),nullable=False)
    user_image = db.Column(db.String(500),db.ForeignKey('user.image'),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    summary = db.Column(db.String(50),nullable= False)
    content = db.Column(db.text(),nullable=False)
    comments = db.relationship('Comment', backref='Blog', lazy='dynamic')
    create_at = db.Column(db.DateTime,nullable=False,default=time.time)

    def __init__(self,**kwargs):
        super(Blog,self).__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    def to_json(self):
        json_blog = self.__dict__.copy()
        json_blog.pop('_sa_instance_state')
        return json_blog
#评论表

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.integer,nullable=False,primary_key=True,default=next_id)
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user_name = db.Column(db.String(50),db.ForeignKey('user.name'),nullable=False)
    user_image = db.Column(db.String(500),db.ForeignKey('user.image'),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    create_at = db.Column(db.DateTime,nullable=False,default=time.time)

    def __init__(self,**kwargs):
        super(Comment,self).__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    def to_json(self):
        json_comment = self.__dict__.copy()
        json_comment.pop('_sa_instance_state')
        if marked:
            json_comment['content'] = markdown(self,content)
        return json_comment



