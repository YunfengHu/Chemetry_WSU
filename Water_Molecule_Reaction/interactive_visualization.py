import pandas as pd 
import plotly
import os
import plotly.graph_objs as go


path = '/home/yunfeng/Downloads/Clark_project/Result_20171218/'
os.chdir(path)
extension = '.csv'
files = os.listdir(path)
files = [file for file in files if extension in file]
saveFiles = [file.replace('.csv', '.html') for file in files]


for file, savefile in zip(files, saveFiles):
	df = pd.read_csv(path + file)
	# figure1 = plotly.tools.make_subplots(rows=1, cols=1)
	data = []
	orders = df['Order'].unique()
	for order in orders:
		dfTempt = df[df['Order'] == order]
		trace1 = plotly.graph_objs.Scatter(
						y=dfTempt['distanceToCenters'], 
						x=dfTempt['Snapshot'], 
						mode='line',
						# marker=plotly.graph_objs.Marker(color='rgb(255, 127, 14)'),
						name='H_' + str(order)
						)
		data.append(trace1)
		# figure1.append_trace(trace1, 1, 1)
	layout = go.Layout(
	title = str(file),
    xaxis=dict(
        title='Snapshot',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        # exponentformat='e',
        # showexponent='All'
    ),
    yaxis=dict(
        title='Distance to Center',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        # exponentformat='e',
        # showexponent='All'
    ))
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename= str(savefile), auto_open=False)
