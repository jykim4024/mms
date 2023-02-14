from flask import Blueprint, url_for, render_template, flash, request, session, jsonify

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/camTest/', methods=('GET', 'POST'))
def camTest():

    return render_template('test/camTest.html')

@bp.route('/camTest2/', methods=('GET', 'POST'))
def camTest2():

    return render_template('test/camTest2.html')