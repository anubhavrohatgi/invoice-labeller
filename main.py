import time

import streamlit as st
import json
from PIL import Image
from helper import load_data
import tkinter as tk
from tkinter import filedialog
from code_editor import code_editor

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)


def json_editor(json_data):
    st.text("Edit JSON:")
    response_dict = code_editor(json.dumps(json_data, indent=4), lang="json", height=500, options={"wrap": True})

    # json_str = st.text_area("", json.dumps(json_data, indent=4), height=700)
    try:
        edited_json = json.loads(response_dict['text'])

    except json.JSONDecodeError:
        st.warning(f"Invalid JSON syntax : {response_dict['text']}")
        return None
    return edited_json


def display_image(image_path, caption):
    image = Image.open(image_path)
    st.image(image, caption=caption, use_column_width=True)


def main():
    st.set_page_config(page_title="Json Image Pair Reviewer",
                       page_icon=":microscope:",
                       layout="wide")
    st.markdown("<h1 style='text-align: center;color: white;'>Json Editor</h1>", unsafe_allow_html=True)

    dir_name = None
    with st.sidebar:
        st.write('Please select Data folder:')
        clicked = st.button('Load Folder')
        if clicked:
            dir_name = filedialog.askdirectory(master=root)
            dir_name = st.text_input('Selected folder:',
                                     dir_name if dir_name != "()" else "None")

    if dir_name is not None and dir_name != "()":
        print(dir_name)
        with st.spinner("Please wait while we load the data ..."):
            records, not_found = load_data(dir_name)
            alert = st.success(f"Total records loaded : {len(records)}")
            time.sleep(5)
            alert.empty()
        # st.warning(f"Records that were not readable : {not_found}")

    # Sample JSON data
    sample_json = {
        "image1": "/home/anubhav/Downloads/review-20231214T162853Z-001/done/9364069016.jpg",
        "image2": "/home/anubhav/Downloads/review-20231214T162853Z-001/done/9364069016.jpg",
        # Add more images as needed
    }

    # Display JSON editor and corresponding image side by side
    st.text("Side-by-Side View:")
    col1, col2 = st.columns([1, 1], gap="medium")

    # JSON editor in the first column
    with col1:
        st.text("Column 1: JSON Editor")
        edited_json = json_editor(sample_json)

    # Corresponding image in the second column
    with col2:
        st.text("Column 2: Corresponding Image")
        if sample_json is not None:
            for key, image_path in sample_json.items():
                st.write(f"**{key}:**")
                display_image(image_path, f"Caption for {key}")


if __name__ == "__main__":
    main()
    # load_data("/home/anubhav/Downloads/review-20231214T162853Z-001/review/")
