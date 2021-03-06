# Source Generated with Decompyle++
# File: index.pyc (Python 2.7)

import os
import re
import sys
from hasher import ZXHash
import webapp2
import logging
import secrets
from google.appengine.ext import ndb
hexre = re.compile('^[a-fA-F0-9]+$')
pathre = re.compile('^[\\w_\\-/\\.]+$')

class PrivateNote(ndb.Model):
    content = ndb.StringProperty()
    
    def get_by_user(cls, user):
        cls.query().filter(cls.user == user).get()

    get_by_user = classmethod(get_by_user)
    
    def get_by_id(identifier):
        key = ndb.Key(PrivateNote, identifier)
        return key.get()

    get_by_id = staticmethod(get_by_id)


class Utils(object):
    
    def reply(response, code, msg, mime = 'text/html'):
        response.status = code
        response.headers.add('X-Served-By', 'index.py')
        response.content_type = mime
        response.write(msg)

    reply = staticmethod(reply)
    
    def parse_urlform(form, delim = ';'):
        data = form.split(delim)
        results = dict()
        for datum in data:
            
            try:
                (key, value) = datum.split('=')
                results[key.strip()] = value.strip()
            continue
            continue
            continue

        
        return results

    parse_urlform = staticmethod(parse_urlform)
    
    def get_user(headers, hasher):
        results = Utils.parse_urlform(headers['cookie'])
        
        try:
            if results['auth']:
                (user, hmac) = results['auth'].split('-')
                if hexre.match(user) and hexre.match(hmac) and hasher.hash(user.strip()) == hmac.strip():
                    return (user.strip(), hmac.strip())
        except:
            pass

        return (None, None)

    get_user = staticmethod(get_user)


class HealthCheckHandler(webapp2.RequestHandler):
    
    def get(self):
        self.response.status = 200



class ValidateHandler(webapp2.RequestHandler):
    
    def get(self):
        (user, _) = Utils.get_user(self.request.headers, hasher)
        if not user:
            return Utils.reply(self.response, 401, 'Bad Authentication')
        return None.reply(self.response, 200, user)



class PrivateNote(ndb.Model):
    content = ndb.TextProperty()
    
    def get_by_user(cls, user):
        cls.query().filter(cls.user == user).get()

    get_by_user = classmethod(get_by_user)
    
    def get_by_id(identifier):
        key = ndb.Key(PrivateNote, identifier)
        return key.get()

    get_by_id = staticmethod(get_by_id)


class RegisterHandler(webapp2.RequestHandler):
    
    def post(self):
        data = Utils.parse_urlform(self.request.body, '&')
        value = data['username']
        logging.warning('value: [' + str(value) + ']')
        if len(value) > 64:
            return Utils.reply(self.response, 400, 'Limit Username to 32 Characters')
        if None and hexre.match(value):
            note = PrivateNote.get_by_id(value)
            logging.warning('note: ' + str(note))
            if note:
                return Utils.reply(self.response, 403, 'User already Exists')
            hashed = None.hash(value)
            self.response.status = 200
            self.response.headers.add('X-Served-By', 'index.py')
            self.response.headers.add('Content-Type', 'text/plain')
            self.response.headers.add('Set-Cookie', 'auth=' + value + '-' + hashed)
            self.response.write(value + '-' + hashed)
            PrivateNote(id = value, content = '').put()
            return None
        logging.warning('Bad request? ' + str(value))
        return Utils.reply(self.response, 400, 'Bad Request!')



class PrivateNoteHandler(webapp2.RequestHandler):
    
    def get(self):
        (user, _) = Utils.get_user(self.request.headers, hasher)
        if user:
            note = PrivateNote.get_by_id(user)
            if note:
                return Utils.reply(self.response, 200, note.content, 'application/octet-stream')
            return None.reply(self.response, 404, 'File Not Found')
        return Utils.reply(self.response, 401, 'Bad Authentication')

    
    def post(self):
        (user, _) = Utils.get_user(self.request.headers, hasher)
        if user:
            if user in locked:
                return Utils.reply(self.response, 403, 'User is Locked')
            note = None.get_by_id(user)
            if not note:
                note = PrivateNote(id = user)
            note.content = self.request.body
            note.put()
            return Utils.reply(self.response, 200, 'Success')
        return None.reply(self.response, 401, 'Bad Authentication')


(key1, key2, db) = secrets.get()
locked_id = '436f7267316c3076657239393c332121'
locked = list()
locked.append(locked_id)
hasher = ZXHash(key1.encode('hex'), key2)
note = PrivateNote.get_by_id(locked_id)
if not note:
    note = PrivateNote(id = locked_id, content = db)
else:
    note.content = db
note.put()
