import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser
import base64
from PIL import Image
from io import BytesIO

# Forecast Function 
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

# Background
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background():
    img = get_img_as_base64("Background.png")
    page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img}");
        background-size: 100%;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        </style>
        """ 
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Tarot 
    # Function to display the image and card details
def display_random_card( card_meaning):
    st.write(f"{card_meaning}")

    # Using the sample method to get a random row from tarot_data
def get_random_card(tarot_data):
    return tarot_data.sample().iloc[0]

# Main
def main():
    set_background()
    
    # Intro 
    st.title("Daily Horoscopes")
    st.text("'Get your free daily, weekly, monthly, yearly horoscopes reading!'")

    # Menu
    with st.sidebar:
        selected = option_menu(
            menu_title = None, 
            options = ["Home", "Forecast", "Astrology Zodiac Signs" ,"Contact Us", "About Us", "Tarot"], 
            icons = ['house', 'cloud-sun', 'star', 'envelope', 'info-circle', "gem"],
            menu_icon = "cast", 
            default_index = 0,
            styles = {
                "container": {"padding": "0!important", "background-color": "#0d0c0c"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#808080",
                },
                "nav-link-selected": {"background-color": "grey"},
            },
        )
    #About us 
    if selected == "About Us":
        st.title("About Us - Stellar")
        st.write("Welcome to Stellar, your celestial companion on the journey through the cosmic tapestry. At Stellar, we believe in the profound connection between individuals and the celestial forces that shape their destinies. As a leading Daily Horoscope Web Service, we empower users to navigate life's twists and turns with insights drawn from the stars themselves.")
        
        # Sử dụng cột để sắp xếp ảnh và văn bản
        col1, col2 = st.columns([1, 3])
    
        # Hiển thị ảnh trong cột 1
        with col1:
            st.image("https://scontent-hkg4-1.xx.fbcdn.net/v/t1.15752-9/376576294_1024187448862555_8898121516945095085_n.png?_nc_cat=109&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeHbeyz6QuAy7_XXvSPgEx_YGWPE2KxmrbIZY8TYrGatskiOlVn3cqtoyze9DpoZrPs2LYmt7qogJ_56fo933Bzo&_nc_ohc=it9hmFoSwAkAX_zWQCJ&_nc_ht=scontent-hkg4-1.xx&oh=03_AdR7G3ILyHR2O7_I8qXh-BlX1msgY7Aj98rjnJcXf_ltAQ&oe=6593F35D", caption='Stellar Image')
    
        # Hiển thị văn bản trong cột 2
        with col2:
            st.header("Our Offerings:")
            
            offerings = {
                "Daily Horoscope Readings": "Find your zodiac sign, and let the universe unfold its secrets. Our daily horoscope readings provide personalized guidance tailored to your unique cosmic imprint, helping you seize the opportunities and overcome challenges that each day presents.",
                "Timeless Insights": "Delve deeper into the cosmic currents with our weekly, monthly, and yearly forecasts. Uncover the patterns that shape your life over extended periods, allowing you to make informed decisions and align with the cosmic energies surrounding you.",
                "Tarot Readings": "Unlock the mystical realm with our Tarot Reading feature. Explore the ancient art of divination and gain profound insights into your past, present, and future. Our Tarot readings offer a captivating glimpse into the unseen forces that influence your journey.",
                "Astrology Zodiac Sign Exploration": "Dive into the rich tapestry of astrology by exploring the characteristics and traits associated with your zodiac sign. Discover the nuances that make you uniquely you and gain a deeper understanding of the cosmic energies that shape your personality."
            }
            
            for offering, description in offerings.items():
                st.subheader(offering)
                st.write(description)
            
            st.header("Our Slogan:")
            st.write('"Apocalypse | Tarot | Astrology"')
            st.write("This powerful mantra embodies the essence of Stellar. We believe in empowering individuals to face life's challenges with strength and grace, drawing inspiration from the apocalypse, seeking guidance through the wisdom of tarot, and understanding the cosmic dance through astrology.")
    
            st.write("At Stellar, we are not just a Daily Horoscope Web Service; we are your cosmic confidants, guiding you through the celestial wonders that surround you. Join us on this extraordinary journey as we explore the mysteries of the universe together.")


    #Tarot 
    if selected == "Tarot":
        # Display the title and description
        st.title("Free Daily Tarot Card Reading")
        st.write("Discover our free daily tarot card reading and take a glimpse into the future. The perfect way to start your day.")
        user_name = st.text_input("Enter your name:")
        if user_name:
            st.success(f'Welcome to our daily tarot reading. Please select your cards, {user_name}!')
        else:
            st.warning('Enter your name, please!')

        # Read data from the CSV file
        tarot_data = pd.read_csv("Tarot-card-Trang-tính1.csv")

        # Display the tarot card images as buttons in a single row
        col1, col2, col3 = st.columns(3)

        # Display the image 1 as a button
        image_url_1 = "https://www.horoscope.com/images-US/tarot/back/daily-tarot-mood.png"
        col1.image(image_url_1, use_column_width=True)

        # Display the image 2 as a button
        image_url_2 = "https://www.horoscope.com/images-US/tarot/back/daily-tarot-love.png"
        col2.image(image_url_2, use_column_width=True)

        # Display the image 3 as a button
        image_url_3 = "https://www.horoscope.com/images-US/tarot/back/daily-tarot-career.png"
        col3.image(image_url_3, use_column_width=True)

        # Check if buttons are clicked
        button_1_clicked = col1.button("Card 1")
        button_2_clicked = col2.button("Card 2")
        button_3_clicked = col3.button("Card 3")

        # Display random card when buttons are clicked
        with col1:
            if button_1_clicked:
                selected_card_1 = get_random_card(tarot_data)
                st.image(selected_card_1['Image file'], caption=f"{selected_card_1['Name']}", use_column_width=True)
                display_random_card( selected_card_1['Meaning'])

        with col2:
            if button_2_clicked:
                selected_card_2 = get_random_card(tarot_data)
                st.image(selected_card_2['Image file'], caption=f"{selected_card_2['Name']}", use_column_width=True)
                display_random_card(selected_card_2['Meaning'])

        with col3:
            if button_3_clicked:
                selected_card_3 = get_random_card(tarot_data)
                st.image(selected_card_3['Image file'], caption=f"{selected_card_3['Name']}", use_column_width=True)
                display_random_card(selected_card_3['Meaning'])    

    # Contact us 
    if selected == "Contact Us":
        # Function to open the Facebook page
        def open_facebook_page():
            webbrowser.open_new_tab("https://www.facebook.com/profile.php?id=61553564769648")

        # Function to show the feedback form
        def show_feedback_form():
            st.header(":mailbox: Leave your feedback for us!")

            contact_form = """
            <form action="https://formsubmit.co/stellar.fbuser@gmail.com" method="POST">
             <input type="hidden" name="_captcha" value="false">
             <input type="text" name="name" placeholder="Your name" required>
             <input type="email" name="email" placeholder="Your email" required>
             <textarea name="message" placeholder="Your message here"></textarea>
             <button type="submit">Send</button>
        </form>
        """
            st.markdown(contact_form, unsafe_allow_html=True)

        # Use Local CSS File
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        local_css("style/style.css")

        # Create a button to toggle between Facebook page and feedback form
        selected_option = st.radio("Select an option:", ["Contact Us", "Feedback Form"])

        if selected_option == "Contact Us":
            st.button("Go to Facebook Page", on_click=open_facebook_page)
        elif selected_option == "Feedback Form":
            show_feedback_form()
    
    # Astrology Zodiac Signs
    if selected == "Astrology Zodiac Signs":
        selectedd = st.selectbox("Choose your Zodiac", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
        zodiac = st.radio("Select Option", ["Love", "Lifestyle", "Friendship", "Health"])

        url = f"https://www.horoscope.com/zodiac-signs/{selectedd.lower()}/{zodiac.lower()}"

        res = requests.get(url)

        content = BeautifulSoup(res.content, 'html.parser')

        sections = content.find_all(['h3', 'p'])

        displayed_text = ""
        for section in sections:
            if section.name == 'h3':
                displayed_text += f"<h3>{section.text}</h3>"
            elif section.name == 'p':
                displayed_text += f"<p>{section.text}</p>"

        st.markdown(displayed_text, unsafe_allow_html=True) 

    # Forecast
    if selected == "Forecast":
        # Zodiac sign dropdown
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        selected_sign = st.selectbox("Choose Your Zodiac Sign", signs)
        zodiac_sign = signs.index(selected_sign) + 1

        # Horoscope period radio
        horoscope_period = st.radio("Choose the Horoscope Period", ["Daily", "Weekly", "Monthly"])

        # Horoscope result
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
    
    # Home - Check Zodiac 
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

        # Method to get user's zodiac  
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
                st.balloons()

if __name__ == "__main__":
    main()