import json
import streamlit as st

st.set_page_config(
    page_title="prettymapp", page_icon="🖼️", initial_sidebar_state="collapsed"
)
st.markdown("# Prettymapp")

with open("./streamlit-prettymapp/examples.json", "r") as f:
    EXAMPLES = json.load(f)

if not st.session_state:
    st.session_state.update(EXAMPLES["DeepDive"])
    st.session_state["previous_example_index"] = 0

example_image_pattern = "streamlit-prettymapp/example_prints/{}_small.png"
example_image_fp = [
    example_image_pattern.format(name.lower()) for name in list(EXAMPLES.keys())[:4]
]

# Create a custom tile layout
num_examples = 4
tile_cols = st.columns(num_examples)

# Display example images as tiles and make them clickable
example_images = {}
button_text = ["Pro User", "Company Comparison", "Deep Dive", "Topic Inference"]
j = 0
for i, example_name in enumerate(list(EXAMPLES.keys())[:num_examples]):
    example_image_path = example_image_pattern.format(example_name.lower())
    with tile_cols[i]:
        st.image(example_image_path, use_column_width=True)
        clicked = st.button(button_text[j], key=f"example_tile_{i}")
        example_images[example_name] = example_image_path
        j = j + 1
        if clicked:
            st.session_state.update(EXAMPLES[example_name].copy())
            st.session_state["previous_example_name"] = example_name
            st.session_state["previous_example_index"] = i

# Create a dropdown for selecting the example
selected_example = st.selectbox(
    "User Type",
    list(example_images.keys()),
    index=st.session_state.get("previous_example_index", 0),
    key="example_dropdown",
)

# Create a text box for displaying the selected example details
example_details = st.text_area(
    "Question",
    value=json.dumps(EXAMPLES[selected_example], indent=2),
    height=200,
    key="example_details",
)

# Update session state if a different example is selected from the dropdown
if selected_example != st.session_state.get("previous_example_name"):
    st.session_state.update(EXAMPLES[selected_example].copy())
    st.session_state["previous_example_name"] = selected_example
    st.session_state["previous_example_index"] = list(example_images.keys()).index(selected_example)

st.write("")
form = st.form(key="form_settings")
col1, col2, col3 = form.columns([3, 1, 1])

form.form_submit_button(label="Submit")