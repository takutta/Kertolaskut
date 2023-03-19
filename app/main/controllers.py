from app.models import (
    User,
    Emoji,
    Level,
    Level_Calc,
    Calc,
    Level_User,
    Answer,
    Game,
)

from flask import session
from app import db

from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from sqlalchemy import not_, select, String, Grouping
import random


def home():
    pass


def get_user_by_emoji(form_data):
    return db.session.scalar(select(User).where(User.emoji_id == form_data))


def create_user(form_data):
    new_user = User(emoji_id=form_data)
    db.session.add(new_user)
    db.session.commit()
    new_user_id = db.session.scalar(select(User.id).where(User.emoji_id == form_data))
    return new_user_id


def add_user_level(user_id):
    new_level = Level_User(level_id=1, user_id=user_id)
    db.session.add(new_level)
    db.session.commit()
    return new_level


def update_user_level(user_id):
    my_obj = db.session.scalar(select(Level_User).where(Level_User.user_id == user_id))
    my_obj.level_id += 1
    db.session.commit()


def add_answer(user, calc, game, right_answer, datetime):
    new_answer = Answer(
        user_id=user,
        calc_id=calc,
        game_id=game,
        right_answer=right_answer,
        datetime=datetime,
    )
    db.session.add(new_answer)
    db.session.commit()
    return new_answer


def available_emojis():
    new_emojis = (
        Emoji.query.filter(
            Emoji.id.notin_(
                db.session.query(User.emoji_id).filter(
                    User.emoji_id.isnot(None), User.emoji_id > 0
                )
            )
        )
        .order_by(func.random())
        .all()
    )
    return [(emoji.id, emoji.emoji) for emoji in new_emojis]


def users_emojis():
    emojis = User.query.join(Emoji).add_columns(User.id, Emoji.emoji).all()
    return [(str(User.id), User.emoji) for User in emojis]


def user_level(id):
    juttu = db.session.scalar(
        select(Level.id)
        .where(User.id == Level_User.user_id)
        .where(Level.id == Level_User.level_id)
        .where(User.id == id)
    )
    if juttu is None:
        return 1
    return juttu


def possible_calcs(id, level, game, prev_answer):
    print("user_level_calcs:", user_level_calcs(level))
    print("answer_sums:", answer_sums(id, level, game))
    print("prev_answer:", prev_answer)
    rights = 4
    lista = [x for x in user_level_calcs(level)]

    for calc in user_level_calcs(level):
        for summa in answer_sums(id, level, game):
            # same calc_id, summa >= 2, calc not same as previously
            if calc[4] == summa[1] and summa[2] >= rights or calc == prev_answer:
                if calc in lista:
                    lista.remove(calc)
    print("possible_calcs:", lista)
    return lista


def send_stars(id, level, game):
    answers = answer_sums(id, level, game)
    stars_amount = len(user_level_calcs(level))
    # full, half, empty
    lista = [0, 0, stars_amount]
    for answer in answers:
        if answer[2] >= 4:
            lista[0] += 1
            lista[2] -= 1
        elif answer[2] >= 2:
            # jos parillinen
            if lista[1] % 2 == 0:
                lista[1] += 1
                lista[2] -= 1
            else:
                lista[0] += 1
                lista[1] = 0
    print(lista)
    return lista


def answer_sums(id, level, game):
    return db.session.execute(
        select(Answer.id, Answer.calc_id, func.sum(Answer.right_answer))
        .where(User.id == id)
        .where(Game.id == game)
        .where(Level.id == level)
        .where(User.id == Answer.user_id)
        .where(Answer.game_id == Game.id)
        .where(Answer.calc_id == Calc.id)
        .where(Calc.id == Level_Calc.calc_id)
        .where(Level.id == Level_Calc.level_id)
        .group_by(Answer.calc_id)
    ).all()


def answers(id, level, game):
    sums = answer_sums(id, level, game)
    right_answers = 4

    icalc_list = user_level_calcs()

    if len(sums) == len(icalc_list):
        rights = len([x for x in sums if x[3] >= right_answers])
        if rights == len(sums):
            print("levelin nosto")
        else:
            for summa in sums:
                print("calc_id:", summa[1], "sum:", summa[2])
            print(rights, "/", len(icalc_list), "need to be:", len(icalc_list))
    else:
        print("vastattu vasta", len(sums), "/", len(icalc_list), "kysymykseen")

    # print("icalc:", icalc_list)
    # print("sums", sums)


def next_calc(id, level, game, prev_answer, pelaaja):
    icalc_list = possible_calcs(id, level, game, prev_answer)
    if icalc_list == []:
        print("level läpi, koska laskuja 0 jäljellä")
        update_user_level(pelaaja)
        return True
    else:
        random.shuffle(icalc_list)
        random_calcs = list(icalc_list[0][0:4])
        # Shuffle:
        # items = [random_calcs[1], random_calcs[2]]
        # random.shuffle(items)
        # random_calcs[1] = items[0]
        # random_calcs[2] = items[1]
        calc_id = icalc_list[0][4]
        answer = random_calcs[1] * random_calcs[2]
        # level, kertoja, kerrottava, answer, laskun id,
        return (random_calcs[0], random_calcs[1], random_calcs[2], answer, calc_id)


# laskut käyttäjälle ja levelille
def user_level_calcs(level):
    return db.session.execute(
        select(
            Level.id,
            Calc.multiplier,
            Calc.multiplicand,
            Calc.multiplier * Calc.multiplicand,
            Calc.id,
        )
        .where(Level.id == Level_Calc.level_id)
        .where(Calc.id == Level_Calc.calc_id)
        .where(User.id == Level_User.user_id)
        .where(Level.id == Level_User.level_id)
        .where(Level.id == level)
        .distinct()
    ).all()


def testi_seikkailu():
    testi = db.session.execute(
        select(Emoji.id, Emoji.emoji)
        .outerjoin(User, Emoji.id == User.emoji_id)
        .where(User.id == None)
    ).all()
    print(testi)


def levels_percent():
    percent = 10
    return percent


def create_answer():
    pass


def user_emoji(id):
    return db.session.scalar(
        select(Emoji.emoji).where(Emoji.id == User.emoji_id).where(User.id == id)
    )
