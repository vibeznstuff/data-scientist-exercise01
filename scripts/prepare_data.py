import pandas as pd, numpy as np
import sqlite3

#Import Census data from provided SQLite database
def download_census_data():
	#Connect to local database with census data
	conn = sqlite3.connect('../exercise01.sqlite')
	c = conn.cursor()

	#Load SQL code for extracting flattened data
	sql = open('../sql/rti_census_extract.sql','r').read()

	#Open new outfile...
	with open('../output/flattened_census_data.csv','w+') as out_file:
		#Add column headers to csv
		out_file.write('respondent_id,age,workclass,education_level,education_num,' +
			'marital_status,occupation,relationship,race,sex,capital_gain,'+
			'capital_loss,hours_week,country,over_50k\n')
		#Execute SQL script and begin writing to out_file
		for row in c.execute(sql):
			record = ",".join([str(i) for i in row])
			out_file.write(record+"\n")
	out_file.close()
	
#Load Census CSV data into a pandas dataframe
def load_census_data():
	#Import flattened CSV census data into dataframe
	df = pd.read_csv('../output/flattened_census_data.csv')

	#Function to convert target from numeric to categorical
	def cat_target(row):
		if row['over_50k'] == 0:
			return 'False'
		elif row['over_50k'] == 1:
			return 'True' 
		else:
			return np.NaN
	
	#Create categorical version of target variable
	df['over_50_bool'] = df.apply(cat_target, axis=1)
	return df
	


