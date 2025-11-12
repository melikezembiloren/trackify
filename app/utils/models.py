from app.extensions import db
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.utils.now_utc import Now
import enum

now_utc = Now.now_utc()


# --- Enums ---
class DefectStatus(enum.Enum):
    REWORK = "REWORK"   # Düzeltme süreci devam ediyor
    OK = "OK"           # Rework tamamlandı ve kontrol edildi
    CLOSED = "CLOSED"   # Hata tamamen kapandı
    SCRAP = "SCRAP"     # TV hurda, rework yapılmayacak

class DefectEventType(enum.Enum):
    FOUND = "FOUND"
    CAUSED = "CAUSED"
    REWORK_START = "REWORK_START"
    REWORK_DONE = "REWORK_DONE"
    QC_VERIFY = "QC_VERIFY"
    REOPEN = "REOPEN"
    CLOSED = "CLOSED"
    SCRAP = "SCRAP"

#user for admins
class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique = True, nullable = False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    password_hash = Column(String(300), nullable=False)
    title = Column(String(65), nullable=False)

#user for operators
class Operators(db.Model):
    __tablename__ = 'operator'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    pin_code = Column(String(6), nullable=False, unique= True)

    found_defects = relationship("Defect", back_populates="found_by", foreign_keys='Defect.found_by_id')
    caused_defects = relationship("Defect", back_populates="caused_by", foreign_keys='Defect.caused_by_id')
    reworked_defects = relationship("Defect", back_populates="rework_by", foreign_keys='Defect.rework_by_id')


# lines 
class Lines(db.Model):
    __tablename__ = 'line'

    id = Column(Integer, primary_key=True)
    line = Column(String(20), nullable=False)
    line_name = Column(String(20), nullable=False)
    line_password_hash = Column(String(300), nullable=False)
    daily_target = Column(Integer, default=0)
    weekly_target = Column(Integer, default=0)
    monthly_target = Column(Integer, default=0)

    tvs = relationship('TV', back_populates='line')
    defects = relationship('Defect' ,  back_populates='line')


#product catalogues
class TvCatalog(db.Model):
    __tablename__ = 'tv_catalog'

    id = Column(Integer, primary_key=True)
    model_name = Column(String(50), nullable=False)
    barcode_prefix = Column(String(20), nullable=False, unique=True)  # barcode başlangıcı veya tam barcode

    tvs = relationship('TV', back_populates='catalog')

# TV
class TV(db.Model):
    __tablename__= 'tv'

    id = Column(Integer, primary_key=True)
    tv_seri_no = Column(String(100), nullable=False)
    line_id = Column(Integer, ForeignKey('line.id'))
    catalog_id = Column(Integer, ForeignKey('tv_catalog.id'))

    created_at = Column(DateTime(timezone=True), default=now_utc)
    updated_at = Column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)

    # relationships
    line = relationship('Lines', back_populates='tvs')   # <--- Lines yerine Line
    defect = relationship('Defect', back_populates='tv')
    catalog = relationship('TvCatalog', back_populates='tvs')


#catalog of defects
class DefectCatalog(db.Model):
    __tablename__ = 'defect_catalog'

    id = Column(Integer, primary_key=True)
    defect_code = Column(String(10), nullable=False)
    defect_name = Column(String(100), nullable=False)
    defect_description = Column(String(150), nullable=False)
    defect_type = Column(String(50), nullable=False)

    solutions = relationship("DefectSolution", back_populates="defect_catalog", cascade="all, delete-orphan")

class DefectSolution(db.Model):
    __tablename__ = 'defect_solution'

    id = Column(Integer, primary_key=True) 
    solution_name = Column(String(300), nullable=True)
    defect_catalog_id = Column(Integer, ForeignKey('defect_catalog.id'))
    

    defect_catalog = relationship("DefectCatalog", back_populates="solutions")



# defect records
class Defect(db.Model):

    __tablename__ = 'defect'

    id = Column(Integer, primary_key=True)
    tv_id = Column(Integer, ForeignKey('tv.id'), nullable=False)
    defect_catalog_id = Column(Integer, ForeignKey('defect_catalog.id'))
    created_at = Column(DateTime(timezone=True), default=lambda: now_utc(), nullable=False )
    solution_text = Column(String(300), nullable=True)
    line_id = Column(Integer, ForeignKey('line.id'), nullable=False)

    status = Column(String(20), default="REWORK", nullable=False, index=True)
    applied_solution_id = Column(Integer, ForeignKey('defect_solution.id'), nullable=True)


    #related operators
    found_by_id = Column(Integer, ForeignKey('operator.id'))
    caused_by_id = Column(Integer, ForeignKey('operator.id'))
    rework_by_id = Column(Integer, ForeignKey('operator.id'))


    # Relationships
    line = relationship('Lines', back_populates='defects')
    tv = relationship('TV', back_populates='defect')
    defect_catalog = relationship('DefectCatalog')
    applied_solution = relationship('DefectSolution')
    found_by = relationship("Operators", foreign_keys=[found_by_id], back_populates="found_defects")
    caused_by = relationship("Operators", foreign_keys=[caused_by_id], back_populates="caused_defects")
    rework_by = relationship("Operators", foreign_keys=[rework_by_id], back_populates="reworked_defects")

    history = relationship("DefectHistory", back_populates="defect", cascade="all, delete-orphan", order_by="DefectHistory.created_at")

# --- Defect History (audit / workflow events) ---
class DefectHistory(db.Model):
    __tablename__ = 'defect_history'

    id = Column(Integer, primary_key=True)
    defect_id = Column(Integer, ForeignKey('defect.id'), nullable=False, index=True)
    operator_id = Column(Integer, ForeignKey('operator.id'), nullable=False)
    event_type = Column(String(20), nullable=False)
    commit = Column(Text, nullable=True)
    solution_text = Column(String(300), nullable=True)
    applied_solution_id = Column(Integer, ForeignKey('defect_solution.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False, index=True)

    operator = relationship("Operators")
    defect = relationship("Defect", back_populates="history")
    applied_solution = relationship("DefectSolution")




