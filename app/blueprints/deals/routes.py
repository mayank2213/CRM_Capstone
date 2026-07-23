from flask import Blueprint, render_template
from flask_login import login_required

deals_bp = Blueprint("deals", __name__)


@deals_bp.route("/")
@login_required
def index():
    return render_template("deals/index.html")
