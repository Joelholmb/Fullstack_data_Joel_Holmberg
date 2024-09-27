import streamlit as st 
from frontend.kpi import ContentKPI
from frontend.graphs import ViewsTrend
from frontend.graphs import ViewsTrend, Traffic
from frontend.graphs import SubscriberGrowth
from frontend.graphs import ViewerDemographics
from frontend.kpi import TopVideos



# device_kpi = DeviceKPI()
content_kpi = ContentKPI()
views_graph = ViewsTrend()
traffic_graph = Traffic()
subscriber_growth = SubscriberGrowth()
demographics = ViewerDemographics()
topp5Videos = TopVideos()



def layout():
    st.markdown("# The data driven youtuber")
    st.markdown("Den här dashboarden syftar till att utforska datan i min youtubekanal")
    # device_kpi.display_device_views()
    # device_kpi.display_device_summary()
    content_kpi.display_content()
    topp5Videos.display_top_videos()
    views_graph.display_plot()
    traffic_graph.display_traffic()
    subscriber_growth.display_subscriber_growth()
    demographics.display_demographics()
    



if __name__ == "__main__":
    layout()