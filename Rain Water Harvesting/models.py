from geoalchemy2 import Geometry
from database import db

class AquiferMaterial(db.Model):
    __tablename__ = 'aquifer_materials'
    id = db.Column(db.Integer, primary_key=True)
    name_of_st = db.Column(db.String(255))  # State name
    type_of_aq = db.Column(db.String(255))  # Aquifer type
    st_area_sh = db.Column(db.Float)  # Area
    st_length_ = db.Column(db.Float)  # Length
    geometry = db.Column(Geometry('MULTIPOLYGON', srid=4326), nullable=False)

class MajorAquifer(db.Model):
    __tablename__ = 'major_aquifers'
    id = db.Column(db.Integer, primary_key=True)
    newcode14 = db.Column(db.String(10))
    aquifer = db.Column(db.String(255))
    newcode43 = db.Column(db.String(10))
    aquifer0 = db.Column(db.String(255))
    system = db.Column(db.String(100))
    aquifers = db.Column(db.String(255))
    zone_m = db.Column(db.String(50))
    mbgl = db.Column(db.Float)  # Meters below ground level
    avg_mbgl = db.Column(db.Float)  # Average MBGL
    m2_perday = db.Column(db.Float)  # Hydraulic conductivity m²/day
    m3_per_day = db.Column(db.Float)  # Transmissivity m³/day
    yeild__ = db.Column(db.Float)  # Yield
    per_cm = db.Column(db.Float)  # Specific yield per cm
    state = db.Column(db.String(100))
    pa_order = db.Column(db.Integer)
    test = db.Column(db.String(50))
    area_re = db.Column(db.Float)
    st_area_sh = db.Column(db.Float)
    st_length_ = db.Column(db.Float)
    geometry = db.Column(Geometry('MULTIPOLYGON', srid=4326), nullable=False)

# You can add more models here for other data layers like soil type, rainfall, etc.
# For example:
#
# class Soil(db.Model):
#     __tablename__ = 'soils'
#     id = db.Column(db.Integer, primary_key=True)
#     soil_type = db.Column(db.String(255), nullable=False)
#     geometry = db.Column(Geometry('MULTIPOLYGON', srid=4326), nullable=False)
