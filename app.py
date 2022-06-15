import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, Table, MetaData
import plotly.express as px
import plotly
import json
# import plotly.graph_objs as go
from flask import Flask, render_template

app = Flask(__name__)

#Connect to the database in AWS
url = "postgresql://root:postgresfp@muspostgresdbfp.cdwx9vxigxvl.us-east-1.rds.amazonaws.com:5432/final_project"
engine = create_engine(url)
connect = engine.connect()


@app.route('/')
def home():
    #Writing a query for the first table
    query1 = '''select state,
	         count(operation_id) as transaction_qty,
	         round(cast((avg(transaction_amount)/1000) as numeric),2) as avg_cost
            from whole_collection_geom
            where fraud_flag = 'Yes'
            group by 1
            order by 2 desc
            '''
    # output first pandas dataframe, creating first figure and setting the data to Json
    fraud_detail = pd.read_sql(query1, con=connect)
    pd.options.plotting.backend='plotly'
    fig1=fraud_detail.plot.bar(x=fraud_detail['state'], y=fraud_detail['transaction_qty'], color=fraud_detail['transaction_qty'],
                           title='Fraud Transacion per State',
                           labels={'state':'State','transaction_qty':'Fraud Transactions'},
                           text_auto=True,
                           height=600,
                           width=1300)      
    #Seting to json the python plotly chart (Fig1)
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # creating second figure and setting the data to Json
    fig2=fraud_detail.plot.bar(x=fraud_detail['state'], y=fraud_detail['avg_cost'], color=fraud_detail['avg_cost'],
                           title='Average value per transaction by month and state',
                           labels={'state':'State','avg_cost':'Average value (K)'},
                           text_auto=True)                           
    #Seting to json the python plotly chart (Fig1)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # output second pandas dataframe, creating third figure and setting the data to Json
    query2 = '''select month_created,
	                to_char(date_created, 'Month') as Month,
	                count(operation_id) as transaction_qty,
	                round(cast(sum(transaction_amount)/1000 as numeric), 2) as total_cost
                from whole_collection_geom
                where fraud_flag='Yes'
                group by 1,2
                order by 1
                '''
    # output is pandas dataframe
    month_detail = pd.read_sql(query2, con=connect)
    fig3=px.histogram(month_detail,x=month_detail['month_created'],y=month_detail['transaction_qty'], nbins=20,
                  color_discrete_sequence=['indianred'],
                  title='Transacciones fraudulentas por mes',
                  labels={'month_created':'Mes','transaction_qty':'Cantidad de transacciones'},
                  text_auto=True,)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    # creating fourth figure and setting the data to Json
    fig4=px.histogram(month_detail,x=month_detail['month_created'],y=month_detail['total_cost'], nbins=20,
                  color_discrete_sequence=['#7C5ABD'],
                  title='Costo fraudulento por mes',
                  labels={'month_created':'Mes','total_cost':'Costo total de los articulos (K)'},
                  text_auto=True,)
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    # output third pandas dataframe, creating fifth figure and setting the data to Json
    query3 = '''select state,
            	    municipality,
	                month_created,
                    fraud_flag,
	                latitude,
                    longitude,	
	                count(operation_id) as operations_qty,
	                round(cast(sum(transaction_amount) as numeric), 2) as total_cost
                from whole_collection_geom
                group by 1,2,3,4,5,6
                order by 3,7 desc
                '''
    geom_detail = pd.read_sql(query3, con=connect)
    geom_detail['totaldisplay']=geom_detail['total_cost']**.5

    fig5=px.scatter_geo(geom_detail, lat='latitude', lon='longitude',
                    color='operations_qty',
                    hover_name='municipality',
                    labels={'month_created':'month_created', 'max_total_cost':'total_cost',
                            'latitude':'latitude','longitude':'longitude','operations_qty':'operations_qty'},
                    size='totaldisplay',
                    animation_frame='month_created',
                    projection='equirectangular',
                    scope='north america',
                    width=1000,
                    height=700,
                    center={'lat':21.8858107, 'lon':-102.3263188})
    fig5.update_layout(title_text='Densidad de compras en un año',geo=dict(landcolor = 'rgb(173, 173, 173)',bgcolor='rgb(64, 65, 65)'))
    graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    # output fourth pandas dataframe, creating sixth figure and setting the data to Json
    query4 ='''select state,
                    municipality,
	                month_created,
                    fraud_flag,
	                latitude,
                    longitude,	
	                count(operation_id) as operations_qty,
	                round(cast(sum(transaction_amount) as numeric), 2) as total_cost
                from whole_collection_geom
                where fraud_flag='Yes'
                group by 1,2,3,4,5,6
                order by 3,7 desc
                '''
    fraud_geom_detail = pd.read_sql(query4, con=connect)
    fraud_geom_detail['totaldisplay']=fraud_geom_detail['total_cost']**.5
    
    fig6=px.scatter_geo(fraud_geom_detail, lat='latitude', lon='longitude',
                    color='operations_qty',
                    hover_name='municipality',
                    labels={'month_created':'month_created', 'max_total_cost':'total_cost',
                            'latitude':'latitude','longitude':'longitude','operations_qty':'operations_qty'},
                    size='totaldisplay',
                    animation_frame='month_created',
                    projection='equirectangular',
                    scope='north america',
                    width=1000,
                    height=700,
                    center={'lat':21.8858107, 'lon':-102.3263188})
    fig6.update_layout(title_text='Densidad de compras fraudulentas en un año',geo=dict(landcolor = 'rgb(173, 173, 173)',bgcolor='rgb(64, 65, 65)'))
    graphJSON6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    # output fifth pandas dataframe, creating seventh figure and setting the data to Json
    query5='''select *
            from (select item1_name,
                    month_created,
	 		        count(operation_id) as transaction_qty,
			        round(cast((avg(transaction_amount)/1000) as numeric),2) as avg_cost
	              from whole_collection_geom
	              where fraud_flag = 'Yes'
	              group by 1,2
	              order by 2,3 asc) AS T1
                '''
    item_fraud = pd.read_sql(query5, con=connect)

    fig7=px.bar(item_fraud,x='transaction_qty', y='item1_name',
                           color_discrete_sequence=['#F5B630'],
                           title='Transacciones Fraudulentas por articulo',
                           labels={'item1_name':'Articulo','transaction_qty':'Transacciones Fraudulentas'},
                           text_auto=True,
                           orientation='h',
                           animation_frame='month_created',
                           height=600,
                           width=1000)                           
    fig7.update_layout(xaxis_range=[0,15])
    graphJSON7 = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    
    # creating eighth figure and setting the data to Json
    fig8=px.bar(item_fraud,x='avg_cost', y='item1_name',
                           color_discrete_sequence=['#4956F3'],
                           title='Valor promedio por articulo',
                           labels={'item1_name':'Articulo','avg_cost':'Costo promedio del articulo (K)'},
                           text_auto=True,
                           orientation='h',
                           animation_frame='month_created',
                           height=600,
                           width=1000)                           
    fig8.update_layout(xaxis_range=[0,15])
    graphJSON8 = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)
     
    return render_template("index.html", graphJSON1=graphJSON1,graphJSON2=graphJSON2,
                                            graphJSON3=graphJSON3, graphJSON4=graphJSON4,
                                            graphJSON5=graphJSON5,graphJSON6=graphJSON6,
                                            graphJSON7=graphJSON7,graphJSON8=graphJSON8)

# @app.route('/list')

if __name__=='__main__':
    app.run(debug=False)