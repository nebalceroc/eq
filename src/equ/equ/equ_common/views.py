#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from equ_common.models import UserProfile, ImageArticle, Article, Category, Trade, TradeOffererArticle
from equ_common.forms import Article_New
from equ_common.services import get_article_dictionary
from userena.decorators import secure_required
from userena.forms import SignupFormOnlyEmail, AuthenticationForm
from helpers import init_categories
import datetime
from django.core.urlresolvers import reverse
from django.contrib.gis.geoip import GeoIP

"""
This view return the call to index,html
"""
def Home(request):
    if len(Category.objects.all()) == 0:
        init_categories()
    diccionary = dict()
    images = dict()
    consult = Article.objects.order_by('id').reverse()[:4]
    for img in consult:
        try:
            im = str(ImageArticle.objects.filter(key_article=img)[0].image)
        except:
            im = str()
        images[str(img.id)] = [im, str(img.name.encode('utf-8'))]
    diccionary['images'] = images
    diccionary['categories'] = Category.objects.exclude(subcategories=None)
    if request.user.is_authenticated():
        seller = UserProfile.objects.filter(user=request.user)[0]
        diccionary['recent_articles'] = Article.objects.filter(date__range=(datetime.datetime.now()+datetime.timedelta(-15),datetime.datetime.now())).exclude(seller=seller)[:4]
    else:
        diccionary['recent_articles'] = Article.objects.filter(date__range=(datetime.datetime.now()+datetime.timedelta(-15),datetime.datetime.now()))[:4]
    if request.user.is_authenticated():
        diccionary['pending_requests'] = list(set(get_pending_requests(request)))
        diccionary['user_items'] = get_items(request)
    return render(request,'index.html',diccionary)

"""
This view return a form of register 
"""
@secure_required
def RegisterUser(request):
    auth_basic_form = SignupFormOnlyEmail()
    if request.method == 'POST':
        user_form = SignupFormOnlyEmail(request.POST)
        
        if user_form.is_valid():
            try:
                user = User.objects.get(email__iexact=request.POST['email']) 
            except Exception as e:
                if 'does not exist' in str(e):
                    user=user_form.save()
                    user_auth = authenticate(identification=user.email, check_password=False)
                    if user_auth is not None:
                        login(request,user_auth)
                        request.session['register'] = True
                        return redirect("/change_user/")
                    else:
                        login_form = AuthenticationForm()
                        diccionary = {'messageReg':'User already exists', 'login':login_form, 'auth_basic':auth_basic_form, }
                        return render(request,"login.html", diccionary)
                else:
                    login_form = AuthenticationForm()
                    diccionary = {'messageReg':'User already exists', 'login':login_form, 'auth_basic':auth_basic_form, }
                    return render(request,"login.html", diccionary)
        else:
            message = 'Invalid data. Please use different information to register'
            if 'email' in user_form.errors:
                message = user_form.errors['email']
            login_form = AuthenticationForm()
            login_form.fields['identification'].label = 'Email'
            diccionary = {'messageReg':message, 'login':login_form, 'auth_basic':auth_basic_form, }
            return render(request,"login.html", diccionary)
    else:
        return redirect("/login/")
"""
This function return the template for do the login user
"""
def LoginUser(request):
    url_redirect = request.GET.get("next", "/")
    auth_basic_form = SignupFormOnlyEmail()
    if request.method == 'POST':
        login_form = AuthenticationForm(request.POST)
        login_form.fields['identification'].label = 'Email'
        if login_form.is_valid():
            username = request.POST['identification']
            password = request.POST['password']
            user = authenticate(identification=username, password=password)
            if user is not None:
                login(request,user)
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
 
                g = GeoIP()
                #lat,lon = g.lat_lon(ip)
                lat,lon = g.lat_lon('186.83.0.68')
                UserProfile.objects.filter(user=user).update(coords = 'POINT(' + str(lon) +' ' +str(lat)+ ')')
                return redirect(url_redirect)
            else:
                diccionary = {'message':'Invalid information', 'login':login_form, 'auth_basic':auth_basic_form, }
        else:
            diccionary = {'message':'Invalid information', 'login':login_form, 'auth_basic':auth_basic_form, }
    else:
        login_form = AuthenticationForm()
        login_form.fields['identification'].label = 'Email'
        diccionary = {'login':login_form, 'auth_basic':auth_basic_form, }
    if 'message' in request.session:
        diccionary['message'] = request.session['message']
        del request.session['message']
    return render(request,'login.html',diccionary)

