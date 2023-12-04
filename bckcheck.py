import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser
from PIL import Image
from io import BytesIO

def get_horoscope_by_day(zodiac_sign: int, day: str):
    if not "-" in day:
        res = requests.get(
            f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}")
    else:
        day = day.replace("-", "")
        res = requests.get(
            f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={zodiac_sign}&laDate={day}")
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    return data.p.text


def get_horoscope_by_week(zodiac_sign: int):
    res = requests.get(
        f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-weekly.aspx?sign={zodiac_sign}")
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    return data.p.text


def get_horoscope_by_month(zodiac_sign: int):
    res = requests.get(
        f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-monthly.aspx?sign={zodiac_sign}")
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    return data.p.text

def set_background():
    img_url = "https://scontent.fsgn4-1.fna.fbcdn.net/v/t1.15752-9/400586626_249503654806842_301230259282390311_n.png?_nc_cat=101&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeGrWoQzi_LR1rqknZg0qACEPTiJAwwRNgk9OIkDDBE2Ce2Wi8wdEOiONKMtPtPpb4LJvxsxGiDBMRu6Hkhzcsh9&_nc_ohc=t8m7WwBE3UIAX9sqObx&_nc_ht=scontent.fsgn4-1.fna&oh=03_AdSPNpEByo1yNlWGqlnFtPipbS8QUyOLc6qoKFg74U6bYQ&oe=65842162"  
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("{img_url}");
        background-size: 99%;
        background-repeat: no-repeat;
        background-attachment: local;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    set_background()
    
    #intro 
    st.title("Daily Horoscopes")
    st.text("'Get your free daily, weekly, monthly, yearly horoscopes reading'")
    #menu
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", "Forecast", "Contact Us", "About Us"], 
            icons=['house', 'date', 'email', 'calling'], menu_icon="cast", default_index=1)
        selected

    #contact us 
    if selected == "Contact Us":
        webbrowser.open_new_tab("https://www.facebook.com/profile.php?id=61553564769648")

    #Forecast
    if selected == "Forecast":
        # zodiac sign dropdown
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        selected_sign = st.selectbox("Choose Your Zodiac Sign", signs)
        zodiac_sign = signs.index(selected_sign) + 1

        # horoscope period radio
        horoscope_period = st.radio("Choose the Horoscope Period", ["Daily", "Weekly", "Monthly"])

        # horoscope result
        horoscope = ""

        if horoscope_period == "Daily":
            day = st.date_input("Choose the date for daily horoscope")
            if day:
                try:
                    horoscope = get_horoscope_by_day(zodiac_sign, day.strftime("%Y-%m-%d"))
                except requests.RequestException as e:
                    st.error(f"Failed to retrieve horoscope: {e}")
        elif horoscope_period == "Weekly":
            horoscope = get_horoscope_by_week(zodiac_sign)
        elif horoscope_period == "Monthly":
            horoscope = get_horoscope_by_month(zodiac_sign)

        if horoscope:
            st.success(f"{selected_sign} Horoscope for {horoscope_period.lower()} period:\n{horoscope}")
    
    #Home - Check Zodiac 
    if selected == "Home":
        zodiac_images = {
    "Aries": "https://s.net.vn/3gvx",
    "Taurus": "https://s.net.vn/k94g",
    "Gemini": "https://s.net.vn/8h7i",
    "Cancer": "https://s.net.vn/Pj7s",
    "Leo": "https://s.net.vn/jhxs",
    "Virgo": "https://s.net.vn/ZMx4",
    "Libra": "https://s.net.vn/6eRu",
    "Scorpio": "https://s.net.vn/kr84",
    "Sagittarius": "https://s.net.vn/f070",
    "Capricorn": "https://s.net.vn/T7HU",
    "Aquarius": "https://s.net.vn/9N1X",
    "Pisces": "https://s.net.vn/CXoV"
}

        def get_zodiac_sign(day, month):
            if (month == 3 and day >= 21) or (month == 4 and day <= 19):
                return "Aries"
            elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
                return "Taurus"
            elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
                return "Gemini"
            elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
                return "Cancer"
            elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
                return "Leo"
            elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
                return "Virgo"
            elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
                return "Libra"
            elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
                return "Scorpio"
            elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
                return "Sagittarius"
            elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
                return "Capricorn"
            elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
                return "Aquarius"
            else:
                return "Pisces"

        
        st.title("What is your Zodiac?")

        # Birthday's user input 
        birthday = st.date_input("Your birthday: ")

        if st.button("Let's Find"):
            # Take user's birthday
            day = birthday.day
            month = birthday.month

            # Determine Zodiac 
            zodiac_sign = get_zodiac_sign(day, month)

            # Image Visualization based on Zodiac 
            if zodiac_sign in zodiac_images:
                st.write(f"{zodiac_sign}:")
                response = requests.get(zodiac_images[zodiac_sign])
                image = Image.open(BytesIO(response.content))              
                st.image(image, caption=zodiac_sign, use_column_width=True)

if __name__ == "__main__":
    main()