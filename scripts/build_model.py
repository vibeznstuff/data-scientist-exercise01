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
	('relationship','ship'),('marital_status','MS')]

#Assign conditional probabilities to validation data
for var, label in model_features:
	x = (var,label)
	val = prep.create_cond_probs(train,val,x)

#print(val.head())

under50_cols = [col for col in val.columns if 'False' in col]
x = pd.DataFrame(1,index=np.arange(len(val)),columns=['Under50_Score'])

for col in under50_cols:
	print(col)
	print(val[col].head())
	x = val[col]*x
print(x)




