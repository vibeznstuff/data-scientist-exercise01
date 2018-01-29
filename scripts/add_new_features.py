import matplotlib.pyplot as plt
import seaborn as sns

#Import custom module with standard data prep functions
import prepare_data as prep 

#Load census data as pandas dataframe
df = prep.load_census_data()

#Function to convert variable into a boolean (string)
def bool_my_feature(row,in_var,threshold):
	if row[in_var] > threshold:
		return 'True'
	elif row[in_var] <= threshold:
		return 'False' 
	else:
		return np.NaN

#Function to categorize numeric variable into bins
def bin_my_feature(row,in_var):
	pass
		
#Create categorical version of target variable
df['cap_gain_gt_0'] = df.apply(bool_my_feature, args=('capital_gain',0),axis=1)
df['education_num_gt_12'] = df.apply(bool_my_feature, args=('education_num',12),axis=1)
df['hours_week_gt_40'] = df.apply(bool_my_feature, args=('hours_week',40),axis=1)

print(df['cap_gain_gt_0'].value_counts())
print(df['education_num_gt_12'].value_counts())
print(df['hours_week_gt_40'].value_counts())

new_cat_features = ['cap_gain_gt_0','education_num_gt_12','hours_week_gt_40']

#Generate plots for new features to assess information gain
for cat_var in new_cat_features:
	f, ax = plt.subplots(figsize=(12,12))
	plt.title(cat_var+' frequencies')
	sns.countplot(x=cat_var, hue="over_50_bool", data=df)
	plt.savefig('../output/figs/by_over50k/'+cat_var+'_by_over50k.png', bbox_inches='tight')
	plt.close()