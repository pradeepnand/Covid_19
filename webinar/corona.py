from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
from io import StringIO
from io import BytesIO
import base64
import urllib.parse
import io
import plotly
import plotly.figure_factory as ff 
import plotly.express as px
import folium
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def scrape():
    url="https://www.mohfw.gov.in/"
    #headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response=requests.get(url) #, headers=headers)
    soup= BeautifulSoup(response.content,'html.parser')
    coronatable_in= soup.find_all("table")
    corona1=coronatable_in[0]
    states=[]
    total_cases=[] #confirmed_cases
    cmd=[] #cured_migrated_discharged
    deaths=[]
    rows=corona1.find_all('tr')[1:-5]
    for row in rows:
        col=row.find_all('td')
        states.append(col[1].text.strip())
        total_cases.append(col[2].text.strip())
        cmd.append(col[3].text.strip())
        deaths.append(col[4].text.strip())
    df = pd.DataFrame(list(zip(states, total_cases, cmd, deaths)), 
               columns =['States', 'Total_Cases',"Cured", "Deaths"]) 
    df.replace({"Uttarakhand": "Uttaranchal", 
                                  "Odisha":"Orrisa"}, inplace=True) 
    df['Total_Cases'] = df['Total_Cases'].astype(int)
    df['Cured']=df['Cured'].astype(int)
    df['Deaths']=df['Deaths'].astype(int)
    df["recovery_rate"] = np.where(df["Cured"]>0,round((df["Cured"]/df["Total_Cases"])*100,2),0)
    df["mortality_rate"]= np.where(df["Deaths"]>0,round((df["Deaths"]/df["Total_Cases"])*100,2),0)
    df["active_cases"]= df["Total_Cases"] - df["Cured"] - df["Deaths"]
    df.sort_values(["Total_Cases"], inplace=True, ascending=False)
    df.reset_index(drop=True,inplace=True)
    return df

def table():
    df = scrape()
    df1 = ff.create_table(df)
    #return df1
    return plotly.offline.plot(df1,output_type='div')

def total():
    df=scrape()
    Total_Cases=df["Total_Cases"].sum()
    Total_Cured=df["Cured"].sum()
    Total_Deaths=df["Deaths"].sum()
    Active_Cases=df["active_cases"].sum()
    Mortality_Rate = round((df["Deaths"].sum()/df["Total_Cases"].sum())*100,2)
    Recovery_Rate = round((df["Cured"].sum()/df["Total_Cases"].sum())*100,2)
    return [Total_Cases,Total_Cured,Total_Deaths,Active_Cases,Mortality_Rate,Recovery_Rate]

def plot1():
    df=scrape()
    #sns.set_style("dark")
    img = io.BytesIO()  # create the buffer
    f, ax = plt.subplots(figsize=(8,4))
    ax.set_title('correlation Heat map', fontsize=16)
    sns.heatmap(df[["Total_Cases","Cured","Deaths"]].corr(), annot=True,fmt="0.0%")
    plt.savefig(img, format='png')  # save figure to the buffer
    plt.close()
    img.seek(0)  # rewind your buffer
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
    return plot_data
    

def plot2():
    df=scrape()
    df= df[df["Total_Cases"] > 100]
    fig = px.bar(df, x='States', y='Total_Cases', color='Total_Cases', height=600)
    return plotly.offline.plot(fig,output_type='div')

def plot6():
    df=scrape()
    df= df[df["Total_Cases"] <= 100]
    df_plot = df.sort_values("Total_Cases",ascending=True)
    fig = px.bar(df_plot, x='States', y='Total_Cases', color='Total_Cases', height=600)
    return plotly.offline.plot(fig,output_type='div')

def plot3():
    df=scrape()
    img = io.BytesIO()  # create the buffer
    df_plot = df.sort_values("Total_Cases",ascending=False)
    df_plot = df_plot[df_plot["Total_Cases"] > 100]
    fig, x1 = plt.subplots(figsize=(12.5,5))
    x1.grid(False)
    x1.set_title('total cases vs mortality rate', fontsize=16)
    x1 = sns.barplot(x="States",
                         y="Total_Cases",
                         data = df_plot
                         )
    plt.xticks(fontsize=7, rotation=40)
    x1.legend(['total cases'])
    #specify we want to share the same x-axis
    x2 = x1.twinx()
    x2.grid(False)
    color='tab:red'
    #line plot creation
    x2 = sns.lineplot(x='States', y='mortality_rate', data = df_plot,sort = False,color=color)
    x2.legend(['mortality rate'],loc='upper left', bbox_to_anchor=(0.6, 1.0), shadow=True, ncol=2)
    plt.savefig(img, format='png')  # save figure to the buffer
    plt.close()
    img.seek(0)  # rewind your buffer
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
    return plot_data

def plot4():
    df=scrape()
    img = io.BytesIO()  # create the buffer
    df_plot = df.sort_values("Total_Cases",ascending=False)
    df_plot = df_plot[df_plot["Total_Cases"] > 100]
    fig, x1 = plt.subplots(figsize=(12.5,5))
    x1.grid(False)
    x1.set_title('total cases vs recovery rate', fontsize=16)
    x1 = sns.barplot(x="States",
                         y="Total_Cases",
                         data = df_plot
                         )
    plt.xticks(fontsize=7, rotation=40)
    x1.legend(['total cases'])
    #specify we want to share the same x-axis
    x2 = x1.twinx()
    x2.grid(False)
    color= 'tab:green'
    #line plot creation
    x2 = sns.lineplot(x='States', y='recovery_rate', data = df_plot,sort = False,color=color)
    x2.legend(['recovery rate'],loc='upper left', bbox_to_anchor=(0.6, 1.0), shadow=True, ncol=2)
    plt.savefig(img, format='png')  # save figure to the buffer
    plt.close()
    img.seek(0)  # rewind your buffer
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
    return plot_data

def plot5():
    df=scrape()
    img = io.BytesIO()  # create the buffer
    df_plot = df.sort_values("recovery_rate",ascending=False)
    df_plot = df_plot[df_plot["Total_Cases"] > 100]
    fig, x1 = plt.subplots(figsize=(12.5,5))
    color = 'tab:green'
    x1.grid(False)
    x1.set_title('recovery rate vs mortality rate', fontsize=16)
    x1 = sns.lineplot(x="States",
                         y="recovery_rate",
                         data = df_plot,color=color,sort=False
                         )
    plt.xticks(fontsize=7, rotation= 40)
    x1.legend(['recovery_rate'])
    #specify we want to share the same x-axis
    x2 = x1.twinx()
    x2.grid(False)
    color = 'tab:red'
    #line plot creation
    x2 = sns.lineplot(x='States', y='mortality_rate', data = df_plot,sort = False,color=color)
    x2.legend(['mortality rate'],loc='upper left', bbox_to_anchor=(0.6, 1.0), shadow=True, ncol=2)
    plt.savefig(img, format='png')  # save figure to the buffer
    plt.close()
    img.seek(0)  # rewind your buffer
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
    return plot_data
