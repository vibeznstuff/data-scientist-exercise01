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

model_features = [('age_bins','age'),('education_num_gt_12','ed_lvl'), \
	('hours_week_gt_40','hr_per_week'), ('cap_gain_gt_0','cap_gain'), \
	('sex','sex'), ('race','race'),('occupation','occup'), \
	('marital_status','MS')]

#Assign conditional probabilities to validation data
for var, label in model_features:
	x = (var,label)
	val = prep.create_cond_probs(train,val,x)


under50_cols = [col for col in val.columns if 'False' in col]
over50_cols = [col for col in val.columns if 'True' in col]
val['Under50_Score'] = 1
val['Over50_Score'] = 1

for col in under50_cols:
	val['Under50_Score'] = val['Under50_Score'].multiply(val[col],axis=0)
	
for col in over50_cols:
	val['Over50_Score'] = val['Over50_Score'].multiply(val[col],axis=0)

def get_pred(row):
	if row['Under50_Score'] > row['Over50_Score']:
		return 'False'
	else:
		return 'True'
			
def assess_accuracy(row):
	if row['pred'] == row['over_50_bool']:
		return 'False'
	else:
		return 'True'
			
val['pred'] = val.apply(get_pred,axis=1)
print(val['pred'].head())

val['accurate'] = val.apply(assess_accuracy,axis=1)
print(val['accurate'].value_counts())





