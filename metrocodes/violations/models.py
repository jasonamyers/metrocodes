from datetime import datetime
from dateutil.parser import parse as date_parser

from metrocodes import db

fields = {
    'Reported Problem': 'reported_problem',
    'City': 'city',
    'Complaint Source': 'complaint_source',
    'Last Activity Date': 'last_activity_date',
    'ZIP': 'zip_code',
    'Date Received': 'date_recieved',
    'Request #': 'request_number',
    'Last Activity': 'last_activity',
    'Status': 'status',
    'Property APN': 'property_apn',
    'State': 'state',
    'Property Address': 'property_address',
    'Property Owner': 'property_owner',
    'Mapped Location': 'mapped_location',
    'Council District': 'council_district'
}


class Violation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    request_number = db.Column(db.String(), nullable=True)
    date_recieved = db.Column(db.DateTime(), nullable=True)
    property_apn = db.Column(db.String(), nullable=True)
    property_address = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=True)
    state = db.Column(db.String(), nullable=True)
    zip_code = db.Column(db.String(), nullable=True)
    property_owner = db.Column(db.String(), nullable=True)
    complaint_source = db.Column(db.String(), nullable=True)
    reported_problem = db.Column(db.String(), nullable=True)
    status = db.Column(db.String(), nullable=True)
    council_district = db.Column(db.String(), nullable=True)
    last_activity_date = db.Column(db.DateTime(), nullable=True)
    last_activity = db.Column(db.String(), nullable=True)
    mapped_location = db.Column(db.String(), nullable=True)

    
    def to_dict(self):
        base_dict = {}
        for field in fields.values():
            if 'date' in field:
                date_field = getattr(self, field)
                if date_field:
                    base_dict[field] = date_field.strftime('%b %d, %Y')
                else:
                    base_dict[field] = ''
            else:
                base_dict[field] = getattr(self, field)
        return base_dict

    @classmethod
    def by_id(cls, violation_id):
        return db.session.query(Violation).filter(Violation.id == violation_id).first()

    @classmethod
    def reload_csv(cls, filename):
        db.session.query(Violation).delete()
        db.session.commit()
        import csv
        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                violation = Violation()
                for key in row.keys():
                    if 'Date' in key:
                        if row[key]:
                            date_time = date_parser(row[key])
                        else:
                            date_time = None
                        setattr(violation, fields[key], date_time)
                    else:
                        setattr(violation, fields[key], row[key])
                db.session.add(violation)
                db.session.commit()
        return True
        
