import pickle
import numpy as np
import os
###########
# general #
###########

config_path='config/'
config_country_name='config_country'
config_db_name='config_db'

country_dict = pickle.load(open(config_path+config_country_name+'.pkl', 'rb'))
country_list = country_dict['country_list']
country_list_daily = country_dict['country_list_daily']
country_list_monthly = country_dict['country_list_monthly']

application = 'AUTOBIZ'
server_exec = 'PROD_DATA'
if os.path.isfile(config_path+'/'+config_db_name+'.pkl'):
	config_db=pickle.load(open(config_path+'/'+config_db_name+'.pkl', 'rb'))
	application=config_db['application']
	server_exec=config_db['server_exec']

log_path='log/'


model={}
model["output_path"]="model/"
model["model_filename"]="model"
model["output_tar"] = "models_compressed.tar.gz"
model["output_REF"]="REF/"
model["output_MCCLBP"]="MCCLBP/"



output = {}
