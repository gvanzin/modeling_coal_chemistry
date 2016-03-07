import pandas as pd
import graphlab as gl
import matplotlib.pyplot as plt

def load_data():
	'''load th dataset into pandas, 
		process with process_data function'''

	metadata=pd.read_csv('/Users/garyvanzin/Downloads/CQ2016224225640.CSV')
	prox_ult=pd.read_csv('/Users/garyvanzin/Downloads/CQ2016224222514/CQ2016224222514.CSV')
	elements=pd.read_csv('/Users/garyvanzin/Downloads/CQ2016224224425.CSV')
	return metadata, prox_ult, elements

def clean(df):
	cols = df.columns
	cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str, unicode)) else x)
	df.columns = cols
	cols = df.columns
	cols = cols.map(lambda x: x.lstrip('_') if isinstance(x, (str, unicode)) else x)
	df.columns = cols
	df=df[:-1]
	return df

def drop_columns_prox_ult(prox_ult):
	colsToDrop=prox_ult.columns[[2,4,6,8,11,13,15,17,19,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58]]
	prox_ult.drop(colsToDrop, axis=1, inplace=True)
	prox_ult=prox_ult[prox_ult['Proximate_Validation']=='Acceptable']
	return prox_ult

def drop_column_elements(elements):
	e=range(2,149,2)
	elements.drop(elements.columns[e], axis=1, inplace=True)
	elements.drop('Strat', axis=1, inplace=True)
	cols2change=['Si', 'Al', 'Ca', 'Mg', 'K', 'Fe', 'Ti', 'Ag', 'As', 'Au', 'Na', 'Ba', 'Be', 'Bi', 'TS', 'B']
	elements[cols2change]=elements[cols2change].astype(float)
	return elements

def drop_columns_metadata(metadata):
	metadata.drop(['Analytical_Lab','Submit_Date','Collector', 'Drill_Core_No', 'Analysis_Type', 'Township', 'Range', 'Section', 'Quarters', 'Tract', 'Location_Detail', 'Strat', 'Comments', 'Literature', 'Series/Epoch', 'Coal_Zone', 'Field', 'District', 'Group', 'Member'], axis=1, inplace=True)
	return metadata

def balance_rows_and_cols(df):
	num_cols=[]
	num_rows=[]
	df2=df[:]
	r=range(len(df),99,-100)
	for i in r:
		df=df2[:]
		el=df.isnull().sum(axis=0)
		el=el [el < i]
		df=df[el.index]
		num_cols.append(len(df.columns))
		df=df.dropna()
		num_rows.append(len(df))
	z=zip(num_cols, num_rows, r)
	df_DF=pd.DataFrame(z,columns=['num_cols','num_rows','r'] )
	return df_DF



def plot_balance(df_DF):
	df_DF=df_DF.groupby(['num_cols','num_rows'])
	df_DF2=df_DF.first()
	df_DF2=df_DF2.reset_index()
	x=df_DF2['num_cols']
	y=df_DF2['num_rows']
	z=df_DF2['r']
	fig, ax = plt.subplots()
	ax.plot(x, y, 'bo-')
	for X, Y, Z in zip(x, y, z):
	    # Annotate the points 5 _points_ above and to the left of the vertex
	    ax.annotate('{}'.format(Z), xy=(X,Y), xytext=(-5, 5), ha='right',
	                textcoords='offset points')


if __name__ == '__main__':
	metadata, prox_ult, elements = load_data()
