from flask import Flask, render_template, send_file, make_response
from corona import table, plot1, plot2,plot3,plot4,plot5,total,plot6
from flask import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
from io import StringIO
from io import BytesIO
import base64
import urllib.parse
import plotly
import plotly.figure_factory as ff 
import plotly.express as px
import folium
import plotly.graph_objects as go
import matplotlib.pyplot as plt


app=Flask(__name__)

@app.route("/")

def show_tables():
    tableDisplay = table()
    figureDisplay1 = plot1()
    figureDisplay2= plot2()
    figureDisplay3= plot3()
    figureDisplay4= plot4()
    figureDisplay5= plot5()
    figureDisplay6= plot6()
    totals = total()

    return render_template('index.html', figure1=figureDisplay1, returnList=tableDisplay, figure6=figureDisplay6,
    figure2=figureDisplay2, figure3=figureDisplay3, figure4=figureDisplay4, figure5=figureDisplay5,total_data=totals )

if __name__ == "main":
    app.jinja_env.cache = {}
    app.run(debug=True)