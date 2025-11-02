DataSource:
github link : https://github.com/PhonePe/pulse
commit used : ec45c24 (March 04, 2025 snapshot)
commit link : https://github.com/PhonePe/pulse/commit/ec45c246a23382d40a1807a8e1019b571b0b4173

The datas were extracted and preprocessed into structured CSVs available in the `preprocessed_data_frames.zip` file.

The paths used in p_2_extraction_code.ipynb and p_2_preprocessing_code.ipynb is NOT Relative paths, so 

setup:
    Unzip the dataset — make sure the folder named preprocessed_data_frames is inside the main project folder (same level as app.py), since the path used in this is Relative.


required libraries for the app:
    streamlit
    pandas
    plotly
    pyngrok

Run the app using this command in your terminal or VS Code:
    streamlit run app.py