"""
This function do logout of an user
"""
def Logout_User(request):
    print UserProfile.objects.get(user=request.user).coords
    logout(request)
    return redirect('/')

"""
This function do up of an article of an user, the user must be logged
"""
@login_required(login_url='/login/')
def ArticleUp(request):
    msg = str()
    if request.method == 'POST':
        article_form = Article_New(request.POST)
        categories_arr = request.POST['item_categories'].split(',')
        if len(categories_arr) > 0 and len(request.FILES) > 0 and article_form.is_valid():
            user = UserProfile.objects.filter(user_id=request.user.id)[0]
            article = Article.objects.create(name=request.POST['name'], description=request.POST['description'], price=request.POST['price'], seller=user, date=datetime.datetime.now())
            #article = Article.objects.create(name=request.POST['name'], description=user.coords, price=request.POST['price'], seller=user, date=datetime.datetime.now())
            for i in range(len(request.FILES)):
                image = ImageArticle.objects.create(key_article=article, image=request.FILES['imgup-{0}'.format(i)])
                article.imagearticle_set.add(image)
            for cat in categories_arr:
                if cat != str():
                    category = Category.objects.get(id=cat)
                    article.category.add(category)
            request.session['message'] = 'You have added a new article to your account. <a href="{0}">View article</a>'.format(reverse('product_detail', kwargs={ 'num':article.id }))
            return redirect('your_items')
        else:
            msg = 'Please complete the form.'
    else:
        article_form = Article_New()
    diccionary = {'article_form': article_form, 'message': msg, 'mod':False,}
    diccionary['categories'] = Category.objects.exclude(subcategories=None)
    diccionary['pending_requests'] = list(set(get_pending_requests(request)))
    if diccionary['message'] == str():
        del diccionary['message']
    return render(request, 'listing_item_description.html', diccionary)

"""
This function modify the informaction of an article
"""
@secure_required
@login_required(login_url='/login/')
def Article_Mod(request, id_article):
    article = Article.objects.get(id=id_article)
    message = str()
    if request.method == 'GET':        
        data = { 'modify':True, 'article_id':article.id,'article_form':Article_New(article.__dict__), 'categories':Category.objects.exclude(subcategories=None), 'article_categories':article.category.all, 'article_images':article.imagearticle_set.all }
        data['pending_requests'] = list(set(get_pending_requests(request)))
        return render(request, 'listing_item_description.html', data)
    elif request.method == 'POST':
        article.name = request.POST['name']
        article.price = request.POST['price']
        article.description = request.POST['description']
        article.save()
        images = json.loads(request.POST['item_images'])
        for img in images:
            if not img['url'].startswith(settings.MEDIA_URL):
                article.imagearticle_set.add(ImageArticle.objects.create(key_article=article, image=request.FILES[img['name']]))
        article.category.clear()
        for cat in request.POST['item_categories'].split(','):
            category = Category.objects.get(id=cat)
            article.category.add(category)
        message = 'Article {0} modified successfully.'.format(article.name.encode('utf-8'))
    if message != str():
        request.session['message'] = message
    return redirect('your_items')

"""
This function delete an article
"""
@secure_required
@login_required(login_url='/login/')
def Delete_Article(request, id_art):
    article = Article.objects.get(id=id_art)
    article.delete()
    return redirect('your_items')

"""
This view print the list of articles contained in the table of Article
"""
def Listing_Article(request):
    consult = Article.objects.all()
    #This dictionary of images:
    dic_images = {}
    for field in consult:
        dic_images[field.name] = str(ImageArticle.objects.get(id=field.id).image)
    #This attributte 
    article_print = {}
    for field in consult:
        article_print[field.name] = [field.id, field.description, field.price, field.quantity]
    diccionary = {'article_print': article_print, 'image': dic_images}
    return render(request, 'lista_productos.html', diccionary)

