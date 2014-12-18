# config.py

from authomatic.providers import  oauth1
from authomatic import Authomatic

CONFIG = {
    
    'tw': { # Your internal provider name
        
        # Provider class
        'class_': oauth1.Twitter,
        
        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '',
        'consumer_secret': '',
        'id': 1
    },
    
}