from __future__ import division
from django.conf import settings
from models import Category
from Crypto.Cipher import AES
import binascii

categories = [ 'Real State', 'Vehicle', 'Electronics', 'Others']
subcategories = { 
    'Real State':[ 'Apartments', 'Business', 'Houses', 'Premises', 'Restaurants', 'Storehouses', 'Studios', 'Others'],
    'Vehicle':[ 'Accessories & Parts', 'Boats & Yachts', 'Bicycles & Motorcycles', 'Car Audio', 'Cars & Trucks', 'Vans & Mini Vans', 'Others'],
    'Electronics':[ 'Blu-Ray & Home Theaters', 'Cameras & Video', 'Cellphones & Phones', 'Computers & Tablets', 'Headphones & Monitors', 'Instruments', 'Laptops & Printers', 'TV\'s & DVD\'s', 'Video Games & Consoles', 'Others'],
    'Others':[ 'Accesories' , 'Art & Antiques', 'Books', 'Babies', 'Collectibles & Memorabilia', 'Health & Beauty', 'Home & Garden', 'Services', 'Sporting Goods', 'Travel', 'Education', 'Others'],
    }

def init_categories():
    for cat in categories:
        category = Category.objects.create(name_category=cat)
        for subcat in subcategories[cat]:
            subcategory = Category.objects.create(name_category=subcat)
            category.category_set.add(subcategory)

def padd(secret, blocksize=16, padding=' '):
    """Pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret

def obfuscate(value):
    secret = padd(settings.SECRET_KEY[0:16])
    encobj = AES.new(secret)
    
    value = value + (" " * (16 - (len(value) % 16)))
    encrypted = encobj.encrypt(value)
    hex_value = binascii.hexlify(encrypted)
    return binascii.b2a_base64(hex_value)[:-1].replace('+','-').replace('/','_')

def deobfuscate(value):
    secret = padd(settings.SECRET_KEY[0:16])
    encobj = AES.new(secret)
    value=value.replace('-','+').replace('_','/')
    decoded = binascii.a2b_base64(str(value))
    unhex = binascii.unhexlify(str(decoded))
    return encobj.decrypt(unhex).rstrip()

import unicodedata
from django.core.files.storage import FileSystemStorage

class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)