from django.conf.urls import patterns, url, include
from views import *
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/$', RegisterUser, name="register"),
    url(r'^login/$', LoginUser, name="login"),
    url(r'^forgot_password/$', forgot_password, name="forgot_password"),
    url(r'^forgot_password/(?P<forgot_key>[^/]+)/$', forgot_password, name="forgot_password"),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^articleup/$', ArticleUp, name="article_up"),
    url(r'^art_delete/(\w+)/$', Delete_Article, name="article_delete"),
    url(r'^mod_article/(\w+)/$', Article_Mod, name="modify_article"),
    url(r'^logout/$', Logout_User, name="logout"),
    #url(r'^articleprint/$', Listing_Article, name="listing_article"),
    url(r'^product_detail/(?P<num>\d+)/$', Product_Detail, name="product_detail"),
    #url(r'^product_detail/(\w+)/contact/$', Dates_Contact, name="contact_user"),
    url(r'^change_user/$', Profile_Change, name="profile_change"),
    #url(r'^change_pass/$', Password_Change, name="pass_change"),
    url(r'^your_items/$', Your_Items ,name="your_items"),
    url(r'^trades/$', list_trades, name='list_trades'),
    url(r'^delete_trade/(?P<trade_id>\d+)/$', delete_trade, name='delete_trade'),
    url(r'^respond_trade/$', respond_trade, name='respond_trade'),
    url(r'^propose_trade/$', create_trade, name='propose_trade'),
    url(r'^buy_article_info/$', buy_article_information, name='buy_article_info'),
    # url(r'^equ/', include('equ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
