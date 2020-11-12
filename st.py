import streamlit as st
import altair as alt
import pandas as pd
alt.data_transformers.disable_max_rows()

hazard = pd.read_csv('hazard_for_challenge.csv')

cols = hazard.columns.to_list()
timestamps = [x for x in cols if x not in [
    'reference', 'longitude', 'latitude']]

st.sidebar.write('## Table of Content')
menu = st.sidebar.radio(
    'Sections',
    ('Compare probability of failure',
     'Monitor probability of failure',
     'Note on design process')
)

# Make Basemap for Manhattan
manhattan_geojson = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/manhattan.geojson'
basemap = alt.Chart(alt.topo_feature(manhattan_geojson, 'features')).mark_geoshape(
    fill='#eee', stroke='#fff', strokeWidth=2
)


# Layout Content
if menu == 'Compare probability of failure':
    # Make compare map
    ## Calculate difference in probability of failure by two timestamps of user choice
    first = st.sidebar.selectbox('Select first timestamp: ', timestamps)
    timestamps_second = timestamps.copy()
    timestamps_second.remove(first)
    second = st.sidebar.selectbox(
        'Select second timestamp: ', timestamps_second, index=25)

    hazard['change in probability'] = hazard[second] - hazard[first]

    ## Plot difference in probability of failure by asset
    compare_dotmap = alt.Chart(hazard,
                            title='Change in probability of failure from ' + first + ' to ' + second
                            ).mark_circle(
        stroke='#aaa', strokeWidth=0.5
    ).encode(
        latitude='latitude:Q',
        longitude='longitude:Q',
        tooltip=[alt.Tooltip('reference:N'),
                alt.Tooltip('change in probability:Q', format=".2%"),
                alt.Tooltip('timestamp:N')
                ],
        size=alt.Size('change in probability:Q',
                    scale=alt.Scale(range=[3, 500])),
        color=alt.Color('change in probability:Q',
                        scale=alt.Scale(scheme='reds'))
    )

    compare_map = alt.layer(
        basemap,
        compare_dotmap
    ).properties(
        width=698,
        height=900
    ).configure_view(
        stroke=None
    )

    st.altair_chart(compare_map)

elif menu == 'Monitor probability of failure':

    # Make monitor map with Altair date slider
    hazard_stacked = hazard.melt(id_vars=['reference', 'longitude', 'latitude'],
                                value_vars=timestamps,
                                var_name='timestamp',
                                value_name='probability of failure'
                                )

    timestamp_dropdown = alt.binding_select(options=timestamps)
    timestamp_select = alt.selection_single(
        fields=['timestamp'], bind=timestamp_dropdown, name="Select")

    monitor_dotmap = alt.Chart(hazard_stacked, title='Probability of failure by timestamp').mark_circle(
        stroke='#aaa', strokeWidth=0.5
    ).add_selection(
        timestamp_select
    ).transform_filter(
        timestamp_select
    ).encode(
        latitude='latitude:Q',
        longitude='longitude:Q',
        # Added percentage formatting to tooltip
        tooltip=[alt.Tooltip('reference:N'),
                alt.Tooltip('probability of failure:Q', format=".2%"),
                alt.Tooltip('timestamp:N')
                ],
        size=alt.Size('probability of failure:Q', scale=alt.Scale(range=[3, 500])),
        color=alt.Color('probability of failure:Q',
                        scale=alt.Scale(scheme='lightgreyred'))
    )

    monitor_map = alt.layer(
        basemap,
        monitor_dotmap
    ).properties(
        width=698,
        height=698
    ).configure_view(
        stroke=None
    )

    st.altair_chart(monitor_map)

else:
    st.write('# my article')
