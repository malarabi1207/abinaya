import streamlit as st
import cv2
import numpy as np
from PIL import Image
# Title of the Web App
st.title("🌍 Cloud Detection and Tracking for Geostationary Satellite Images ☁️")

# Sidebar Navigation
st.sidebar.title("Navigation")


# Custom CSS to change the background color of the sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #faf0e6; /* grey */
        }
    </style>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio("Go to:", ["Welcome Page", "About", "Cloud Detection", "Weather Explanation"])
 
# WELCOME PAGE
if page == "Welcome Page":
    st.header("Welcome to the Cloud Detection & Tracking System!")
    st.write("""
    This application helps detect and track clouds using geostationary satellite images. 
    Simply upload a satellite image, and our model will analyze it to detect cloud patterns and coverage.
    """)
    
    # Instructions Section
    st.subheader("📌 How to Use:")
    st.write("""
    1. Navigate to the **Cloud Detection Page**.
    2. Upload a **satellite image** in JPG, PNG, or TIFF format.
    3. The system will **analyze the image** and display detected clouds.
    4. You will see **bounding boxes** around detected clouds.
    5. Cloud coverage percentage will be displayed.
    6. Visit the **Weather Explanation** page for interpretation.
    """)
    
    # Footer
    st.markdown("---")
    st.write("🌎 Developed By: M MALAR & S JANANI| **Year:** 2025")
    # Set background color to sky blue
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #b9f2ff; /* Sky Blue */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

 # ABOUT PAGE
elif page == "About":
    st.header("📖 About This Application")
    st.write("""
    This cloud detection and tracking application was developed to assist in analyzing geostationary satellite images. 
    Using advanced image processing techniques, this system identifies cloud formations, tracks their movement, 
    and provides weather insights based on cloud coverage.
    
    **Key Features:**
    - Cloud detection using satellite imagery
    - Bounding box visualization of detected clouds
    - Cloud coverage percentage calculation
    - Weather condition interpretation
    - User-friendly interface powered by Streamlit
    
    **Developed By: M MALAR & S JANANI| **Year:** 2025
    """)
    # Set background color to sky blue
    st.markdown(
    """
    <style>
    .stApp {
     background-color: #b9f2ff; /* Sky Blue */
     }
     </style>
     """,
     unsafe_allow_html=True
 )
# CLOUD DETECTION PAGE
elif page == "Cloud Detection":
    st.header("🛠️ Cloud Detection System")
    st.sidebar.write("Upload geostationary satellite images to perform cloud detection.")

    # Upload satellite image
    uploaded_file = st.sidebar.file_uploader("Choose a satellite image", type=["jpg", "jpeg", "png", "tiff"])
    # Set background color to sky blue
    st.markdown(
       """
       <style>
       .stApp {
           background-color: #b9f2ff; /* Sky Blue */
       }
       </style>
       """,
       unsafe_allow_html=True
   )


    if uploaded_file is not None:
        # Read and display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Satellite Image", use_column_width=True)

        # Convert the uploaded image to a format OpenCV can process
        img = np.array(image.convert("RGB"))

        # Convert to grayscale for processing
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Apply binary thresholding for cloud detection
        threshold_value = 200  # Adjust based on satellite image characteristics
        _, cloud_mask = cv2.threshold(gray_img, threshold_value, 255, cv2.THRESH_BINARY)

        # Calculate cloud coverage percentage
        cloud_coverage = np.mean(cloud_mask > 0) * 100  # Percentage of image covered by clouds

        # Bounding Box Detection
        contours, _ = cv2.findContours(cloud_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes on the original image
        img_with_boxes = img.copy()
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green bounding box

        # Convert BGR to RGB for Streamlit display
        img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)

        # Display detected results
        st.image(img_with_boxes, caption="Clouds with Bounding Boxes", use_column_width=True)
        st.image(cloud_mask, caption="Cloud Mask (Binary)", use_column_width=True)
        st.write(f"☁️ **Cloud Coverage:** {cloud_coverage:.2f}%")
        # Set background color to sky blue
        st.markdown(
           """
           <style>
           .stApp {
               background-color: #b9f2ff; /* Sky Blue */
           }
           </style>
           """,
           unsafe_allow_html=True
       )


        # Save cloud coverage to session state for Weather Explanation
        st.session_state["cloud_coverage"] = cloud_coverage

    else:
        st.write("Please upload a satellite image to begin.")
        # Set background color to sky blue
        st.markdown(
        """
        <style>
        .stApp {
         background-color: #b9f2ff; /* Sky Blue */
         }
         </style>
         """,
         unsafe_allow_html=True
     )

# WEATHER EXPLANATION PAGE
elif page == "Weather Explanation":
    st.header("⛅ Weather Interpretation Based on Cloud Coverage")

    if "cloud_coverage" in st.session_state:
        cloud_coverage = st.session_state["cloud_coverage"]
        st.title(f"🌬️ **Detected Cloud Coverage:** {cloud_coverage:.2f}%")
        # Set background color to sky blue
        st.markdown(
           """
           <style>
           .stApp {
               background-color: #b9f2ff; /* Sky Blue */
           }
           </style>
           """,
           unsafe_allow_html=True
       )
        if cloud_coverage == 0:
            st.markdown("""<h2 style='font-size:30px; color:green;'>☀️ Clear sky detected! Minimal to no cloud presence.</h2>""", unsafe_allow_html=True)
        elif 0 < cloud_coverage <= 30:
            st.markdown("""<h2 style='font-size:30px; color:blue;'>🌤️ Partly cloudy conditions. Weather is mostly clear with some cloud patches.</h2>""", unsafe_allow_html=True)
        elif 30 < cloud_coverage <= 60:
            st.markdown("""<h2 style='font-size:30px; color:orange;'>⛅ Mostly cloudy conditions. Expect significant cloud coverage, with possible overcast periods.</h2>""", unsafe_allow_html=True)
        elif 60 < cloud_coverage <= 90:
            st.markdown("""<h2 style='font-size:30px; color:red;'>🌧️ Overcast sky detected! Limited visibility and possible precipitation.</h2>""", unsafe_allow_html=True)
        elif 90 < cloud_coverage <= 100:
            st.markdown("""<h2 style='font-size:30px; color:darkred;'>🌪️ Heavy cloud coverage! Possible storm formation or intense weather conditions.</h2>""", unsafe_allow_html=True)
        else:
            st.markdown("""<h2 style='font-size:30px; color:purple;'>☔️ High chance of rain! Expect wet conditions and potential thunderstorms.</h2>""", unsafe_allow_html=True)
    else:
        st.write("No detected cloud coverage data available. Please analyze an image first.")
        # Set background color to sky blue
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #b9f2ff; /* Sky Blue */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        