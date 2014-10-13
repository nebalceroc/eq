#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.gis.db.models import PointField, GeoManager
from django.contrib.gis.geos import GEOSGeometry, fromstr
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from stdimage import StdImageField

"""
It is a list of categories for an article
"""
class Category(models.Model):
    name_category = models.CharField(max_length=70)
    subcategories = models.ForeignKey('self', null=True)

"""
It is the information of contact of a user.
"""
class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name="userprofile")
    phone = models.IntegerField(_('phone'), null=True, blank=True)
    celular = models.IntegerField(_('mobile'), null=True, blank=True)
    state = models.CharField(_('state'), max_length=30,blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True)
    image = StdImageField(_('image'), upload_to='statics/image_profile/', blank=True, variations={ 'large':(470,470), 'thumbnail':(80, 80, True), 'small':(180, 180, True) })
    zipcode = models.IntegerField(_('zipcode'), null=True, blank=True)
    adress = models.CharField(_('address'), max_length=50, blank=True)
    terms = models.BooleanField(_('terms'),default=False)
    welcome = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)
    coords = PointField(null=True)
    objects = GeoManager()

"""
This is the atributtes of a article.
"""
class Article(models.Model):
    seller = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(decimal_places=4, max_digits=10)
    category = models.ManyToManyField(Category)
    date = models.DateField()

"""
It is the diferent images that has a article.
"""
class ImageArticle(models.Model):
    key_article = models.ForeignKey(Article)
    image = StdImageField(upload_to='statics/image_article/', variations={ 'large':(470,470), 'thumbnail':(80, 80, True), 'small':(180, 180, True) })

"""
It is a register of the sales made by the users
"""
class Buy(models.Model):
    date_buy = models.DateTimeField()
    article = models.ForeignKey(Article)
    buyer = models.ForeignKey(UserProfile)

class Trade(models.Model):
    date = models.DateTimeField()
    receiver_article = models.ForeignKey(Article, unique=False)
    state = models.CharField(max_length=100)
    buy = models.ForeignKey(Buy, null=True, blank=True)

class TradeOffererArticle(models.Model):
    offerer_article = models.ForeignKey(Trade)
    article = models.ForeignKey(Article)
