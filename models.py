# models.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    address = Column(String)
    region = Column(Integer)
    memari_number = Column(String)
    utm_x = Column(Float)
    utm_y = Column(Float)
    sabti_code = Column(String)
    last_modified = Column(Date)

    has_permit = Column(Boolean)
    permit_usage = Column(String)
    permit_occupancy = Column(Float)
    permit_floors = Column(Integer)
    permit_density = Column(Float)
    widening_area = Column(Float)

    has_finalization = Column(Boolean)
    final_total_area = Column(Float)
    final_current_usage = Column(String)
    final_floors = Column(Integer)
    final_approved_usage = Column(String)
    final_current_occupancy = Column(Float)
    final_approved_occupancy = Column(Float)

    has_komission = Column(Boolean)
    komission_roof_no = Column(String)
    komission_roof_area = Column(Float)
    komission_structure_type = Column(String)
    komission_current_usage = Column(String)
    komission_occupancy = Column(Float)
    komission_density = Column(Float)
    komission_zone = Column(String)
    komission_verdict = Column(String)
    komission_description = Column(Text)
    komission_report_date = Column(Date)
    komission_sent_date = Column(Date)

    has_no_conflict_cert = Column(Boolean)
    cert_date = Column(Date)
    cert_area = Column(Float)
    cert_floors = Column(Integer)
    cert_parking = Column(Integer)
    cert_usage = Column(String)

    has_architectural = Column(Boolean, default=False)
    architectural_data = Column(Text)
    architectural_last_modified = Column(Date)

    # Comment out the following lines for building and HSE standards
    # has_building = Column(Boolean, default=False)
    # building_data = Column(Text)
    # building_last_modified = Column(Date)

    # has_hse = Column(Boolean, default=False)
    # hse_data = Column(Text)
    # hse_last_modified = Column(Date)