import streamlit as st
import pandas as pd

# Define a list of months
MONTH_LIST = ["January", 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

def find_zodiac(month, day):
    """
    Determine the zodiac sign based on the provided month and day.

    Parameters:
    month (str): The month of birth (e.g., 'January').
    day (int): The day of birth.

    Returns:
    str: The zodiac sign corresponding to the provided date.
    """
    if month == 'december':
        astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 'january':
        astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
    elif month == 'february':
        astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
    elif month == 'march':
        astro_sign = 'Pisces' if (day < 21) else 'Aries'
    elif month == 'april':
        astro_sign = 'Aries' if (day < 20) else 'Taurus'
    elif month == 'may':
        astro_sign = 'Taurus' if (day < 21) else 'Gemini'
    elif month == 'june':
        astro_sign = 'Gemini' if (day < 21) else 'Cancer'
    elif month == 'july':
        astro_sign = 'Cancer' if (day < 23) else 'Leo'
    elif month == 'august':
        astro_sign = 'Leo' if (day < 23) else 'Virgo'
    elif month == 'september':
        astro_sign = 'Virgo' if (day < 23) else 'Libra'
    elif month == 'october':
        astro_sign = 'Libra' if (day < 23) else 'Scorpio'
    elif month == 'november':
        astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
    return astro_sign

@st.cache_data
def load_data(data):
    """
    Load the dataset from a CSV file.

    Parameters:
    data (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded pandas DataFrame.
    """
    return pd.read_csv(data)

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Zodiac Application")
    
    # Load the dataset
    df = load_data('data/zodiac_data.csv')

    # Define the sidebar menu
    menu = ['Home', 'About']
    choice = st.sidebar.selectbox("Menu", menu)

    # Manage page navigation based on sidebar menu choice
    if choice == 'Home':
        st.subheader("Home")

        # User input for date of birth
        dob = st.date_input("Date of Birth")
        month_of_birth = st.selectbox("Month", MONTH_LIST)
        day_of_birth = st.number_input("Date", min_value=1, max_value=31)

        # Predict zodiac sign when the button is clicked
        if st.button("Predict"):
            result = find_zodiac(month_of_birth.lower(), day_of_birth)
            st.success("Results")
            st.write(f"You Are {result}")
			
            zdf = df[df['horoscope'] == result.title()]
            st.write(f"Alias: {zdf.iloc[0].aliasname}")
			
            rcol1, rcol2, rcol3 = st.columns([2, 1, 1])

            with rcol1:
                st.info("Description")
                st.write(zdf.iloc[0].description)

            with rcol2:
                with st.expander("Positives"):
                    st.write(zdf.iloc[0].positives.split(','))

            with rcol3:
                with st.expander("Negatives"):
                    st.write(zdf.iloc[0].negatives.split(','))

    elif choice == 'About':
        st.subheader("About")

if __name__ == '__main__':
    main()
