import pickle
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process
from joblib import load
import requests
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from sqlalchemy.sql import func

#SQLAlchemy
# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html#accessing-the-metadata
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Load in slimmed random forest pickled model
test_model = load("targetrobustforest.joblib")

# Load the craigslist cleaned data
df_cl = pd.read_csv("data/model_and_image_url_lookup.csv")
# List of unique CL cars
cl_models = sorted(df_cl.model.unique())

class Pred:
    '''    
    Instance of our predition, represented as a Class

    '''
    def __init__(
        self, 
        miles_per_year: int = 15000,
        num_years: int = 5,
        gas_cost: int = 3,
        electrical_cost: float = 0.12,
        maintenance_cost_per_year: int = 1000,
        make: str='Ford',
        model: str='F150 Pickup 4WD',
        year: int=2005,
        odometer: int=99999):

        self.miles = miles_per_year
        self.years = num_years
        self.gas = gas_cost
        self.electrical = electrical_cost
        self.maint = maintenance_cost_per_year
        self.make = make
        self.model = model
        self.year = year
        self.manufacturer = make.lower()
        self.model_lower = model.lower()
        self.co2 = None
        self.model_fz = process.extractOne(self.model_lower, cl_models, scorer=fuzz.token_sort_ratio)[0] 
        self.odometer = odometer
        self.fire = "\N{fire}"
        self.tree = "\N{evergreen tree}"
        self.maint_5yr = self.maint*5
        

    def get_car_pred(self):

        input = pd.DataFrame({
        "year": [self.year],
        "manufacturer": [self.manufacturer],
        "model": [self.model_fz]
        })

        pred = test_model.predict(input)
        return pred[0]
    
    def get_comb_mpg(self):
        """Get the combined mpg using ORM"""
        return db.query(func.avg(models.Epa.comb08)\
        .filter(
            models.Epa.make==self.make, 
            models.Epa.model==self.model,
            models.Epa.year==self.year))\
                .all()[0][0]

    def get_comb_co2(self):
        """Get the combbined co2 using ORM"""
        return db.query(func.avg(models.Epa.co2tailpipegpm)\
            .filter(
            models.Epa.make==self.make, 
            models.Epa.model==self.model,
            models.Epa.year==self.year))\
                .all()[0][0]

    def co2_num_years(self):
        """CO2 over a X year period (Kg)"""
        self.co2 = self.get_comb_co2()
        total = self.co2 * self.miles * self.years/1000
        return total

    def get_fuel_cost(self):
        """5 year fuel cost"""
        return self.miles/ self.get_comb_mpg() * self.gas * self.years

    def cto(self):
        """Get 5 year cost to own"""
        cto = self.get_fuel_cost() + self.maint_5yr + self.get_car_pred()
        return cto

    def co2_offset(self):
        """How many trees to offset co2 emissions"""
        ## Number of kgs of CO2 absorbed by one tree per year
        tree_absorption = 21.7724
        return self.co2_num_years()/(tree_absorption * self.years)
    
    def emoji(self):
        """graphically represent CO2 emissions as emoji"""
        offset = int(round(self.co2_offset(), 0))
        fire_e = offset//100 
        tree_e = 10 - fire_e
        fire_total = self.fire * fire_e
        tree_total = self.tree * tree_e
        ft = fire_total + tree_total
        emoji_graph = [ft for x in range(5)]
        return emoji_graph

    #### Images of Selected Car

    def year_to_urls(self):
        """
        input cl car and year, output a list of working urls
        """
        df_models = df_cl[df_cl['model'] == self.model_fz]
        df_models_at_year = df_models[df_models['year'] == self.year]
        index_of_model_year = df_models_at_year.index[0:4]

        list_urls = list(df_cl['image_url'][index_of_model_year])
        list_w_nan = [self.status_200_or_nan(x) for x in list_urls]
        clean_list_urls = [x for x in list_w_nan if x is not np.NaN]
        return clean_list_urls

    def fetch_img(self):
        """
        Create a list that contains only valid URLs.
        If there are no good images, check years before and ahead for images to return.
        """
        clean_list_urls = self.year_to_urls()
        #if list empty, check other years
        if len(clean_list_urls) == 0:
            self.year = self.year + 1
            clean_list_urls = self.year_to_urls()

            if len(clean_list_urls) == 0:
                self.year = self.year - 2
                clean_list_urls = self.year_to_urls()

                # no car image
                if len(clean_list_urls) == 0:
                    return ['https://raw.githubusercontent.com/Lambda-School-Labs/street-smarts-ds/master/data/noImage_large.png']
                return clean_list_urls
            return clean_list_urls
        return clean_list_urls
    
    def status_200_or_nan(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            return np.NaN