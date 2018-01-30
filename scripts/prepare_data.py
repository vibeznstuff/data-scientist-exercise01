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
	
#Load modified census data after data cleaning and feature engineering steps
def load_mod_census_data():
	#Import flattened CSV census data into dataframe
	df = pd.read_csv('../output/engineered_census_data.csv')
	return df
	
#Function to convert variable into a boolean (string)
def bool_my_feature(row,in_var,threshold):
	if row[in_var] > threshold:
		return 'True'
	elif row[in_var] <= threshold:
		return 'False' 
	else:
		return np.NaN

#Function to categorize numeric variable into bins
def bin_my_feature(row,in_var,bin_list):
	bin_list.sort() #Just in case
	out_label = np.NaN #If field doesn't match any bins
	n = len(bin_list)-1 #Max index
	for i in list(range(0,n+1)):
		if i < n:
			#Lower and upper ends of bin
			x,y = bin_list[i:i+2] 
		if i == 0 and row[in_var] <= bin_list[i]:
			#Value is less than min bin value
			out_label = '<=' + str(bin_list[i])
		elif i == n and row[in_var] >= bin_list[i]:
			#Value is greater than max bin value
			out_label = '>=' + str(bin_list[i])
		elif i < n and row[in_var] >= x and row[in_var] < y:
			out_label = str(x) + ' - ' + str(y)
	return out_label
	


