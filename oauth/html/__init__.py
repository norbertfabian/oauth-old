# -*- coding: utf-8 -*-
import hashlib
import logging

from flask import g, redirect, request, render_template, after_this_request, url_for

from oauth import app, lib

@app.route('/api/html/logged/')
def logged():
    return render_template("html/logged.html")

@app.route('/')
def index():
    application_id = request.args.get(app.config['APPLICATION_GET_ARG'], False)
    return_path = request.args.get('REDIRECT_GET_ARG', False)

    #@after_this_request
    #def set_cookie(response):
        #response.set_cookie(app.config['APPLICATION_TOKEN_COOKIE'], value=application_id)
        #response.set_cookie(app.config['RETURN_PATH_COOKIE'], value=return_path)
        #return response

    args = {}
    if application_id:
        args[app.config['APPLICATION_GET_ARG']] = application_id

    if return_path:
        args[app.config['REDIRECT_GET_ARG']] = return_path

    url = url_for('auth', **args)
    return redirect(url)

@app.route('/api/html/blacklist/<email>/<hash>/')
def blacklist(email=None, hash=None):
    return 'Hej how'

@app.route('/api/html/auth/', methods=['get', 'post'])
def auth():
    '''
    Authenticate method

    Check, if user is authorize to oAuth server and authorize it if not.
    If user has no account, can create one

    '''
    # initial variables
    application = request.cookies.get(app.config['APPLICATION_TOKEN_COOKIE'])
    application = request.args.get(app.config['APPLICATION_GET_ARG'], application)

    # get application that want to user authorize
    if (isinstance(application, str) or isinstance(application, unicode)) and application.isdigit():
        application = int(application)
    else:
        application = app.config['APPLICATION_ID']
    application = lib.dbGetApplication(int(application))

    # get return path
    return_path = app.config['RETURN_PATH']
    return_path = request.cookies.get(app.config['RETURN_PATH_COOKIE'], return_path)
    if application is not None:
        return_path = application.return_path

    return_path = request.args.get(app.config['REDIRECT_GET_ARG'], return_path)

    if return_path is None:
        return_path = app.config['RETURN_PATH']

    # get information about user
    oauth_token = request.cookies.get(app.config['USER_TOKEN_COOKIE'])
    oauth_token = request.headers.get(app.config['USER_HEADER_FIELD'], oauth_token)
    oauth_token = lib.getValidToken(oauth_token)

    # Try login form
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = lib.authenticate(username, password)

        # password match
        if user is not None:
            # if user is authentivated
            if user.validation_type:
                lib.sendValidation(user)
                return redirect(url_for('validate', id_user=user.id))

            oauth_token = lib.getUserToken(user)

    # everythink is OK, create token for application
    if oauth_token is not None:
        token = None
        if application is None or application.id == app.config['APPLICATION_ID']:
            token = oauth_token
        else:
            token = lib.getUserToken(oauth_token.id_user, application)

        @after_this_request
        def set_cookie(response):
            response.set_cookie(app.config['USER_TOKEN_COOKIE'],value=oauth_token.token, expires=oauth_token.expiration)
            response.set_cookie(app.config['APPLICATION_TOKEN_COOKIE'], value='', expires=0)
            response.set_cookie(app.config['RETURN_PATH_COOKIE'], value='', expires=0)
            return response

        return_path = '%s&token=%s' % (return_path, token.token)
        #app.logger.info("REDIRECT %s(%d) -> %s" % (token.user.username, token.id_application, return_path,))
        return redirect(return_path)


    # user is not authorized, show login form
    @after_this_request
    def set_cookie(response):
        response.set_cookie(app.config['USER_TOKEN_COOKIE'],value='')
        if application is not None:
            response.set_cookie(app.config['APPLICATION_TOKEN_COOKIE'], value=str(application.id))
        response.set_cookie(app.config['RETURN_PATH_COOKIE'], value=return_path)
        return response
    return render_template("html/auth.html")

@app.route('/api/html/logout/')
def logout():
    token = request.cookies.get(app.config['USER_TOKEN_COOKIE'])
    token = request.headers.get(app.config['USER_HEADER_FIELD'], token)
    lib.removeToken(token)
    return redirect(url_for('index'))


@app.route('/api/html/validate/', methods=['get', 'post'])
def validate():
    '''
    Validate user by secret
    '''
    application = app.config['APPLICATION_ID']
    application = request.cookies.get(app.config['APPLICATION_TOKEN_COOKIE'], application)
    application = request.args.get(app.config['APPLICATION_GET_ARG'], application)

    if isinstance(application, int) or application.isdigit():
        application = lib.dbGetApplication(int(application))
    else:
        application = lib.dbGetApplication(app.config['APPLICATION_ID'])

    oauth_token = request.cookies.get(app.config['USER_TOKEN_COOKIE'])
    oauth_token = request.headers.get(app.config['USER_HEADER_FIELD'], oauth_token)
    oauth_token = lib.getValidToken(oauth_token)
    user = None
    if oauth_token is None:
        id_user = request.args.get('id_user')
        id_user = request.form.get('id_user', id_user)
        secret = request.args.get('secret')
        secret = request.form.get('secret', secret)
        if id_user.isdigit():
            id_user = int(id_user)
            user, oauth_token = lib.validate(id_user, secret)

        if user is None:
            params = {'id_user': id_user}
            return render_template('html/validation.html', **params)

    @after_this_request
    def set_cookie(response):
        response.set_cookie(app.config['USER_TOKEN_COOKIE'],value=oauth_token.token, expires=oauth_token.expiration)
        return response

    return redirect(url_for('auth'))

@app.route('/api/html/confirm/<int:id_user>/<secret>/')
def confirm(id_user=None, secret=None):
    user, oauth_token = lib.validate(id_user, secret)
    if user is None:
        return render_template('html/confirm.html')

    @after_this_request
    def set_cookie(response):
        response.set_cookie(app.config['USER_TOKEN_COOKIE'],value=oauth_token.token, expires=oauth_token.expiration)
        return response
    return redirect(url_for('auth'))

@app.route('/api/html/registration/', methods=['get', 'post'])
def registration():
    g.errors = {}
    if request.method == 'POST':
        email = request.form.get('email')
        if email is None:
            g.errors['email'] = 'Email nebyl zadany'
        else:
            if not lib.validateEmail(email):
                g.errors['email'] = 'Neplatny email'

        username = request.form.get('username')
        user = lib.dbGetUserId(username)
        if user:
            g.errors['username'] = 'Uzivatel jiz existuje'

        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password is None:
            g.errors['password'] = 'heslo nebylo zadane'
        else:
            if not lib.validatePassword(password):
                g.errors['password'] = 'Heslo je kratsi nez nez znaku'

        if password != password_confirm:
            g.errors['password_confirm'] = 'Hesla se neshoduji'

        if not g.errors:
            user = lib.registerUser(username, email, password)
            g.registration_done = True

    return render_template("html/registration.html")


@app.template_filter('h1')
def h1(v):
    return u'%s\n%s' % (v, '='*len(v))

@app.template_filter('h2')
def h2(v):
    return u'%s\n%s' % (v, '-'*len(v))

@app.template_filter('hashmail')
def hashmail(email):
    if email is None:
        return
    hasher = hashlib.sha1()
    hasher.update(unicode(email))
    return hasher.hexdigest()


if app.config.get('DEBUG'):
    from oauth.html import email
