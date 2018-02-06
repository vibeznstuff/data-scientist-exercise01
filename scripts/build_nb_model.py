import matplotlib.pyplot as plt
import pandas as pd, numpy as np
import seaborn as sns

#Import custom module with standard data prep functions
import prepare_data as prep 

#Load census data as pandas dataframe
df = prep.load_mod_census_data()

#Weights for Training, Validation, Test (% Left Over)
train_weight = 0.8
test_weight = 0.2

#Sample records for test dataset 
test_bool = np.random.rand(len(df)) < test_weight
test = df[test_bool]

#Of remaining records not in test, sample for training
#Remainder to be used as validation
t_and_v = df[~test_bool]
train_bool = np.random.rand(len(t_and_v)) < train_weight
train = t_and_v[train_bool]
val = t_and_v[~train_bool]

#Print out sample counts
print(str(len(train)) + ' records for training model')
print(str(len(val)) + ' records for validating model')
print(str(len(test)) + ' records for testing model')
print('\n')

model_features = [('age_bins','age'),('education_num_gt_12','ed_lvl'), \
	('hours_week_gt_40','hr_per_week'), ('cap_gain_gt_0','cap_gain'), \
	('sex','sex'), ('race','race'),('occupation','occup'), \
	('marital_status','MS')]
	
#Given training dataset and model features to be used,
#generate predictions for a dataset to be scored.
#test_val_flag used to indicate if scoring validation or test data
def create_predictions(model_features,train_data,test_data,test_val_flag):
	#Assign conditional probabilities to validation data
	for var, label in model_features:
		x = (var,label)
		test_data = prep.create_cond_probs(train,test_data,x)

	#Create percent frequencies for either target class
	target_probs = test_data['over_50_bool'].value_counts(normalize=True).to_dict()

	#Add target likelihoods to dataframe
	test_data['True_Likelihood'] = target_probs[True]
	test_data['False_Likelihood'] = target_probs[False]

	#Extract conditional probabilities and target likelihoods by target
	#for multiplying into each other
	under50_cols = [col for col in test_data.columns if 'False' in col]
	over50_cols = [col for col in test_data.columns if 'True' in col]
	test_data['Under50_Score'] = 1
	test_data['Over50_Score'] = 1

	# Multiply conditional probabilities under assumption
	# respondent makes less than 50k
	for col in under50_cols:
		test_data['Under50_Score'] = test_data['Under50_Score'].multiply(test_data[col],axis=0)

	# Multiply conditional probabilities under assumption
	# respondent makes over than 50k
	for col in over50_cols:
		test_data['Over50_Score'] = test_data['Over50_Score'].multiply(test_data[col],axis=0)

	#Get predictions based on final target scores
	def get_pred(row):
		if row['Under50_Score'] > row['Over50_Score']:
			return False
		else:
			return True

	#Compare predictions to actual target test_dataues
	def assess_accuracy(row):
		if row['pred'] == row['over_50_bool']:
			return 'Accurate'
		else:
			return 'Inaccurate'

	test_data['pred'] = test_data.apply(get_pred,axis=1)
	test_data['accurate'] = test_data.apply(assess_accuracy,axis=1)
	print('Model accuracy for '+test_val_flag+' set (' + str(len(test_data)) + " records):")
	print(test_data['accurate'].value_counts(normalize=True))

	#Create new csv with updated, engineered data
	test_data.to_csv('../output/'+test_val_flag+'_predictions.csv')

	#Print out validation accuracy to csv file
	test_data['accurate'].value_counts(normalize=True).to_csv('../output/'+test_val_flag+'_accuracy.csv')

#Create predictions for validation data
create_predictions(model_features,train,val,'Validation')

print("/n")

#Create predictions for test data
create_predictions(model_features,train,test,'Test')




