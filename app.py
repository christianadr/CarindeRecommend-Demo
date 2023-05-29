import streamlit as st
import prediction as pred
import nutrition_parser as ntp
from PIL import Image
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="CarindeRecommend")


def homePage():

    st.write("""
    # Welcome to CarindeRecommend Demo App - a Food Recommender System Powered by YOLOv5
    #### Partial fulfillment for the course CPE 020 - Methods of Research
    """)
    st.markdown("""---""")
    st.write(
        """
         ### How it Works
    1. **Object Detection:** The app uses YOLOv5, a pre-trained deep learning model designed to detect various food items in images.
    2. **Recommender System:** We analyze the ingredients detected in the image and recommend food meals that will suit your tastes.
    3. **Macro Detector:** We can also analyze the available nutrients on the food meal recommended by the app.

    **Please Note:** This app is a demo version created within the time constraints of our project which is limits from perfect detections and recommendations for some cases.
        """
    )

def predictionPage():
    image_path = st.file_uploader("Choose an image from your device", type=['jpg', 'png'])
    col1, col2 = st.columns(2)
    
    if image_path is not None:
        st.success("Inference run completely!")
        with col1:
            img = Image.open(image_path)
            st.image(img)
            predicted_img, recipes = pred.predictions(img)
        

        with col2:
            st.image(predicted_img, caption="Detected objects on the image")
        
        st.markdown("---")
        if not recipes.empty:
            st.write("## Recommended Food Recipes")
            st.markdown("---")
            for _, recipe in recipes.iterrows():
                st.write(f"### {recipe['Recipe']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Ingredients:**\n{recipe['Ingredients']}")
                    st.write(f"**Directions:**")
                    st.write(f"{recipe['Directions']}")
                # st.write(f"**Nutrition:**\n{recipe['Nutrition']}")
                with col2:
                    st.write("**Nutrition Information**")
                    fig = ntp.parse_nutrition(recipe['Nutrition'])
                    st.plotly_chart(fig)
                # st.table(ntp.parse_nutrition(recipe['Nutrition']))
                st.markdown("---")
        else:
            st.error("No food matched the available ingredients.")

        
    else:
        pass
        
def main():


    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", "Try Demo"], 
            icons=['house', 'play'], menu_icon="cast", default_index=0)
    
    if selected == "Home":
        homePage()
    if selected == "Try Demo":
        predictionPage()


    

if __name__ == '__main__':
    main()