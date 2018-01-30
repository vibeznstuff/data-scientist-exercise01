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
validation = t_and_v[~train_bool]

#Print out sample counts
print(str(len(train)) + ' records for training model')
print(str(len(validation)) + ' records for validating model')
print(str(len(test)) + ' records for testing model')

age_prob = pd.crosstab(train.age_bins,train.over_50_bool).apply(lambda r: r/r.sum(),axis=1)

print(age_prob)
prob_dict = {}
prob_dict['age_bins']={}
prob_dict['age_bins']['False']={}
prob_dict['age_bins']['True']={}

#Populate dictionary of probabilities
for i,row in age_prob.iterrows():
	prob_dict['age_bins']['False'][i]=round(row[0],4)
	prob_dict['age_bins']['True'][i]=round(row[1],4)
print(prob_dict)