"""
This view print the information of an article
"""
def Product_Detail(request, num):
    diccionary = dict() # It is a dictionary that send all information to template
    if request.method == 'GET':
        diccionary['article'] = Article.objects.get(id=num)
        if request.user.is_authenticated():
            user = UserProfile.objects.filter(user=request.user)[0]
            diccionary['user_items'] = Article.objects.filter(seller=user)
    if request.user.is_authenticated():
        seller = UserProfile.objects.filter(user=request.user)[0]
        diccionary['recent_articles'] = Article.objects.filter(date__range=(datetime.datetime.now()+datetime.timedelta(-15),datetime.datetime.now())).exclude(seller=seller)[:4]
    else:
        diccionary['recent_articles'] = Article.objects.filter(date__range=(datetime.datetime.now()+datetime.timedelta(-15),datetime.datetime.now()))[:4]
    if request.user.is_authenticated():
        diccionary['pending_requests'] = list(set(get_pending_requests(request)))
    if 'error' in request.session:
        diccionary['error'] = request.session['error']
    return render(request,'detalle_productos.html', diccionary)

"""
This function change the information of an user
"""
@secure_required
@login_required(login_url='/login/')
def Profile_Change(request):
    active_user = UserProfile.objects.filter(user_id=request.user.id)[0]

    diccionary = { 'msg':str() }
    if request.method == 'POST':
        form_pass = UserProfileForm(request.POST, request.FILES)
        if 'register' in request.POST:
            form_pass.fields['terms'].required = True
        
        if form_pass.is_valid():
            if 'password' in request.POST:
                if 'confirm_password' in request.POST:
                    if request.POST['password'] == request.POST['confirm_password']:
                        active_user.user.password = request.POST['password']
                    else:
                        diccionary['msg'] = 'Passwords don\'t match'
            if diccionary['msg'] == str():
                active_user.user.email = request.POST['email']
                active_user.celular = request.POST['mobile']
                active_user.city = request.POST['city']
                active_user.user.first_name = request.POST['first_name']
                active_user.user.last_name = request.POST['last_name']
                if 'password' in request.POST:
                    if 'confirm_password' in request.POST:
                        active_user.user.password = request.POST['password']

                active_user.user.save()
                
                if 'terms' in request.POST:
                    active_user.terms = request.POST['terms']
                categories = request.POST['user_categories'].split(',')
                if len(categories) > 0:
                    for user_cat in active_user.categories.all():
                        if user_cat.id not in categories:
                            active_user.categories.remove(user_cat)
                    for cat in categories:
                        if cat != str():
                            category = Category.objects.get(id=cat)
                            active_user.categories.add(category)
                else:
                    diccionary['msg'] = 'Select at least one category'
                active_user.save()
                try:
                    if 'register' in request.session:
                        del request.session['register']
                    if 'image' in request.FILES:
                        active_user.image = request.FILES['image']
                    active_user.save()
                except:
                    pass
                return redirect('home')
        else:
            diccionary['msg'] = 'Invalid data. Please fill all the fields of the form'
    form_data = dict()
    form_data['first_name'] = active_user.user.first_name
    form_data['last_name'] = active_user.user.last_name
    form_data['email'] = active_user.user.email
    form_data['mobile'] = active_user.celular
    form_data['city'] = active_user.city
    form_data['image'] = active_user.image
    form_pass = UserProfileForm(form_data, initial={ 'image':active_user.image })
    diccionary['form'] = form_pass
    diccionary['terms'] = active_user.terms
    diccionary['register'] = 'register' in request.session
    diccionary['image'] = active_user.image
    diccionary['user_categories'] = Category.objects.filter(userprofile=active_user)
    diccionary['categories'] = Category.objects.exclude(subcategories=None)
    diccionary['pending_requests'] = list(set(get_pending_requests(request)))
    if diccionary['msg'] == str():
        del diccionary['msg']
    return render(request,'change_profile.html', diccionary)

"""
This function list the items of an user
"""
@secure_required
@login_required(login_url="/login/")
def Your_Items(request):
    user_profile = UserProfile.objects.filter(user=request.user)[0]
    dictionary = { 'articles':Article.objects.filter(seller_id=user_profile.id) }
    dictionary['categories'] = Category.objects.exclude(subcategories=None)
    dictionary['pending_requests'] = list(set(get_pending_requests(request)))
    if 'message' in request.session:
        dictionary['message'] = request.session['message']
        del request.session['message']
    return render(request,'your_items.html',dictionary)

