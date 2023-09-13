
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
"""
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
"""
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
print("after year_list created")
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div(childeren=[
    #TASK 2.1 Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard", 
        style={'textAlign': 'center', 'color': '#503D36', 'font-size':24}
    ),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label(
            "Select Statistics:", style={'margin-right': '2em'}
        ),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label' : 'Yearly Statistics', 'value':'Yearly Statistics'},
                {'label': 'Recession Statistics','value':'Recession Statistics'}
            ],
            value ='Yearly Statistics', #'Default Statistics
            #placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size':'20px', 'text-align-last':'center'}
        )
    ]),
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value = 1980, # 'Default Year'
            #placeholder='Select a year to report',
            style={'width': '80%', 'padding': '3px', 'font-size':'20px', 'text-align-last':'center'}
        )
    ),
    html.Div([#TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])
print("layout is created")
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value')
)


def update_input_container(selected_statistics):
    print("update_input_container : selected_statistics : " +str(selected_statistics))
    
    if selected_statistics =='Yearly Statistics': 
        print("if update_input_container : selected_statistics == 'Yearly Statistics', and actual argument is : " +str(selected_statistics))
        print("return False")
        return False
    else: 
        print("else update_input_container : selected_statistics == 'Recession Statistics', and actual argument is : " +str(selected_statistics))
        print("return True")
        return True


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')]
)


def update_output_container(input_year, selected_statistics):
    print("update_output_container :: input_year : " +str(input_year)+ " /  selected_statistics : " +str(selected_statistics))
    
    if selected_statistics == 'Recession Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        print("if selected_statistics == 'Recession Statistics', and actual argument is : "+str(selected_statistics))

#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_sales=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_sales, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )
        print("R_chart1")
#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        type_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(
            figure=px.line(type_sales, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Automobile Sales per Vehicle Type'
            )
        )
        print("R_chart2")
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        type_exp= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(type_exp,
                values='Advertising_Expenditure', 
                names='Vehicle_Type', 
                title=" Total Advertising Expenditure per Vehicle Type"
            )
        )
        print("R_chart3")
# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unempl_type_sale = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()
        R_chart4 = dcc.Graph(
            figure = px.bar(unempl_type_sale, 
                x='Unemployment_Rate', 
                y='Automobile_Sales', 
                color='Vehicle_Type', 
                title='Total sales across Unemployment Rate and Vehicle Type'
            )
        )   
        print("R_chart4")

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
        ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
        print("elif input_year is True and selected_statistics == 'Yearly Statistics', and actual argument is : "+str(selected_statistics))                    
#TASK 2.5: Creating Graphs Yearly data
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        avg_sales= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(avg_sales, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation"
            )
        )
        print("Y_chart1")   
# Plot 2 Total Monthly Automobile sales using line chart.
        monthly_sales= data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(monthly_sales, 
                x='Month',
                y='Automobile_Sales',
                title="Total Monthly Automobile Sales fluctuation in"
            )
        )
        print("Y_chart2") 
# Plot bar chart for average number of vehicles sold during the given year
        avg_sales_year=yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
             figure=px.bar(
                avg_sales_year, 
                x='Month', 
                y='Automobile_Sales', 
                title='Average sales in {}'.format(input_year)
             )
        )
        print("Y_chart3") 
            # Total Advertisement Expenditure for each vehicle using pie chart
        total_exp_year=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(total_exp_year,
                values='Advertising_Expenditure', 
                names='Vehicle_Type', 
                title=" Total Advertising Expenditure per Vehicle Type in {}".format(input_year)
            )
        )
        print("Y_chart4") 
#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]
        
    else:
        print("update_output_container : selected_statistics is NOT 'Yearly Statistics', and actual argument is : " +str(selected_statistics))
        return None
print("after def update_output_container")

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

