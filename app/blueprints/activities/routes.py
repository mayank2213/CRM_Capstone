from flask import Blueprint, render_template
from flask_login import login_required

activities_bp = Blueprint("activities", __name__)


@activities_bp.route("/")
@login_required
def index():
    return render_template("activities/index.html")
