import io
import streamlit as st
import boto3
import json
import pandas as pd
import numpy as np
import base64
import logging
from io import BytesIO
from PIL import Image
from utils import *
from constants import *
import multiprocessing
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from botocore.exceptions import ValidationError, ClientError


similar_post_texts = ""
product_input = ""
recommendations = ""
webcam_on = False
st.set_page_config(layout="wide")

###########################
# Streamlit app widgets  #
###########################

col1, col2 = st.columns([1, 3])

# Image column
with col1:
    st.write("  ")
    st.image("icon.png", width=150, caption='')

# Title column
with col2:
    st.title('Social Media Assistant')


# Add dropdowns in the left sidebar
with st.sidebar:
    # User text input 
    text_input = st.text_input('Enter your image enhancement prompt, such as: Christmas tree, holiday decoration, warm lights', value='Christmas tree, holiday decoration, warm lights')
    product_input = st.text_input('Enter your product object, such as: bag, car, perfume etc.', value='bag')

    ########
    # File upload
    uploaded_file = st.file_uploader('Upload a product image')
    
        
    ########
    # Camera input capability 
    
    if "show_camera" not in st.session_state:
        st.session_state.show_camera = False

    # Create a button to toggle the camera view
    if st.button("Show/Hide Camera"):
        st.session_state.show_camera = not st.session_state.show_camera

    # Check if the camera view should be shown
    if st.session_state.show_camera:
        # Camera input
        img_file_buffer = st.camera_input("Take a picture")

        if img_file_buffer is not None:
            # To read image file buffer as a PIL Image:
            webcam_on = True
            webcam_img = Image.open(img_file_buffer)
            
            
     ########   
     # Select prepared image 
    
    import glob
    files = sorted(glob.glob("./sample_images/*.png"))
    names = [f.split("/")[-1].split(".")[0] for f in files]
    image_options = dict(zip(names, files))
    
 
    left_column, right_column = st.columns(2)
    with left_column:
        selected_image = st.selectbox('Or select image', [''] + list(image_options.keys()))
    with right_column:
        selected_position = st.selectbox('Position (advanced)', ['', 'top-left', 'top-middle', 'top-right', 
                                             'middle-left', 'middle-middle', 'middle-right','bottom-left',
                                             'bottom-middle', 'bottom-right'])
    

    # Dropdown for brand style
    brand_df = pd.read_csv('brand_guideline.csv')
    brand = st.selectbox('Select Brand', ['']+ brand_df['Category'].tolist())
    
    # Load brand guideline
    
    if brand: 
        selected_row = brand_df[brand_df['Category'] == brand]

        # Extract the data from the selected row
        visual_style = selected_row['Visual Style'].values[0]
        tone = selected_row['Tone of Voice'].values[0]
        hashtag = selected_row['Hashtags and Tags'].values[0]
        copywriting = selected_row['Copywriting Style'].values[0]
        brand_messageing = selected_row['Brand Messaging'].values[0]

        # Display the data
        st.write(f"Visual Style: {visual_style}")
        st.write(f"Tone of Voice: {tone}")
        st.write(f"Hashtags and Tags: {hashtag}")
        st.write(f"Copywriting Style: {copywriting}")
        st.write(f"Brand Messaging: {brand_messageing}")
 
    

    # Dropdown for style
    style = st.selectbox('Image Style', ['Photographic', 'Cinematic'])
    

    if 'submit' not in st.session_state:
        st.session_state.submit = False

    def click_submit():
        st.session_state.submit = True

    button = st.button('Submit', on_click=click_submit)



col3, col4 = st.columns(2)

with col3:  
        
    if selected_image or uploaded_file or webcam_on:
        st.write('Initial Image:')

        if selected_image:
            image_path = image_options[selected_image]
            if selected_position:
                positioned_image = create_positioned_image(image_path, selected_position)
                caption = f"{selected_image} at {selected_position}"
                inital_image = st.image(positioned_image, caption=caption, width=600)
            else:
                caption = selected_image
                inital_image = st.image(image_path, caption=caption, width=600)

        elif uploaded_file:
            uploaded_file = resize_image(uploaded_file)
            if selected_position:
                positioned_image = create_positioned_image(uploaded_file, selected_position)
                caption = f"uploaded file at {selected_position}"
                inital_image = st.image(positioned_image, caption=caption, width=600)
            else:
                inital_image = st.image(uploaded_file, caption='uploaded file', width=600)

        elif webcam_on:
            webcam_file = resize_webcam_image(webcam_img)
            if selected_position:
                positioned_image = create_positioned_image(webcam_file, selected_position)
                caption = f"webcam file at {selected_position}"
                inital_image = st.image(positioned_image, caption=caption, width=600)
            else:
                inital_image = st.image(webcam_file, caption='webcam file', width=600)
    
    

###########################
# LLM model invokation  #
###########################     

# image enhancement 
image_enhanced = 0
        
