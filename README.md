# analysis-vtuber
This repository aims at giving a public access to the dashboard developped to see interactive data analysis of french VTubers.

In order to make it work on your own machine, follow these steps :
- install all required packages : pip -r requirements.txt
- git clone the repository in a local folder of your machine
- verify that the paths are the good ones
- then, from your terminal launch the command line : python index.py

Once on the dashboard, there is a welcome page. You can navigate towards two others pages containing the analysis.
- General : gives a global overview conerning the french Vtubers
- Vtuber : gives a overview on a specific VTuber. This Vtuber can have a Youtube channel and a Twitch channel. By default, every reachable Vtuber has on this dashboard a youtube channel since this dashboard has been created with the Virtual Youtubers database.

Concerning the data : 
We had these data using python scripts and the Youtube and Twitch APIs. Data cleaning, treatments were done by ourselves. 

Concerning the dashboard : 
We have chosen to use dash from plotly to develop the dashboard since it is a very convenient tool when developing web application for data analysis.
