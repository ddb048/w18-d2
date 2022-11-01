from flask import (Blueprint, render_template)
import os
import sqlite3
import datetime

bp = Blueprint("main", __name__, url_prefix="/")
DB_FILE = os.environ.get("DB_FILE")

@bp.route('/')
def main():
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")
        rows = curs.fetchall()
        start = []
        end = []
        for apps in rows:
            datetime_str1 = apps[2]
            datetime_str2 = apps[3]
            datetime_obj1 = datetime.strptime(datetime_str1,  '%Y-%m-%d %H:%M:%S')
            datetime_obj2 = datetime.strptime(datetime_str2,  '%Y-%m-%d %H:%M:%S')
            start.append(datetime_obj1.strftime("%H:%M"))
            end.append(datetime_obj2.strftime("%H:%M"))
        print(rows)
    return render_template('main.html', rows=rows, start=start, end=end)
