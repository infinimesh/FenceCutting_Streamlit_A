## -------------------------------
## ====    Import smthng      ====
## -------------------------------

##Libraries for Streamlit
##--------------------------------
import streamlit as st
from PIL import Image
import io
from scipy.io import wavfile as scipy_wav

##Libraries for prediction
##--------------------------------
import numpy as np
import matplotlib.pyplot as plt
import auditok
# import tensorflow as tf
# from tensorflow.keras import models





## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


## Page decorations
##--------------------------------


id_logo = Image.open("TypoMeshDarkFullat3x.png")
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image(id_logo)

st.markdown("<h1 style='text-align: center; color: grey;'>AI Audio Recognition App</h1>", 
            unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Fence Cutting Detector</h1>", 
            unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: black;'>Canvas Cutting Detection</h3>", 
#             unsafe_allow_html=True)
st.header(" ")
st.header(" ")





## -------------------------------
## ====  Select and load data ====
## -------------------------------
# st.header("Select data to analyze")
st.markdown("<h2 style='text-align: center; color: grey;'>Select data to analyze</h2>", 
            unsafe_allow_html=True)

st.subheader("Select one of the samples")
##---------------------------------------
selected_provided_file = st.selectbox(label="", 
                            options=["option_1", 
                                     "option_2",
                                     "option_3",]
                            )

if selected_provided_file == "option_1":
    region = auditok.load("./samples2try/sample_Fence_Session_2.wav")
elif selected_provided_file == "option_2":
    region = auditok.load("./samples2try/sample_Fence_thin_wire.wav")
elif selected_provided_file == "option_3":    
    region = auditok.load("./samples2try/sample_Green_Fence_Strings_Session_1.wav")



st.subheader("Play the audio")
##----------------------------
# st.audio(region.samples, sample_rate=region.sampling_rate)
audio_sampling_rate = region.sampling_rate
audio_data = region.samples

audio_data = (audio_data - np.mean(audio_data)) / np.std(audio_data)

virtualfile = io.BytesIO()
scipy_wav.write(virtualfile, rate=audio_sampling_rate, data=audio_data)
uploaded_audio_file = virtualfile
st.audio(uploaded_audio_file, format='audio/wav')




st.subheader("Plot the detected events")
##--------------------------------------
audio_regions = region.split_and_plot(
                                min_dur=0.01,     # minimum duration of a valid audio event in seconds
                                max_dur=0.5,       # maximum duration of an event
                                max_silence=0.2, # maximum duration of tolerated continuous silence within an event
                                energy_threshold=55, # 55 # threshold of detection
                                save_as='auditok_fig.png',
                                show=False,
                            )


auditok_fig_reggions = Image.open("auditok_fig.png")
st.image(auditok_fig_reggions)


events_per_second = len(audio_regions) / region.duration

st.subheader("Rate of Events per second:")
st.markdown(f"### _{events_per_second}_")

