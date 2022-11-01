from flask import (Blueprint, render_template, redirect)
import os
import sqlite3
from datetime import datetime
from app.forms import AppointmentForm

bp = Blueprint("main", __name__, url_prefix="/")
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily():
    form = AppointmentForm()
    if form.validate_on_submit():
        print("test")
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute('''INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
            VALUES (:name, :start_datetime, :end_datetime, :description, :private)''', {
                'name': form.name.data,
                'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
                'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
                'description': form.description.data,
                'private': form.private.data})
            conn.commit()
            return redirect('/')
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")

        rows = curs.fetchall()
        appointments = []
        for apps in rows:
            dic = {}
            dic["name"] = apps[1]
            dic['start'] = datetime.strptime(apps[2], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")
            dic['end'] = datetime.strptime(apps[3], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")
            appointments.append(dic)
            # datetime_str1 = apps[2]
            # datetime_str2 = apps[3]
            # datetime_obj1 = datetime.strptime(datetime_str1,  '%Y-%m-%d %H:%M:%S')
            # datetime_obj2 = datetime.strptime(datetime_str2,  '%Y-%m-%d %H:%M:%S')
            # start.append(datetime_obj1.strftime("%H:%M"))
            # end.append(datetime_obj2.strftime("%H:%M"))
        print(rows)
    return render_template('main.html', rows=appointments, form=form)
