'''
/*
 * Copyright (C) 2019-2020 University of South Florida
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 '''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Use this class to share any default attributes with any subsequent
    classes that inherit from Config.
    """
    DEBUG = False
    TESTING = False
    
    # Only required when using the session object
    # Generated with secrets.token_urlsafe(16)
    # You could also use os.urandom(16)
    SECRET_KEY = os.environ.get('SECRET_KEY')

class ProductionConfig(Config):
    """
    This class will inherit any attributes from the parent Config class.
    Use this class to define production configuration atrributes, such
    as database usernames, passwords, server specific files & directories etc.
    """
    pass


class DevelopmentConfig(Config):
    """
    This class will inherit any attributes from the parent Config class.
    Use this class to define development configuration atrributes, such
    as local database usernames, passwords, local specific files & directories etc.
    """
    DEBUG = True