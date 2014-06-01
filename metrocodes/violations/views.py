from collections import defaultdict
import json

from flask import (Blueprint, request, render_template, flash, g, session,
        redirect, url_for, json, jsonify, current_app)

from sqlalchemy import func
from sqlalchemy.sql import label

from metrocodes import db
from metrocodes.violations.models import Violation

mod = Blueprint('violations', __name__, url_prefix='/violations')


@mod.route('/', methods=['GET', ])
def violations():
    violations = db.session.query(Violation).order_by(
        'date_recieved desc',
    ).all()
    violation_list = []
    for violation in violations[0:100]:
        violation_list.append(violation.to_dict())
    return json.dumps(violation_list)

@mod.route('/thing', methods=['GET', ])
def thing():
    violations = db.session.query(
        Violation.reported_problem,
        label('year', func.date_part('year', Violation.date_recieved)),
        label('month', func.date_part('month', Violation.date_recieved)),
        label('count', func.count(Violation.id))
    ).group_by(
        func.date_part('year', Violation.date_recieved),
        func.date_part('month', Violation.date_recieved),
        Violation.reported_problem
    ).order_by(
        'year desc',
        'month desc',
        'count desc'
    ).all()

    months = []
    series = defaultdict(dict)
    previous_month = None
    violation_types = set([])
    prep_agg = defaultdict(list)
    prep_series = []

    for violation in violations:
        month = '{}-{}'.format(int(violation.year), int(violation.month))
        if not month == previous_month:
            months.append(month)
        previous_month = month
        violation_types.add(violation.reported_problem)
        series[month][violation.reported_problem] = violation.count

    for month in months[0:1]:
        for violation_type in violation_types:
            if series[month].get(violation_type):
                prep_agg[violation_type].append(series[month][violation_type])
            else:
                prep_agg[violation_type].append(0)

    for key in prep_agg:
        prep_series.append({'name': key, 'data': prep_agg[key]})

    months = json.dumps(months)
    series = json.dumps(prep_series)
    return render_template('violations/index.html', months=months, series=series)

@mod.route('/start', methods=['GET', ])
def start():
    violations = db.session.query(
        Violation.reported_problem,
        label('year', func.date_part('year', Violation.date_recieved)),
        label('month', func.date_part('month', Violation.date_recieved)),
        label('count', func.count(Violation.id))
    ).group_by(
        func.date_part('year', Violation.date_recieved),
        func.date_part('month', Violation.date_recieved),
        Violation.reported_problem
    ).order_by(
        'year desc',
        'month desc',
        'count desc'
    ).all()

    months = []
    series = defaultdict(dict)
    previous_month = None
    violation_types = set([])
    prep_agg = defaultdict(list)
    prep_series = []

    for violation in violations:
        month = '{}-{}'.format(int(violation.year), int(violation.month))
        if not month == previous_month:
            months.append(month)
        previous_month = month
        violation_types.add(violation.reported_problem)
        series[month][violation.reported_problem] = violation.count

    for month in months[0:6]:
        for violation_type in violation_types:
            if series[month].get(violation_type):
                prep_agg[violation_type].append(series[month][violation_type])
            else:
                prep_agg[violation_type].append(0)

    for key in prep_agg:
        prep_series.append({'name': key, 'data': prep_agg[key]})

    months = json.dumps(months)
    series = json.dumps(prep_series)
    return render_template('index.html', months=months, series=series)