with col4:
    if text_input and product_input and brand: 
        outpaint_prompt = style + "style, " + visual_style + " , " + text_input
        mask_prompt = product_input
        negative_prompt = "bad quality, unrealistic, outdated, blurry, noisy, unattractive, sloppy, "

        if button:
            with st.spinner("Drawing..."):
                print(type(inital_image))

                if selected_image:
                    if selected_position:
                        image_str = image_to_base64(upload_file = positioned_image)
                    else:
                        image_str =  image_to_base64(image_path= image_options[selected_image])
                if uploaded_file:
                    if selected_position:
                        image_str = image_to_base64(upload_file = positioned_image)
                    else:
                        image_str =  image_to_base64(upload_file= uploaded_file)
                if webcam_on:
                    if selected_position:
                        image_str = image_to_base64(upload_file = positioned_image)
                    else:
                        image_str =  image_to_base64(upload_file= webcam_file)
                
                    
                try:
                    body = get_titan_ai_request_body(outpaint_prompt, negative_prompt, mask_prompt, image_str = image_str)
                    response = generate_image(model_id =MODEL_IMAGE, body = body)
                    image_enhanced = base64_to_image(response["images"][0])
                    
                    st.write('Enhanced Image:')
                    st.image(image_enhanced, width=600)
                except NameError as ne:
                    st.warning('Error! Upload an image or choose an image from the list', icon="⚠️")
                except ClientError as ce:
                    message = ce.response["Error"]["Message"]
                    st.warning(f'Error from model: {message}', icon="⚠️")
                    
                

# Initial post text generation    
post_text = ""    

role = "an expert in content generation" # for social media
# tone, hashtag, copywriting and brand_messageing retrieved from brand guidelines. 


if image_enhanced and product_input and brand:
    # Generate answer
    with st.spinner("Generating..."):
        initial_post_prompt = PROMPT_TEXT.format(role=role, product_name=product_input, target_brand=brand, 
                                                 tone=tone, hashtag = hashtag, copywriting= copywriting, brand_messageing = brand_messageing)
        print(initial_post_prompt)
        
        post_text = generate_text_with_claude(image = image_enhanced, prompt=initial_post_prompt)
        st.subheader("Enhanced post text")
        st.text_area("post_text", post_text)  
        print(post_text)


        
# Similar posts retrieval 
mapping_table = pd.read_csv('data_mapping.csv') 

index_name = "social-media-blog-img-text"
host = "ljqs6g4p3shfkalo08se.us-east-1.aoss.amazonaws.com"
service = 'aoss'
region_name = 'us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWSV4SignerAuth(credentials, region_name, service)

oss_client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300
)


if image_enhanced and post_text:
    with st.spinner("Retrieving Similar Posts..."):
        with BytesIO() as byte_io:
            image_enhanced.save(byte_io, format="PNG")
            image_enhanced_bytes = byte_io.getvalue()
        # query_prompt=post_text initially
        similar_images, post_texts = find_similar_items(image_bytes=image_enhanced_bytes, query_prompt=text_input + " " + post_text,
                                           k=5, num_results=3, index_name=index_name, dataset=mapping_table,
                                           open_search_client=oss_client)
        similar_post_texts = '\n'.join(f'<similar_post>\n{similar_post}\n</similar_post>' for similar_post in post_texts)
       
    
        col5, col6 = st.columns(2)
        with col5:
            st.subheader('Similar Posts:')
            st.image(similar_images[0], width=400)
            st.image(similar_images[1], width=400)
            st.image(similar_images[2], width=400)
            
        with col6:
            st.subheader("Historical post analysis")
            # Generate answer
            with st.spinner("Generating..."):
                
                analysis_text_0, analysis_text_1, analysis_text_2 = process_images(similar_images, PROMPT_ANALYSIS)
                st.text_area("post_texts_1", post_texts[0])
                st.markdown(parse_task_response(analysis_text_0)) #height=400
                st.markdown("""---""")
                st.text_area("post_texts_2", post_texts[1])
                st.markdown(parse_task_response(analysis_text_1))
                st.markdown("""---""")
                st.text_area("post_texts_3", post_texts[2])
                st.markdown(parse_task_response(analysis_text_2))  
                analysis_list = [analysis_text_0, analysis_text_1, analysis_text_2]
                recommendations = '\n'.join(f'<recommendation>\n{get_task2_response(txt)}\n</recommendation>' for txt in analysis_list)
                
if image_enhanced and post_text and analysis_text_0:
    with st.spinner("Generating final post..."):
        print("Final prompt")
        final_post_prompt = FINAL_PROMPT_TEXT.format(role=role, initial_post=post_text, similar_posts=similar_post_texts, 
                                                     recommendations=recommendations, product_name=product_input,tone=tone, hashtag = hashtag, 
                                                     target_brand=brand, copywriting= copywriting, brand_messageing = brand_messageing)
        
        print(final_post_prompt)

        final_post_text = generate_text_with_claude(image = image_enhanced, prompt=final_post_prompt)
        st.subheader("Final post text")
        st.text_area("initial_post_text", post_text)  
        st.image(image_enhanced, width=600)
        st.text_area("final_post_text", final_post_text)  
        print(final_post_text)