"""
This function search and make the pagination in the web site
"""
def Busqueda(request):
    search = request.GET['q']
    articles = list()
    if request.user.is_authenticated():
        seller = UserProfile.objects.filter(user=request.user)
        articles.extend(list(Article.objects.filter(name__icontains=search).exclude(seller=seller)))
        articles.extend(list(Article.objects.filter(description__icontains=search).exclude(seller=seller)))
    else:
        articles.extend(list(Article.objects.filter(name__icontains=search)))
        articles.extend(list(Article.objects.filter(description__icontains=search)))
    categories = Category.objects.filter(name_category__icontains=search)
    for cat in categories:
        if request.user.is_authenticated():
            seller = UserProfile.objects.filter(user=request.user)
            articles.extend(list(Article.objects.filter(category=cat).exclude(seller=seller)))
        else:
            articles.extend(list(Article.objects.filter(category=cat)))
            

    
    article_dictionary = []
    for article in list(set(articles)):
        article_dictionary.append(get_article_dictionary(article,request.user.userprofile.coords.distance(article.seller.coords)))

    #data = { 'articles':list(set(articles)) }
    data = { 'articles':article_dictionary }
    data['pending_requests'] = Trade.objects.filter(state='Pending')
    if request.user.is_authenticated():
        data['user_items'] = get_items(request)
    data['categories'] = Category.objects.exclude(subcategories=None)
    if 'message' in request.session:
        data['message'] = request.session['message']
        del request.session['message']
    elif 'error' in request.session:
        data['error'] = request.session['error']
        del request.session['error']
    return render(request, 'search/search.html', data)


# Novcat's development
from django.core.mail import EmailMultiAlternatives
import os, stripe, base64, json, hashlib
from helpers import obfuscate, deobfuscate
from forms import UserProfileForm, ForgotPasswordForm
from models import Buy

@secure_required
@login_required(login_url='login')
def list_trades(request):
    user_profile = UserProfile.objects.filter(user_id=request.user.id)
    articles = Article.objects.filter(seller_id=user_profile[0].id)
    data = dict()
    trades = list()
    for article in articles:
        receipts = Trade.objects.filter(receiver_article_id=article.id)
        trades.extend(list(receipts))
        offerers = TradeOffererArticle.objects.filter(article_id=article.id)
        for offerer in offerers:
            trades.append(Trade.objects.get(id=offerer.offerer_article.id))
    data['trades'] = list(set(trades))
    data['accepted'] = int()
    data['declined'] = int()
    data['pending'] = int()
    for trade in data['trades']:
        if trade.state == 'Pending':
            data['pending'] = int(data['pending']) + 1
        elif trade.state == 'Accepted':
            data['accepted'] = int(data['accepted']) + 1
        else:
            data['declined'] = int(data['declined']) + 1
    data['pending_requests'] = list(set(get_pending_requests(request)))
    return render(request, 'list_trades.jade', data)

def get_pending_requests(request):
    user_profile = UserProfile.objects.filter(user_id=request.user.id)
    articles = Article.objects.filter(seller_id=user_profile[0].id)
    pending = list()
    for art in articles:
        art_trades = Trade.objects.filter(receiver_article=art)
        for trad in art_trades:
            if trad.state != 'Declined':
                pending.append(trad)
        art_trades = TradeOffererArticle.objects.filter(article=art)
        for trad in art_trades:
            if trad.offerer_article.state != 'Declined':
                pending.append(trad)
    return pending

@secure_required
@login_required(login_url='login')
def delete_trade(request, trade_id):
    Trade.objects.get(id=trade_id).delete()
    return redirect('list_trades')

@secure_required
@login_required(login_url='login')
def respond_trade(request):
    if request.method == 'POST':
        trade = Trade.objects.get(id=request.POST['trade'])
        trade.state = request.POST['response']
        trade.date = date.today()
        trade.save()
        message = str()
        if request.POST['response'] == 'Accepted':
            message = 'Congratulations, your trade for {0} has been accepted.\n\nPlease log in Equallo to access the contact\'s information.\n\nRegards,\n\nThe Equallo team'.format(trade.receiver_article.name)
            message_file = '<p style="margin-bottom:15px">Congratulations, your trade for {0} has been accepted.</p><p style="margin-bottom:15px">Please log in Equallo to access the contact\'s information.</p><p style="margin-bottom:15px">Regards,</p><p style="margin-bottom:15px">The Equallo team</p>'.format(trade.receiver_article.name)
        else:
            message = 'We\'re sorry, your trade for {0} has been declined. Maybe try another item?\n\nRegards,\n\nThe Equallo team'.format(trade.receiver_article.name)
            message_file = '<p style="margin-bottom:15px">We\'re sorry, your trade for {0} has been declined. Maybe try another item?</p><p style="margin-bottom:15px">Regards,</p><p style="margin-bottom:15px">The Equallo team</p>'.format(trade.receiver_article.name)
        
        message_html = open(r'/home/equallo/eq/src/equ/equ/equ_common/static/files/trade_email.html').read()
        #message_html = open(r'/home/nicolas/git/equ_project/equ_project/src/equ/equ/equ_common/static/files/trade_email.html').read()
        
        message_html = message_html.replace('{{message}}',message_file)
        email_offerer = EmailMultiAlternatives('Trade result', message, settings.DEFAULT_FROM_EMAIL, [trade.tradeoffererarticle_set.all()[0].article.seller.user.email])
        email_offerer.attach_alternative(message_html, 'text/html')
        email_offerer.send(fail_silently=False)
        email_receiver = EmailMultiAlternatives('Trade result', message, settings.DEFAULT_FROM_EMAIL, [request.user.email])
        email_receiver.attach_alternative(message_html, 'text/html')
        email_receiver.send(fail_silently=False)
    return redirect('list_trades')

