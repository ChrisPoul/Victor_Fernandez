from flask import (
    Blueprint, render_template
)
from VicSM.models import (
    Product, Client, Receipt, format_date
)

bp = Blueprint('main_page', __name__)


@bp.route('/')
def main_page():
    recent_receipts = Receipt.query.all()
    clients = Client.query.all()
    products = Product.query.all()

    return render_template(
        'main_page/main_page.html', clients=clients,
        products=products, format_date=format_date,
        receipts=recent_receipts
    )
