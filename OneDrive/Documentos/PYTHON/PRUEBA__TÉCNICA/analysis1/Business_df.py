
from dash import Dash, html, dcc
from plotly import data
import plotly.express as px
import pandas as pd
import json

app = Dash(__name__)

file = open("C:\\Users\\estef\\OneDrive\\Documentos\\PYTHON\PRUEBA__TÉCNICA\\yelp_academic_dataset_business.json", "r", encoding="utf8")

dataset = []

for business in file:
    dataset.append(json.loads(business))

dictionary = {}
states_dictionary = {}

for d in dataset:
    star = d["stars"]
    if star in dictionary:
        dictionary[star] = dictionary[star] + 1
    else:
        dictionary[star] = 1

for d in dataset:
    state = d["state"]
    stars = d["stars"]
    if state in states_dictionary:
        if stars in states_dictionary[state]:
            states_dictionary[state] = {
                **states_dictionary[state],
                stars: states_dictionary[state][stars] + 1
            }
        else:
            states_dictionary[state] = {
                **states_dictionary[state],
                stars: 1
            }
    else:
        states_dictionary[state] = {
            stars: 1
        }

df = pd.DataFrame({
    "Stars ⭐️": list(dictionary.keys()),
    "Amount 📊": list(dictionary.values())
})

print(states_dictionary)

stars = []
amount = []
states = []

for key in states_dictionary.keys():
    value = states_dictionary[key]
    for j in value:
        val = value[j]
        states.append(key)
        stars.append(j)
        amount.append(val)


states_df = pd.DataFrame({
    "States": states,
    "Amount": amount,
    "Stars": stars
})

fig = px.bar(df, x="Stars ⭐️", y="Amount 📊", barmode="group")
states_fig = px.bar(states_df, x="States", y="Amount",
                    color="Stars", barmode="group")

app.layout = html.Div(
    children=[
        html.Div([
            html.H1(children='Quantity of business by stars'),
            html.Div(children='''General Report 📝'''),
            dcc.Graph(id='stars', figure=fig),
        ]),
        html.Div([
            html.H1(children='Quantity of business by state with a specific rating'),
            html.Div(children='''Specific Report 📉'''),
            dcc.Graph(id='states', figure=states_fig),
        ])
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