def get_items(request):
    user = UserProfile.objects.filter(user_id=request.user.id)[0]
    return Article.objects.filter(seller=user)

@secure_required
@login_required(login_url='login')
def create_trade(request):
    previous = request.META.get('HTTP_REFERER')
    data = { 'error':str(), 'message':str() }
    if request.method == 'POST':
        if request.POST['user_articles']:
            receiver = Article.objects.get(id=request.POST['article_id'])
            trade = Trade.objects.create(date=datetime.datetime.now(), state='Pending', receiver_article=receiver)
            user_articles_id = request.POST['user_articles'].split(',')
            for art_id in user_articles_id:
                offer = TradeOffererArticle.objects.create(article=Article.objects.get(id=art_id), offerer_article=trade)
                trade.tradeoffererarticle_set.add(offer)
            message = 'Your item is wanted!\n\nYou have received a trade for {0}.\n\nPlease log in to Equallo to receive further information.\n\nRegards,\n\nThe Equallo team'.format(receiver.name)
            message_file = '<p style="margin-bottom:15px">Your item is wanted!</p><p style="margin-bottom:15px">You have received a trade for {0}.</p><p style="margin-bottom:15px">Please log in to Equallo to receive further information.</p><p style="margin-bottom:15px">Regards,</p><p style="margin-bottom:15px">The Equallo team</p>'.format(receiver.name)
            
            message_html = open(r'/home/equallo/eq/src/equ/equ/equ_common/static/files/new_trade_email.html').read()
            #message_html = open(r'/home/nicolas/git/equ_project/equ_project/src/equ/equ/equ_common/static/files/new_trade_email.html').read()
            
            
            
            message_html = message_html.replace('{{message}}',message_file)
            email_receiver = EmailMultiAlternatives('New trade received', message, settings.DEFAULT_FROM_EMAIL, [receiver.seller.user.email])
            email_receiver.attach_alternative(message_html, 'text/html')
            email_receiver.send(fail_silently=False)
            request.session['message'] = 'Your trade has been sent.'
            return redirect('list_trades')
        else:
            data['error'] = 'You must offer at least one article.'
    if data['error'] != str():
        request.session['error'] = data['error']
    if data['message'] != str():
        request.session['message'] = data['message']
    return redirect(previous)

if settings.DEBUG:
    stripe.api_key = 'sk_test_j6XEtAa3NiA6uugPHbtDpe6I'
else:
    stripe.api_key = 'sk_live_QzSgvbMu1S2jBs96VycxegcA'

