#from userena.tests.profiles.test import ProfileTestCase
#from userena.models import UserenaSignup
from django.test import TestCase
from equ_common.models import User, ImageArticle, Article, UserProfile, Buy
from django.core.files import File
import datetime

class UserTest(TestCase):
    def test_user_addition(self):
        """
        Tests that do the register of user 
        """
        user = User()
        user.username = "fab48"
        user.first_name = "Cristian"
        user.last_name = "Rodriguez"
        user.email = "asdf@cd.com"
        user.password = "asdf"
        user.save()

        con = User.objects.all()
        self.assertEqual(con[1].email, user.email)

    def test_load_image(self):
        image_article = ImageArticle()
        image_article.image = File(open("/tmp/debian1.jpg"))
        image_article.name = "prueba"
        image_article.save()

        r = ImageArticle.objects.all()

    def test_create_article(self):
        
        """
        Test that do the add of articles
        """
        user = User()
        user.username = "fab48"
        user.first_name = "cristian"
        user.last_name = "rodriguez"
        user.email = "asdf@cd.com"
        user.password = "asdf"
        user.save()
        
        image_article = ImageArticle()
        image_article.image = File(open("/tmp/debian1.jpg"))
        image_article.name = "prueba"
        image_article.save()

        article = Article()
        article.quantity = 1
        article.seller = user
        article.name = "posillo"
        article.description = "Posillo de color cafe"
        article.price = 3333.3333
        article.image = image_article
        article.state = True
        article.stanby = False
        article.save()
        
        prueba = Article.objects.all()
        self.assertEqual(prueba[0].name, "posillo")

    def test_user_profile(self):
        
        """
        Test that add the characterics additional of the users 
        """
        
        user = User()
        user.username = "fab48"
        user.first_name = "cristian"
        user.last_name = "rodriguez"
        user.email = "asdf@cd.com"
        user.password = "asdf"
        user.save()
        print("-----------------")        
        print type(user)
        print("-----------------")        
        profile = UserProfile()
        profile.user = user
        profile.phone = 7696650
        profile.celular = 1111111111
        profile.state = "cundinamarca"
        profile.city = "Bogota"
        profile.image = File(open("/tmp/debian1.jpg"))
        profile.save()

        p = UserProfile.objects.all()
        
        self.assertEqual(p[0].phone, 7696650)

    def test_buy(self):
        """
        Test that add the buy that do a user
        """
        user = User()
        user.username = "fab48"
        user.first_name = "cristian"
        user.last_name = "rodriguez"
        user.email = "asdf@cd.com"
        user.password = "asdf"
        user.save()
        
        image_article = ImageArticle()
        image_article.image = File(open("/tmp/debian1.jpg"))
        image_article.name = "prueba"
        image_article.save()
        
        article = Article()
        article.quantity = 1
        article.seller = user
        article.name = "posillo"
        article.description = "Posillo de color cafe"
        article.price = 3333.3333
        article.image = image_article
        article.state = True
        article.stanby = False
        article.save()
        
        user2 = User()
        user2.username = "fab123"
        user2.first_name = "cristian"
        user2.last_name = "rodriguez"
        user2.email = "asdf@cd.com"
        user2.password = "asdf"
        user2.save()

        buy = Buy()
        buy.date_buy = datetime.datetime.strptime('17/06/2013 6:44', '%d/%m/%Y %H:%M') 
        buy.article=article
        buy.buyer=user2
        buy.save()

        r = Buy.objects.all()

        self.assertEqual(r[0].buyer, user2)

