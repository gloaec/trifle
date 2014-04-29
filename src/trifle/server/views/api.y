from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    #if current_user.is_authenticated():
    #    return redirect(url_for('frontend.app'))
    return render_template('index.html')