@secure_required
@login_required(login_url='login')
def buy_article_information(request):
    previous = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        print request.POST

        token = request.POST['stripe_token']
        try:
            stripe.Charge.create(
                amount=199, # amount in cents, again
                currency="usd",
                card=token,
                description=request.user.email
            )
            article = Article.objects.get(id=request.POST['article_id'])
            user = UserProfile.objects.filter(user=request.user)[0]
            buy = Buy.objects.create(buyer=user, article=article, date_buy=datetime.datetime.now())
            if 'trade_id' in request.POST:
                trade = Trade.objects.get(id=request.POST['trade_id'])
                trade.buy = buy
                trade.save()
            request.session['message'] = 'Congratulations! Your payment was approved. You\'ll receive an email with the article\'s information'
            
            message_html = open(r'/home/equallo/eq/src/equ/equ/equ_common/static/files/buy_email.html').read().decode('utf8')
            #message_html = open(r'/home/nicolas/git/equ_project/equ_project/src/equ/equ/equ_common/static/files/buy_email.html').read().decode('utf8')
            
            message_html = message_html.replace('{{first_name}}',article.seller.user.first_name.decode('cp437').encode('utf8')).replace('{{last_name}}',article.seller.user.last_name.decode('cp437').encode('utf8')).replace('{{city}}',article.seller.city).replace('{{mobile}}', str(article.seller.celular)).replace('{{email}}', article.seller.user.email.encode('utf8'))
            message_text = 'Congratulations!\n\nYou have just bought the following contact information:\n\nContact name: {0} {1}\nContact location:{2}\nContact mobile:{3}\nContact email:{4}'.format(article.seller.user.first_name.decode().encode('utf8'), article.seller.user.last_name.decode().encode('utf8'), article.seller.city.decode().encode('utf8'), str(article.seller.celular), article.seller.user.email.encode('utf8'))
            send_email = EmailMultiAlternatives('Buy result', message_text, settings.DEFAULT_FROM_EMAIL, [user.user.email])
            send_email.attach_alternative(message_html, 'text/html')
            send_email.send(fail_silently=False)
        except stripe.CardError:
            request.session['error'] = 'We\'re sorry, we couldn\'t process your payment.'
    return redirect(previous)

def forgot_password(request, forgot_key=None):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            email = user[0].email
            data = '{0}&{1}'.format(email, (datetime.datetime.now()+datetime.timedelta(hours=24)).strftime('%d-%m-%Y %H:%M:%S'))
            sha = hashlib.sha256()
            sha.update(data)
            hash_key = base64.b64encode(sha.digest())
            forgot_key = obfuscate('{0}#{1}'.format(data, hash_key))
            if settings.DEBUG:
                message = 'http://localhost:8000/forgot_password/{0}/'.format(forgot_key)
            else:
                message = 'http://www.equallo.com/forgot_password/{0}/'.format(forgot_key)
            
            message_html = open(r'/home/equallo/eq/src/equ/equ/equ_common/static/files/forgot_password_email.html').read()
            #message_html = open(r'/home/nicolas/git/equ_project/equ_project/src/equ/equ/equ_common/static/files/forgot_password_email.html').read()
            
            message_html = message_html.replace('{{message}}',message)
            message_text = 'Forgot your password?\n\nPlease click the following link to set a new one.\n\n{0}'.format(message)
            send_email = EmailMultiAlternatives('Password reset', message_text, settings.DEFAULT_FROM_EMAIL, [email])
            send_email.attach_alternative(message_html, 'text/html')
            send_email.send(fail_silently=False)
        else:
            request.session['message'] = 'User not found'
    elif request.method == 'GET':
        try:
            link = deobfuscate(forgot_key)
            parts = link.split('#')
            sha = hashlib.sha256()
            sha.update(parts[0])
            hashing = base64.b64encode(sha.digest())
            if hashing == parts[1]:
                data = parts[0].split('&')
                if datetime.datetime.strptime(data[1],'%d-%m-%Y %H:%M:%S') >= datetime.datetime.now():
                    user = User.objects.filter(email=data[0])
                    if len(user) > 0:
                        form = ForgotPasswordForm(initial={ 'email':data[0] })
                        return render(request, 'forgot_password.jade', { 'form':form })
                    else:
                        request.session['message'] = 'Key to reset password not valid.'
                else:
                    request.session['message'] = 'Expired password recovery link.'
            else:
                request.session['message'] = 'Corrupted password recovery link.'
        except Exception as e:
            request.session['message'] = 'Corrupted password recovery link.'
    return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        data = { 'message':str(), 'error':str() }
        if form.is_valid():
            user = User.objects.filter(email=request.POST['email'])
            data['form'] = ForgotPasswordForm()
            if len(user) > 0:
                user = user[0]
                user.set_password(request.POST['password'])
                user.save()
                auth_user = authenticate(identification=request.POST['email'], password=request.POST['password'])
                if auth_user is not None:
                    login(request,auth_user)
                    return redirect('home')
                else:
                    data['error'] = 'Invalid login'
            else:
                data['error'] = 'Invalid user.'
        else:
            data['error'] = 'Passwords must match.'
        if data['error'] == str():
            del data['error']
        if data['message'] == str():
            del data['message']
        return render(request, 'forgot_password.jade', data)
    return render(request, 'forgot_password.jade', dict())
