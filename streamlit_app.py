## -------------------------------
## ====    Import smthng      ====
## -------------------------------

##Libraries for Streamlit
##--------------------------------
import streamlit as st
from PIL import Image
import io
import os
from scipy.io import wavfile as scipy_wav
import pydub

##Libraries for prediction
##--------------------------------
import numpy as np
import matplotlib.pyplot as plt
import auditok
# import tensorflow as tf
# from tensorflow.keras import models



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


# # st.snow()
# snow_state = 0
# if snow_state == 0:
#     st.snow()
#     snow_state = 1


## -------------------------------
## ====  Select and load data ====
## -------------------------------
# st.header("Select data to analyze")
st.markdown("<h2 style='text-align: center; color: grey;'>Select data to analyze</h2>", 
            unsafe_allow_html=True)



st.subheader("Select one of the samples")
##---------------------------------------
selected_provided_file2 = st.selectbox(label="", options=os.listdir("./samples2try/"))
audio_file_name = "./samples2try/" + selected_provided_file2



st.subheader("or Upload an audio file in WAV format")
##---------------------------------------------------
st.write("if a file is uploaded, previously selected samples are not taken into account")

uploaded_audio_file = st.file_uploader(label="Select a single-channels WAV file", 
                                        type="wav", 
                                        accept_multiple_files=False, 
                                        key=None, 
                                        help=None, 
                                        on_change=None, 
                                        args=None, 
                                        kwargs=None, 
                                        disabled=False)


##Data reading
##----------------------------
if uploaded_audio_file is not None:
    bytes_data = uploaded_audio_file.read()
    region = auditok.load(bytes_data, sampling_rate=44100, sample_width=2, channels=1, skip=0.001)

else:
    region = auditok.load(audio_file_name)



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

st.subheader("Number of detected Events:")
##----------------------------------------
st.markdown(f"### _{len(audio_regions)}_")

# st.subheader("Rate of Events per second:")
# st.markdown(f"### _{events_per_second}_")

st.subheader("Select Threshoold for Alarm:")
##----------------------------------------
st.write("If the number of detected events is more of equal to the Threshoold within 10sec, the alarm is triggered.")
# alarm_threshold = st.slider('Select the Threshoold level', 0, 10, 3)
alarm_threshold = st.slider('', 0, 10, 3)
# st.write('Values:', alarm_threshold)


if len(audio_regions) >= alarm_threshold:
    st.error('===> Alarm is triggered. <===', icon="🚨")
elif len(audio_regions) >= 1:
    st.info('An Event is detected, but the Threshoold is not reached.', icon="ℹ️")
else:
    st.success('Nothing is detected, keep calm, relax.', icon="✅")