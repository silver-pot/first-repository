import pandas as pd
import dash
#import dash_html_components as html
#import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash import dcc, html
#from dash import html
import plotly.express as px
#import plotly.graph_objs as go

#print("___imported libraries")
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#print("___spacex_df=pd.read_csv('spacex_launch_dash.csv')")
# Create a dash application
app = dash.Dash(__name__)
#print("___add=dash.Dash(__name__)")
# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard__',
                style={'textAlign': 'center', 'color': '#503D36','font-size': 20}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        html.Div([
            html.Label(
                "Launch Site", style={'margin-right':'2em'}
            ),
            dcc.Dropdown(
                id='site-dropdown',
                options=[
                    {'label':'All Sites', 'value':'All Sites'},
                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                ],
                value='ALL Sites',
                placeholder="Select a Lauch Site here",
                searchable=True
            )
        ]),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div([
            #html.Label(
            #    "Pie chart", style={'margin-right':'2em'}
            #),
            dcc.Graph(id='success-pie-chart')
        ]),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        #dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 2000: '2000', 4000: '4000', 6000: '6000', 8000: '8000', 10000:'10000'}, value=[min_payload, max_payload]),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(id='success-payload-scatter-chart')
        ),
    ]
)
#print("___html layout created")
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
#print("___callback for dropdown")
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    All_sites_df=spacex_df[spacex_df['class']==1]
    CCAFS_LC_df=spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
    CCAFS_SLC_df=spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
    KSC_LC_df=spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
    VAFB_SLC_df=spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
    #print("____before if-else ALL in get_pie_chart")
    if entered_site=='All Sites':
        site_counts=All_sites_df['Launch Site'].value_counts()
        fig=px.pie(All_sites_df, values=site_counts.values, names=site_counts.index, title='Total Success Launches By Site')
        #print('______returning ALL pie')
        
    elif entered_site=='CCAFS LC-40':
        site_counts=CCAFS_LC_df['class'].value_counts()
        fig=px.pie(CCAFS_LC_df, values=site_counts.values, names=site_counts.index, title='Total Success Launches For Site CCAFS LC-40')
        #print('______returning CCAFS LC pie')

    elif entered_site=='CCAFS SLC-40':
        site_counts=CCAFS_SLC_df['class'].value_counts()
        fig=px.pie(CCAFS_SLC_df, values=site_counts.values, names=site_counts.index, title='Total Success Launches For Site CCAFS SLC-40')
        #print('______returning CCAFS SLC pie')

    elif entered_site=='KSC LC-39A':
        site_counts=KSC_LC_df['class'].value_counts()
        fig=px.pie(KSC_LC_df, values=site_counts.values, names=site_counts.index, title='Total Success Launches For Site KSC LC-39A')
        #print('______returning KSC pie')

    elif entered_site=='VAFB SLC-4E':
        site_counts=VAFB_SLC_df['class'].value_counts()
        fig=px.pie(VAFB_SLC_df, values=site_counts.values, names=site_counts.index, title='Total Success Launches For Site VAFB SLC-4E')
        #print('______returning VAFB pie')

    else:
        #print('______else returning nothing')
    
    return fig

print('___get_pie_chart ended')
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
print("___callback for slider")
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(entered_site, slider_range):
    low, high = slider_range
    print('___entered_site : ', entered_site, '    slider_range : ', slider_range )
    if entered_site=='All Sites':
        filtered_df=spacex_df
        print("______preparing_", entered_site, "_scatter_chart")
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        if high > filtered_df['Payload Mass (kg)'].max():
            print("high>filtered_df_[Kg].max")
            high=filtered_df['Payload Mass (kg)'].max()
        else:
           None 
        if low < filtered_df['Payload Mass (kg)'].min():
            print("low<filtered_df_[kg].min")
            low=filtered_df['Payload Mass (kg)'].min()
        else:
            None
        #print("______preparing_", entered_site, "_scatter_chart")

    mask = (filtered_df['Payload Mass (kg)'] >= low) & (filtered_df['Payload Mass (kg)'] <= high)
    #print("______x axis masked for scatter chart", )
    fig = px.scatter(
        filtered_df[mask], 
        x="Payload Mass (kg)", 
        y="class", 
        color="Booster Version Category", 
        hover_data=['Booster Version']
    )
    #print("___masked scatter_chart is ready")
    return fig

#print("___get scatter chart ended")

# Run the app
if __name__ == '__main__':
    app.run_server()