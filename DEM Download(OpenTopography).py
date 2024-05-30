
import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
st.set_page_config(
        page_title="DEM Download(OpenTopography)",
)
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked=False
def callback():
    st.session_state.button_clicked=True
global dem1
import os
container =st.container()
with st.sidebar:
    selected=option_menu(menu_title="Main menu",options=["Home","Download DEM"])
    if selected=="Home":
            container.title('Streamlit Digital Elevation Model Downloading APP')
            container.caption('The APP uses Python to download  Digital Elevation Model')
            container.text("Requirements\n1.API KEY from OpenTopography\n2.Bounds of the DEM(North,East,South,West)")
    elif selected=="Download DEM":
            option1 = st.selectbox(
            "Select the Product?",
            ("SRTMGL3 (SRTM GL3 90m)","SRTMGL1 (SRTM GL1 30m)","SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)","AW3D30 (ALOS World 3D 30m)","AW3D30_E (ALOS World 3D Ellipsoidal, 30m)","SRTM15Plus (Global Bathymetry SRTM15+ V2.1 500m)","NASADEM (NASADEM Global DEM)","COP30 (Copernicus Global DSM 30m)","COP90 (Copernicus Global DSM 90m)","EU_DTM (DTM 30m)","GEDI_L3 (DTM 1000m)","GEBCOIceTopo (Global Bathymetry 500m)","GEBCOSubIceTopo (Global Bathymetry 500m)"),
            index=1,
            placeholder="Select contact method...",
            )
            file_name=st.text_input("Enter File Name","Raster")
            DEM_name={"SRTMGL3 (SRTM GL3 90m)":"SRTMGL3","SRTMGL1 (SRTM GL1 30m)":"SRTMGL1","SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)":"SRTMGL1_E","AW3D30 (ALOS World 3D 30m)":"AW3D30","AW3D30_E (ALOS World 3D Ellipsoidal, 30m)":"AW3D30_E","SRTM15Plus (Global Bathymetry SRTM15+ V2.1 500m)":"SRTM15Plus","NASADEM (NASADEM Global DEM)":"NASADEM","COP30 (Copernicus Global DSM 30m)":"COP30","COP90 (Copernicus Global DSM 90m)":"COP90","EU_DTM (DTM 30m)":"EU_DTM","GEDI_L3 (DTM 1000m)":"GEDI_L3","GEBCOIceTopo (Global Bathymetry 500m)":"GEBCOIceTopo","GEBCOSubIceTopo (Global Bathymetry 500m)":"GEBCOSubIceTopo"}
            format1={"GTiff for GeoTiff":"GTiff", "AAIGrid for Arc ASCII Grid":"AAIGrid", "HFA for Erdas Imagine (.IMG)":"HFA"}
            st.write("You selected:",option1,"in GeoTiff format" )
            container.title("Enter the details")
            container.write("Enter coordinates in Decimal Degrees ")
            col1,col2,col3,col4=container.columns(4)
            S_input=col1.text_input("South Bound",0)
            N_input=col2.text_input("North Bound",0)
            W_input=col3.text_input("West Bound",0)
            E_input=col4.text_input("East Bound",0)
            API_Key=container.text_input("API-KEY(OpenTopograhy)","32 digit API Key")
            if container.button("Show Bounds",on_click=callback):
                south=float(S_input)
                north=float(N_input)
                east=float(E_input)
                if float(south):
                    st.write("")
                else:
                    container.write("Invalid")
                    
                    
                xbounds=[south,south,north,north]
                west=float(W_input)
                ybounds=[east,west,east,west]
                df=pd.DataFrame(data={'lat':xbounds,"lon":ybounds})
                container.map(df)
            if st.button("Download DEM",type="primary"):
                url="https://portal.opentopography.org/API/globaldem?demtype="+DEM_name[option1]+"&south="+S_input+"&north="+N_input+"&west="+W_input+"&east="+E_input+"&outputFormat="+format1["GTiff for GeoTiff"]+"&API_Key="+API_Key
                response=requests.get(url)
                response_codes={200:"Valid request",204:"No Data",400:"Bad Request",401:"Unauthorized",500:"Internal error"}
                st.write("Status:",response_codes[response.status_code])
                
                if response.status_code==200:
                    open(f"{file_name}.tiff",'wb').write(response.content)
                    st.write("Download succesfull") 
                    st.write(f"File downloaded as {file_name}.tiff") 
                else:
                    container.write("Invalid Inputs") 
                
                