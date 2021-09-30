# filename = 'dash-01.py'

#
# Imports
#

import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#
# Data
#



year = 2002

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)


if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    

    

    #Back end
    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)

    #Front end 
    app.layout = html.Div(children=[

                            

                            html.H1(
                                id='title1',
                                children=f'Life expectancy vs GDP per capita ({year})',
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)
                            
                            html.Button('On/Off', id='button',n_clicks=0),

                            dcc.Dropdown(
                                id="year-dropdown",
                                options = [{'label':str(year),'value': year} for year in gapminder["year"].unique()],
                                value=2007,
                            ),

                            dcc.Slider(
                                id="year-slider",
                                min = 1952,
                                max =2007,
                                step =5,
                                #marks ={year: '{}'.format(year) for year in gapminder["year"].unique()},
                                value=2007,
                            ),

                            dcc.Interval(   id='interval',
                                interval=1*300, # in milliseconds
                                n_intervals=0,
                                disabled = True,
                            ),

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''), # (7)

                            html.Label('Year'),
                            

                            

    ]
    )
    @app.callback(
        Output(component_id='graph1', component_property='figure'),
        Output(component_id='title1', component_property='children'), # (1)
        [Input(component_id="year-slider",component_property="value")]
        #[Input(component_id='year-dropdown', component_property='value')] # (2)
    )
    def update_figure(input_value): # (3)
        fig= px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)

        #fig.update_layout(title ='Life expectancy vs GDP per capita ('+str(input_value)+')')
        title = 'Life expectancy vs GDP per capita ('+str(input_value)+')'
        return fig,title
    
    @app.callback(  Output('year-slider', 'value'),
                    Output('interval','disabled' ),
                [Input('interval', 'n_intervals'),Input('button','n_clicks')])
    def on_tick(n_intervals,n_clicks):
        OK=True
        if n_intervals is None: return 0
        if n_clicks%2==0: OK=True
        else : OK =False
        return years[(n_intervals+1)%len(years)],OK

    #
    # RUN APP
    #

    
    
    app.run_server(port =2734,debug=True) # (8)

    