"""
WSGI config for corona_stat_tracking_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application
print('this one: ' + os.getcwd())
sys.path.append(os.getcwd())
os.environ.setdefault("PYTHON_EGG_CACHE", f"{os.getcwd()}/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corona_stat_tracking_site.settings")
application = get_wsgi_application()




# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corona_stat_tracking_site.settings')
#
# application = get_wsgi_application()
