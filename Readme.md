By Willa Hua

Nov 12, 2020

## Exploratory Data Analysis
The data contains asset failure probabilities of 2100 assets in NYC Manhattan, from 10/27 to 11/9, 2012, recorded 2 times a day at midnight and noon. I started by brainstorming some visualization tasks, such as comparison by day and night and filter assets by a threshold. Next, I explored the data in Tableau. Here're some findings:
- Looking at the distribution by boxplots and histograms, the probabilities of asset failure changed minimally over time, compares to their absolute values. 
- There's no significant difference between day and night, shown below.

<img alt="Tableau: Average probability of failure by day and night over the weeks" style = "width: 350px" src="https://raw.githubusercontent.com/wiiilla/TagupChallenge/master/img/TableauSmallMultiples.png">


- The lack of visually discernable fluctuation doesn't justify a small multiple visualization. A slider over time (shown below) adds interactivity and is useful for monitoring equipment, but fails to highlight spikes in hazard probability. For that, I need to calculate differences between two timestamps.

<img alt="Tableau: Time Slider Prototype" style = "width: 400px" src="https://raw.githubusercontent.com/wiiilla/TagupChallenge/master/img/TableauSliderPrototype.png">


## Goal Setting
For my visualization, I want to help my user, an asset manager, monitor risks of asset failure by performing two tasks:
- Identify increases in probabilities of failure over time
- Monitor assets with high values of probabilities of failure

## Final Solution
I made a two-layered map of Manhattan in Altair and used Streamlit, a Python-based data app builder, to change underlying data based on user input. I hosted the app on a virtual private server of mine. Here're some highlights of my solution:
- High-risk assets have high visual prominence
- Tooltip to read further information
- Data-driven chart title
- Dropdown boxes enable user customization of the timestamp for monitoring and the time frame for comparison

## Discussion
This visualization is made based on the assumption that the assets are independent of each other. If that's not the case (e.g., assets managed by the same organization), a more aggregated visualization could be better. The best solution always depends on context. For example, a choropleth map to show failure risk by neighborhood is useful in dispatching field workers; a heatmap based on spatial analysis for hot spots is useful for larger dataset where all assets cannot fit onto a single map. The visualization app can also be combined with an alert system that detects and alerts anomalies. 

### Tool comparison
Tableau would have been sufficient if we're only interested in visualizing absolute values. Visualizing changes based on a flexible user-specified time frame calls for a more technical solution. Mapbox and Leaflet take more engineering but offer maps with higher interactivity (e.g. zooming and panning).

### [Sourcecode](https://github.com/wiiilla/TagupChallenge)
To run the app locally, run the following line in console:
> streamlit run st.py

### Time Spent
- 1 hr Tableau
- 2 hr Altair
- 1 hr Documentation and Deployment
