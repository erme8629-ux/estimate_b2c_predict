import os
import pickle
import numpy as np
import pandas as pd
from functools import partial
from autobiz_utility_functions.db.connection import DBconf, DBconn
from estimate_b2c_predict import config
import time
import joblib
import xgboost as xgb
from datetime import datetime
import tarfile 
import xgboost as xgb
import io
import tempfile

def call_estimate_b2c(input_data):

	if isinstance(input_data,list):
		country = input_data[0].get('country',None)
	else:
		country = input_data.get('country',None)

	dbconf = DBconf(country=country, application=config.application, server_exec=config.server_exec)
	
	with DBconn(dbconf=dbconf) as dbconn:
		connection,cursor=dbconn.get_conn()
		start= datetime.now()
		output = []
		
		if isinstance(input_data,list):

			country = np.array([d["country"] for d in input_data])
			date = np.array([d["date"] for d in input_data])
			ID = np.array([d["ID"] for d in input_data])
			age = np.array([d["age"] for d in input_data])
			km = np.array([d["km"] for d in input_data])

			vectorized_b2c = np.vectorize(estimate_b2c)
			results = vectorized_b2c(country, date, ID, age, km)
			output.append(results)
			
		else:
			results = estimate_b2c(country, date, ID, age, km)
			output.append(results)
			

		print(output)
		time = (datetime.now() - start).total_seconds() 
		print(time)	
		return output
	
TAR_CACHE = {}
MODEL_CACHE = {}

def load_tar_once(tar_path):
	if tar_path in TAR_CACHE:
		return TAR_CACHE[tar_path]

	extracted = {}
	with tarfile.open(tar_path, "r:gz") as tar:
		for member in tar.getmembers():
			if member.isfile():
				extracted[os.path.basename(member.name)] = tar.extractfile(member).read()

	TAR_CACHE[tar_path] = extracted
	return extracted


def load_model_cached(model_id, file_data):
	if model_id not in MODEL_CACHE:
		model = xgb.XGBRegressor()
		model.load_model(bytearray(file_data))
		MODEL_CACHE[model_id] = model
	return MODEL_CACHE[model_id]

		
def estimate_b2c(country, date, ID, age, km):
	

	output={}
	output['country']=country
	output['date']=date
	output['ID']=ID
	output['age']=age
	output['km']=km

	dbconf = DBconf(country=country, application=config.application, server_exec=config.server_exec)
	db, country, country_code = dbconf.db, dbconf.country, dbconf.country_code
	
	if country not in config.country_list:
		print("Error country not in country list")
		print(config.country_list)
		sys.exit(0)

	input_path = config.model["output_path"]
	input_path = input_path+country+'/'+date+'/'

	if any(char.isalpha() for char in ID):
		base_path = input_path+config.model["output_MCCLBP"]
		

	else:
		base_path = input_path+config.model["output_REF"]
		

	tar_path = base_path + config.model["output_tar"]

	
	files = load_tar_once(tar_path)

	target_filename = ID + ".ubj"
	if target_filename not in files:
		raise FileNotFoundError(f"Model {target_filename} not found in tar")

	file_data = files[target_filename]

	model = load_model_cached(ID, file_data)

	X = pd.DataFrame({"age": [age], "km": [km]})
	pred = model.predict(X)[0]

	output["b2c"] = float(pred)
	
	return output

