# -*- coding: utf-8 -*-
from datetime import datetime, date
from App import db


class User(db.Model):
    """用户"""
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = db.Column(db.String(32), doc='手机号码', primary_key=True)
    nickname = db.Column(db.String(20), doc='昵称', default='Wanted User', nullable=False, unique=True)
    password = db.Column(db.String(32), doc='密码', nullable=False)
    payPassword = db.Column(db.String(32), doc='支付密码', nullable=False)
    money = db.Column(db.Float, doc='账户余额', default=50, nullable=False)
    description = db.Column(db.String(50), doc='个性签名', default='这个人很懒，什么也没留下', nullable=False)
    isAdmin = db.Column(db.Boolean, doc='是否管理员', default=False)

    orders = db.relationship('Order', backref='users', cascade='all', lazy='dynamic')
    coupons = db.relationship('Coupon', backref='users', cascade='all', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='users', cascade='all', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', cascade='all', lazy='dynamic')


class Store(db.Model):
    """店铺"""
    __tablename__ = 'stores'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = db.Column(db.String(32), primary_key=True)
    storeName = db.Column(db.String(32), doc='店铺名称', nullable=False, unique=True)
    location = db.Column(db.String(32), doc='位置', nullable=False)
    isDiscount = db.Column(db.Boolean, doc='店铺名称', nullable=True)
    description = db.Column(db.Text, doc='店铺介绍', default='暂无介绍', nullable=False)
    rating = db.Column(db.Float, doc='评分', nullable=True)
    ratingNum = db.Column(db.SmallInteger, doc='评分人数', default=0)
    img = db.Column(db.String(40), doc='店铺头像路径')

    recommends = db.relationship('Recommend', backref='stores', cascade='all', lazy='dynamic')
    dishes = db.relationship('Dishes', backref='stores', cascade='all', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='stores', cascade='all', lazy='dynamic')
    comments = db.relationship('Comment', backref='stores', cascade='all', lazy='dynamic')


class Dishes(db.Model):
    """菜品"""
    __tablename__ = 'dishes'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = db.Column(db.String(32), primary_key=True)
    dishName = db.Column(db.Integer, doc='菜名', nullable=False)
    dishPrice = db.Column(db.Float, doc='价格', nullable=False)
    storeId = db.Column(db.String(32), db.ForeignKey('stores.id'), nullable=False)

    orders = db.relationship('Order', backref='dishes', cascade='all', lazy='dynamic')


class Recommend(db.Model):
    __tablename__ = 'recommendation'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    storeId = db.Column(db.String(32), db.ForeignKey('stores.id'), primary_key=True, nullable=False)


class Order(db.Model):
    """订单"""
    __tablename__ = 'orders'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键

    id = db.Column(db.String(32), primary_key=True)
    dishesId = db.Column(db.String(32), db.ForeignKey('dishes.id'), nullable=False)
    username = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    createTime = db.Column(db.DateTime, doc='创建时间', nullable=False)
    status = db.Column(db.Boolean, doc='订单状态(0:未支付,1:已支付)', default=0, nullable=False)
    couponId = db.Column(db.String(32), db.ForeignKey('coupons.id'))
    payPrice = db.Column(db.Float, doc='实际支付', nullable=False)
    totalPrice = db.Column(db.Float, doc='原价', nullable=False)


class Coupon(db.Model):
    """优惠券"""
    __tablename__ = 'coupons'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键

    id = db.Column(db.String(32), primary_key=True)
    discount = db.Column(db.SmallInteger, doc='折扣', nullable=False, default=5)
    condition = db.Column(db.SmallInteger, doc='满多少元可用', default=30, nullable=False)
    username = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False, doc='手机号码')
    expiredTime = db.Column(db.Date, doc='过期时间', nullable=False)
    status = db.Column(db.Boolean, doc='状态(0:未使用,1:已使用)', default=0, nullable=False)


class Favorite(db.Model):
    """收藏"""
    __tablename__ = 'favorites'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键

    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False, doc='手机号码')
    storeId = db.Column(db.String(32), db.ForeignKey('stores.id'), nullable=False)


class Comment(db.Model):
    """评论"""
    __tablename__ = 'comments'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键

    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False, doc='手机号码')
    storeId = db.Column(db.String(32), db.ForeignKey('stores.id'), nullable=False)
    content = db.Column(db.Text, nullable=False, doc='评论内容')
    rating = db.Column(db.SmallInteger, nullable=False, doc='店铺评分')


db.create_all()




