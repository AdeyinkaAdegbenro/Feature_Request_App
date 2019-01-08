import sys
path = '/home/adeyinka/mysite/FeatureRequestApp'
if path not in sys.path:
   sys.path.insert(0, path)

from app import app as application