from sqlalchemy import Column, Integer, String, Float
from database import Base

# Creating variable names and their associated column names in the postgresql db
class Epa(Base):
    #Name of the table in the AWS RDS
    __tablename__ = 'epa_vehicles_all'

    barrels08 = Column('barrels08', Float)
    barrelsA08 = Column('barrelsA08', Float)
    charge120 = Column('charge120',Float)
    city08 = Column('city08', Float)
    city08U = Column('city08U', Float)
    cityCD = Column('cityCD', Float)
    cityE = Column('cityE', Float)
    cityUF = Column('cityUF', Float)
    co2 = Column('co2', Float)
    co2A = Column('co2A', Float)
    co2TailpipeAGpm = Column('co2TailpipeAGpm', Float)
    co2tailpipegpm = Column('co2tailpipegpm', Float)
    comb08 = Column('comb08', Float)
    comb08U = Column('comb08U', Float)
    combA08 = Column('combA08', Float)
    combA08U = Column('combA08U', Float)
    combE = Column('combE', Float)
    combinedCD = Column('combinedCD', Float)
    combinedUF = Column('combinedUF', Float)
    cylinders = Column('cylinders', Float)
    displ = Column('displ', Float)
    drive = Column('drive', String)
    engID = Column('engID', Float)
    eng_dscr = Column('eng_dscr', String)
    feScore = Column('feScore', Float)
    fuelCost08 = Column('fuelCost08', Float)
    fuelCostA08 = Column('fuelCostA08', Float)
    fuelType = Column('fuelType', String)
    fuelType1 = Column('fuelType1', String)
    ghgScore = Column('ghgScore', Float)
    ghgScoreA = Column('ghgScoreA', Float)
    highway08 = Column('highway08', Float)
    highway08U = Column('highway08U', Float)
    highwayA08 = Column('highwayA08', Float)
    highwayA08U = Column('highwayA08U', Float)
    highwayCD = Column('highwayCD', Float)
    highwayE = Column('highwayE', Float)
    highwayUF = Column('highwayUF', Float)
    hlv = Column('hlv', Float)
    hpv = Column('hpv', Float)
    id = Column('id', Integer, primary_key=True)
    lv2 = Column('lv2', Float)
    lv4 = Column('lv4', Float)
    make = Column('make', String)
    model = Column('model', String)
    mpgData = Column('mpgData', String)
    phevBlended = Column('phevBlended', Float)
    pv2 = Column('pv2', Float)
    pv4 = Column('pv4', Float)
    range = Column('range', Float)
    rangeCity = Column('rangeCity', Float)
    rangeCityA = Column('rangeCityA', Float)
    rangeHwy = Column('rangeHwy', Float)
    rangeHwyA = Column('rangeHwyA', Float)
    trany = Column('trany', String)
    UCity = Column('UCity', Float)
    UCityA = Column('UCityA', Float)
    UHighway = Column('UHighway', Float)
    UHighwayA = Column('UHighwayA', Float)
    VClass = Column('VClass', String)
    year = Column('year', Float)
    youSaveSpend = Column('youSaveSpend', Float)
    guzzler = Column('guzzler', String)
    trans_dscr = Column('trans_dscr', String)
    tCharger = Column('tCharger', String)
    sCharger = Column('sCharger', String)
    atvType = Column('atvType', String)
    fuelType2 = Column('fuelType2', String)
    rangeA = Column('rangeA', String)
    evMotor = Column('evMotor', String)
    mfrCode = Column('mfrCode', String)
    c240Dscr = Column('c240Dscr', String)
    charge240b = Column('charge240b', Float)
    c240bDscr = Column('c240bDscr', String)
    createdOn = Column('createdOn', String)
    modifiedOn = Column('modifiedOn', String)
    startStop = Column('startStop', String)
    phevCity = Column('phevCity', Float)
    phevHwy = Column('phevHwy', Float)
    phevComb = Column('phevComb', Float)