import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    Set config variables or use environment variables.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or "You are not authorized to access this resource!"

    
