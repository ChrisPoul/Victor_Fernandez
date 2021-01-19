from flask import (
    Blueprint, g, render_template
)

bp = Blueprint('receipt', __name__)


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():

    return render_template('receipt/receipt.html')