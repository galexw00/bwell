from flask import Blueprint, render_template, redirect, url_for, session, request
from db import *

from helpers.flashes import *
from helpers.authority import *
from proxies import db, user


bp = Blueprint(
    "account",
    __name__,
    url_prefix="/account",
    template_folder="templates",
    static_folder="static",
)


@bp.route("/")
@login_required
def read():
    return render_template("account.j2")


@bp.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("read"))


@bp.route("/accounts")
@admin_rights_required
def accounts():
    users = db_get_users(db)
    return render_template("accounts.j2", users=users)


@bp.post("/delete_account/<int:user_id>")
@admin_rights_required
def delete_account(user_id):
    if user_id == user.user_id:
        flash_info("You can only delete your account via personal account page.")
    else:
        try:
            db_delete_user(db, user_id)
        except ModelError as error:
            flash_error(error)

    return redirect(request.referrer)