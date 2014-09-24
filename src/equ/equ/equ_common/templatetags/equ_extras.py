#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()
"""
This filter search in the dictionary dic the key 'key' and
return a string 'cad' with all the contained of the dictionary
"""
@register.filter(name='filterdic')
def filterdic(dic,key):
    lista=dic[key]
    cad=""
    cad=cad+'<a href="/product_detail/'+str(lista.pop(0))+'">'+str(key.encode('utf-8'))+"</a></br>"
    
    for field in lista:
        try:
            cad=cad+(str(field.encode('utf-8')))+"<br/>"
        except:
            cad=cad+str(field)+"<br/>"
    return cad
register.filter('filterdic',filterdic)

"""
This function filter a dictionary contained in other dictionary
"""
def filterdicfordic(dic,key):
    cad = '<img width="80" height="80" src="'+str(dic['image'])+'" ><div class="item_info"><h2 class="list_items-title"><a href="/product_detail/'+str(dic['id'])+'">'+str(dic['name'].encode('utf-8'))+'</a></h2><p class="descrip">'+str(dic['description'].encode('utf-8'))+'</p></div>'+'<span class="price">'+'$'+str(dic['price'])+'</span>'
    cad = cad+'<div class="buttons"> <ul><li><a class="btn cancel" href="/art_delete/'+str(dic['id'])+'">Delete</a></li>'
    cad = cad+'<li><a class="btn" href="/mod_article/'+str(dic['id'])+'">Edit</a></li></ul></div>'
    return cad
register.filter('filterdicfordic',filterdicfordic)

@register.filter
def filter_category(art, categories):
    cat_general=art.filter(type_cat="games")
    return cat_general 
register.filter('filter_cat', filter_category)
