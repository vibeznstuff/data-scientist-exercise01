Select
	a.id as respondent_id,
	age,
	b.name as workclass,
	c.name as education_level,
	education_num,
	d.name as marital_status,
	e.name as occupation,
	f.name as relationship,
	g.name as race,
	h.name as sex,
	capital_gain,
	capital_loss,
	hours_week,
	i.name as country,
	over_50k
From records a
Left Join workclasses b
	On a.workclass_id = b.id
Left Join education_levels c
	On a.education_level_id = c.id
Left Join marital_statuses d
	On a.marital_status_id = d.id
Left Join occupations e
	On a.occupation_id = e.id
Left Join relationships f
	On a.relationship_id = f.id
Left Join races g
	On a.race_id = g.id
Left Join sexes h
	On a.sex_id = h.id
Left Join countries i
	On a.country_id = i.id;