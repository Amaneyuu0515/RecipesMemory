# RecipesMemory
cd recipesmemory
python manage.py runserver
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': recipesmemory_db,
        'USER': root,
        'PASSWORD': amaneyuu0515,
        'HOST': containers-us-west-xxx.railway.app,
        'PORT': 3306,
    }
}
