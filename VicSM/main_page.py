from flask import (
    Blueprint, request, render_template
)

bp = Blueprint('main_page', __name__)


@bp.route('/')
def main_page():

    return render_template('main_page/main_page.html')
