from flask import (
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    request,
    flash,
)

from . import main
from .forms import IndexForm, CalcForm
from .controllers import (
    home,
    get_user_by_emoji,
    create_user,
    available_emojis,
    users_emojis,
    add_user_level,
    testi_seikkailu,
    next_calc,
    levels_percent,
    user_emoji,
    user_level,
    add_answer,
    send_stars,
)

from app import db
from sqlalchemy import select, String
from datetime import datetime
import giphypop


@main.route("/", methods=["GET", "POST"])
def index():
    form = IndexForm()

    form.vanha.choices = available_emojis()
    form.pelaaja.choices = users_emojis()

    if request.method == "POST" and form.validate():
        print("validointi onnistui")
        user = get_user_by_emoji(form.vanha.data)
        if user is None:
            new_user = create_user(form.vanha.data)
            add_user_level(new_user)
            session["pelaaja"] = new_user
        else:
            session["pelaaja"] = form.pelaaja.data
        if form.moodi.data == "seikkailu":
            return redirect(url_for(".seikkailu"))
        elif form.moodi.data == "tasot":
            return redirect(url_for(".tasot"))
    else:
        flash_errors(form)

        return render_template(
            "index.jinja",
            form=form,
        )


@main.route("/seikkailu", methods=["GET", "POST"])
def seikkailu():
    testi_seikkailu()

    # session["pelaaja"] =
    return render_template(
        "seikkailu.jinja",
        # pelaaja=session.get("pelaaja"),
    )


@main.route("/tasot", methods=["GET", "POST"])
def tasot():
    form = CalcForm()
    session["user_emoji"] = user_emoji(session.get("pelaaja"))
    session["user_level"] = user_level(session.get("pelaaja"))
    session["stars"] = send_stars(session.get("pelaaja"), session.get("user_level"), 1)
    if session.get("next_calc") is None:
        session["next_calc"] = next_calc(
            session.get("pelaaja"),
            session.get("user_level"),
            1,
            session.get("prev_answer"),
            session.get("pelaaja"),
        )
        print("seuraava:", session.get("next_calc"))
        session["prev_answer"] = session.get("next_calc")
    if request.method == "POST" and form.validate():
        vastaus = int(form.answer.data)
        oikea = session.get("prev_answer")
        print("vastaus:", vastaus, "oikea:", oikea[3], "lasku:", oikea[1], oikea[2])

        if vastaus == oikea[3]:
            oikea_vastaus = 1
            print("oikein!")
        else:
            oikea_vastaus = 0
            print("väärin!")
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
        answer = add_answer(
            session.get("pelaaja"), oikea[4], 1, int(oikea_vastaus), dt_string
        )

        # answers(session.get("pelaaja"), session.get("user_level"), 1)
        session["next_calc"] = next_calc(
            session.get("pelaaja"),
            session.get("user_level"),
            1,
            session.get("prev_answer"),
            session.get("pelaaja"),
        )
        # Jos level nousee
        if session.get("next_calc") == True:
            session["user_level"] = user_level(session.get("pelaaja"))
            session["next_calc"] = next_calc(
                session.get("pelaaja"),
                session.get("user_level"),
                1,
                session.get("prev_answer"),
                session.get("pelaaja"),
            )
            return redirect(url_for(".level_change"))
        print("seuraava:", session.get("next_calc"))
        session["prev_answer"] = session.get("next_calc")

        return redirect(url_for(".tasot"))
    return render_template("tasot.jinja", form=form)


@main.route("/tasot/onnea", methods=["GET", "POST"])
def level_change():
    session["user_emoji"] = user_emoji(session.get("pelaaja"))
    session["user_level"] = user_level(session.get("pelaaja"))
    giphy_api_key = os.environ.get('GIPHY_API_KEY')
    g = giphypop.Giphy(api_key=giphy_api_key)
    gif = g.random_gif("congratulations")
    print(gif.media_url)
    return render_template("level_change.jinja", gif=gif.media_url)


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "Virhe (%s) - %s" % (getattr(form, field).label.text, error),
                "error",
            )
