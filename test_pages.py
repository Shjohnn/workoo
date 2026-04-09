import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ishtop.settings')
django.setup()
from django.test import Client
c = Client()

# Test profile page (own profile — need auth)
# First register a fresh user
import random
username = 'testuser_' + str(random.randint(10000,99999))
r = c.post('/accounts/royxat/', {
    'first_name': 'Ali',
    'last_name': 'Valiyev',
    'username': username,
    'password1': 'TestPass123!',
    'password2': 'TestPass123!',
    'role': 'worker',
    'region': 'toshkent_shahar',
    'phone': '+998901234567',
})
print('REGISTER POST (' + username + '): ' + str(r.status_code) + ' -> ' + r.get('Location', 'no redirect'))

# Test profile
r2 = c.get('/accounts/profil/')
print('PROFILE OWN: ' + str(r2.status_code))

# Test job create page
r3 = c.get('/ishlar/yaratish/')
print('JOB CREATE: ' + str(r3.status_code))

# Test chat list
r4 = c.get('/chat/')
print('CHAT LIST: ' + str(r4.status_code))

# Test job list
r5 = c.get('/ishlar/?region=toshkent_shahar&category=qurilish')
print('ISHLAR FILTER: ' + str(r5.status_code))
