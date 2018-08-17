from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1,name='one plus 3 event',status=True,limit=20,
                             address='上海闵行',start_time='2018-07-27 17:06:00')
        Guest.objects.create(id=1,event_id=1,realname='alen',phone='13711110000',email='alen@mail.com',sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='one plus 3 event')
        self.assertEqual(result.address,'上海闵行')
        self.assertTrue(result.status)

    def test_guest_manage(self):
        result = Guest.objects.get(realname='alen')
        self.assertFalse(result.sign)
        self.assertEqual(result.phone,'13711110000')
        self.assertEqual(result.email,'alen@mail.com')


class IndexPageTest(TestCase):
    '''测试index登录首页'''

    def test_index_page_renders_index_template(self):
        '''测试index试图'''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    '''登录测试'''

    def setUp(self):
        User.objects.create_user('admin','admin@email.com','admin123456')

    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@email.com')
        #self.assertEqual(user.password,'admin123456')

    def test_login_action_username_password_null(self):
        '''账号密码为空'''
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_username_password_error(self):
        '''密码错误'''
        test_data = {'username':"admin",'password':'111111'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_success(self):
        '''登录成功'''
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action',data=test_data)
        self.assertEqual(response.status_code,301)

class EventManageTest(TestCase):
    '''发布会管理测试'''
    def setUp(self):
        User.objects.create_user('admin','admin@email.com','admin123456')
        Event.objects.create(id=1,name='one plus 3 event',status=True,limit=20,
                             address='上海闵行',start_time='2018-07-27 17:06:00')
        self.login_uesr = {'username':'admin','password':'admin123456'}

    def test_event_manage_success(self):
        '''发布会测试'''
        response = self.client.post('/login_action/',data=self.login_uesr)
        self.assertEqual(response.status_code,302)
        response = self.client.get('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'one plus 3 event',response.content)
        #self.assertIn('上海闵行',response.content)

    def test_event_manage_search(self):
        '''发布会搜索功能测试'''
        response = self.client.post('/login_action/',data=self.login_uesr)
        self.assertEqual(response.status_code,302)
        response = self.client.get('/search_name/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'one plus 3 event',response.content)
       # self.assertIn('上海闵行',response.content)