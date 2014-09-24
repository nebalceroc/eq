from userena.forms import SignupForm, AuthenticationForm
from equ_common.forms import DateAddRegisterForm
from equ_common.models import ImageArticle, UserProfile
import os
import stripe
from django.conf import settings

"""
Thist task defined the dictionary returned to the template register.html
The parameter message is the message of response send to the template
The parameter show is a boolean, True: watch the form, False: Not watch then form
"""
def Diccionary_register(message,show):
    if show:
        user_form = SignupForm()
        user_add_form = DateAddRegisterForm()
        diccionary = {'user':user_form,'additional':user_add_form,'message':message,'show':show}
    else:
        diccionary = {'message':message,'show':show}
    return diccionary

"""
This function save the image of profile of an user
"""
def Save_Image_Profile(user, image):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'statics/image_profile/' + str(user.username))):
        #create new file folder
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'statics/image_profile/' + str(user.username)))
    #name of the new file image
    name_image=os.path.join(settings.MEDIA_URL, "statics/image_profile/" + str(user.username) + "/" + image.name)
    #create new file
    image_save = file("../static_media"+name_image, 'wb')
    image_save.write(image.read())
    image_save.close()
    consult = UserProfile.objects.filter(user=user)
    consult.update(image = name_image)
    return True
"""
This task save the a image of the article send by the user in the form
of 'ArticleUp'. Return a object of type 'ImageArticle'
"""
def Save_Image_Article(article, user_id, image, nom_image):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'statics/image_article/' + user_id + "/" + str(article.id))):
        #create new folder
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'statics/image_article/' +user_id  + "/" + str(article.id)))
    #name of the new file image
    path_image=os.path.join(settings.MEDIA_ROOT, "statics/image_article/" + user_id + "/" + str(article.id) + "/"+image.name)
    name_image=os.path.join(settings.MEDIA_URL, "statics/image_article/" + user_id + "/" + str(article.id) + "/"+image.name)
    asign = 1
    while os.path.exists(path_image):
        path_image=os.path.join(settings.MEDIA_ROOT, "statics/image_article/" + user_id + "/" + str(article.id) + "/"+ str(asign) + image.name)
        name_image=os.path.join(settings.MEDIA_URL, "statics/image_article/" + user_id + "/" + str(article.id) + "/"+ str(asign) + image.name)
        asign= asign+1
    #create new file
    image_save = file(path_image,'wb')
    image_save.write(image.read())
    image_save.close()
    image_article = ImageArticle(key_article=article,image=name_image)
    image_article.save()

"""
This function make the payment;
Return True if the payment if it was successful, otherwise False
"""
def Payment(request):
    payment=False
    """
    This space to make payment
    """
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://manage.stripe.com/account
    stripe.api_key = "sk_test_j6XEtAa3NiA6uugPHbtDpe6I"
    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']
    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        charge = stripe.Charge.create(
            amount=199, # amount in cents, again
            currency="usd",
            card=token,
            description="payinguser@example.com"
        )
        payment = True
    except stripe.CardError, e:
        # The card has been declined
        payment = False  
    return True
