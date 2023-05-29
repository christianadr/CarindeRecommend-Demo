import streamlit as st
import torch
import recommender as rec
from PIL import Image, ImageDraw, ImageFont

@st.cache_resource
def load_model():
    model = torch.hub.load("ultralytics/yolov5", "custom", path="models/best.pt")
    return model

def detection(image):
    
    model = load_model()
    """ Run detection on given image using custom YOLOv5 model 
        and return the image with respective bounding boxes. """

    results = model([image])
    
    boxes = results.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax']].values.tolist()
    labels = results.pandas().xyxy[0]['name'].tolist()
    confidences = results.pandas().xyxy[0]['confidence'].tolist()

    image_with_bb = draw_bounding_boxes(image, boxes, labels, confidences)

    return image_with_bb, labels

def draw_bounding_boxes(image, boxes, labels, confidences):

    """ Drawing bounding boxes on detected objects on image """
    
    draw = ImageDraw.Draw(image)
    font_size = max(1, int(image.width / 100))  # Adjust the divisor as needed

    for box, label, confidence in zip(boxes, labels, confidences):
        draw.rectangle(box, width=5, outline='red')
        # font = ImageFont.truetype(size=font_size)
        text = f"{label}: {confidence:.2f}"
        text_width, text_height = draw.textsize(text)
        draw.rectangle((box[0], box[1] - text_height - 5, box[0] + text_width + 5, box[1]), fill='red')
        draw.text((box[0] + 2, box[1] - text_height - 3), text, fill='white')
    
    return image

def predictions(image_path):
    image = image_path
    predicted_img, labels = detection(image)

    fr = rec.FoodRecommender("assets/filipino_recipes.xlsx")
    fr.preprocess_data()
    fr.compute_recipe_profiles()
    top_recipes = fr.get_top_recipes(labels, n=3)
    return predicted_img, top_recipes
