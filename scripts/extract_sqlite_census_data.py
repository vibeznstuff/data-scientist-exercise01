import sqlite3

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

	

