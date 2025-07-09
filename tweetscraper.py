from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import time
import random
import os
from T2json import save_tweets_as_json
from Elements import ElementsStr
from names import names

from Responsemessages import Responsemesssage

init(autoreset=True)

#email = animerealm15@gmail.com
#pass = 
json_dir = "JSONfiles"
email = "kkdrama35@gmail.com"
user_pass = "kk@drama#kkdrama$35"
username = "EncryptedLaura"
# email = "codecrush23@gmail.com"
# user_pass = "code@crush#23"
# username = "curious_co78120"
credentials = [
    {"email": "kkdrama35@gmail.com", "user_pass": "kk@drama#kkdrama$35", "username": "EncryptedLaura"},
    {"email": "headlinehunters01@gmail.com", "user_pass": "headline@hunter@01", "username": "MehtaUnfiltered"},
    {"email": "animerealm15@gmail.com", "user_pass": "anime@realm#15", "username": "DCryptaris86649"},
]

output_dir = "HtmlFile"
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")

driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

links = {
    # "pay_for_this":"https://x.com/search?q=I%20will%20pay%20for%20this&src=typed_query&f=live",
        #  "SEO":"https://x.com/search?q=I%20Need%20Seo&src=typed_query&f=live",
        #  "Want_web":"https://x.com/search?q=I%20want%20a%20website&src=typed_query&f=live",
         "NEED_WEB":"https://x.com/search?q=I%20Need%20a%20website&src=typed_query&f=live"}

login_url = "https://x.com/search?q=I%20will%20pay%20for%20this&src=typed_query&f=live"
# driver.get(login_url)

print("Page loaded.")

# Wait for the page to load
time.sleep(3)
# function to get random sleep time
def GetSleepTime(max):
    return random.randint(5, max)

def StartScrape():
    try:
        logged_in = False
        for key in links:
            selected_cred = random.choice(credentials)
            # Assign values to variables
            email = selected_cred[names.email]
            user_pass = selected_cred[names.user_pass]
            username = selected_cred[names.username]
            driver.get(links[key])
            timeline_div = None
            if not logged_in:
                time.sleep(5)
            for i in range(5):
                try:
                    timeline_div = driver.find_element(By.XPATH, ElementsStr.timeline)
                except:
                    pass
                if timeline_div:
                    break
                time.sleep(1)
            if not timeline_div:
                logged_in = False
            if not logged_in:
                loginresp = LogIn(email,user_pass,username)
                if loginresp[names.status] == 400:
                    return loginresp
                logged_in = True
            print("getting data")
            time.sleep(10)
            GetData(key)
        print("data fetched")
        return {names.status:200 ,names.message: Responsemesssage.SCRAPING_SUCCESS}
    except Exception as e:
        return {names.status:400 ,names.message: Responsemesssage.SCRAPING_FAILED + str(e)}

#******************************************** SAVE DATA FUNCTIONS ********************************************

# function to save html content
def SaveHtml(current_scroll,file_name):
    max_retries = 10
    retries = 0

    try:
        print(f"{Fore.GREEN}Attempting to save HTML for scroll {current_scroll}...")
        while retries < max_retries:
            try:
                json_dir = "JSONfiles"
                timeline_div = driver.find_element(By.XPATH, ElementsStr.timeline)
                timeline_html = timeline_div.get_attribute(ElementsStr.outerhtml)
                file_name = f"data{file_name}{current_scroll}"

                save_tweets_as_json(timeline_html, file_name, json_dir=json_dir)
                
                # os.makedirs(output_dir, exist_ok=True)

                # with open(f'HtmlFile/data{file_name}{current_scroll}.html', "w", encoding="utf-8") as file:
                #     file.write(timeline_html)

                print(f"{Fore.CYAN}Timeline HTML saved to data{file_name}{current_scroll}.html")
                return {names.status: 200, names.message: Responsemesssage.HTML_SAVED}

            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    print(f"{Fore.RED}HTML SAVE FAILED: {str(e)}")
                    return {names.status: 400, names.message: Responsemesssage.HTML_SAVE_FAILED + str(e)}
                print(f"{Fore.YELLOW}Timeline div not found, retrying in 1 second... Attempt {retries}/{max_retries}")
                time.sleep(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return {names.status: 400, names.message: Responsemesssage.HTML_SAVE_FAILED + str(e)}

#******************************************** GET DATA FUNCTIONS ********************************************

def smooth_scroll(driver, distance, duration):
    """ Function to scroll smoothly by incrementally moving down the page. """
    scroll_step = random.uniform(8, 16)
    steps = int(distance / scroll_step)
    for i in range(steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(duration / steps)  # Sleep to spread out the scrolling time
#function to get html from page
def GetData(file_name):
    try:
        print(f"{Fore.GREEN}Calculating height...")
        time.sleep(random.uniform(5.0, 10.0))
        last_height = driver.execute_script(ElementsStr.getheight)
        max_scrolls = 20
        current_scroll = 0

        while current_scroll < max_scrolls:
            print(f"{Fore.YELLOW}Inside while loop, scroll {current_scroll + 1}/{max_scrolls}...")
            saveresp = SaveHtml(current_scroll,file_name)
            if saveresp[names.status] == 400:
                return saveresp
            
            scroll_duration = random.uniform(1.0, 3.0)
            distance_to_scroll = driver.execute_script(ElementsStr.disttoscroll)
            smooth_scroll(driver, distance_to_scroll, scroll_duration)
            
            print(f"{Fore.CYAN}Scrolled smoothly to bottom, waiting for {scroll_duration:.2f} seconds...")
            time.sleep(scroll_duration)
            
            new_height = driver.execute_script(ElementsStr.getheight)
            if new_height == last_height:
                print(f"{Fore.RED}No more content to load.")
                break
            last_height = new_height
            current_scroll += 1

        print(f"{Fore.GREEN}GET DATA SUCCESS")
        return {names.status: 200, names.message: Responsemesssage.GET_DATA_SUCCESS}
    except Exception as e:
        print(f"{Fore.RED}GET DATA FAILED: {str(e)}")
        return {names.status: 400, names.message: Responsemesssage.GET_DATA_FAILED + str(e)}

#******************************************** LOGIN FUNCTIONS ********************************************
#function to add email
def FillMail(user_mail):
    try:
        max_retries = 15
        retries = 0
        while retries < max_retries:
            try:
                email_input = driver.find_element(By.NAME, ElementsStr.textinput)
                email_input.clear()
                email_input.send_keys(user_mail)
                print(f"{Fore.GREEN}Email field found and email entered.")
                break
            except:
                retries += 1
                print(f"{Fore.YELLOW}Email input field not found, retrying in 1 second...")
                time.sleep(1)

        if retries >= max_retries:
            return {names.status: 200, names.message: Responsemesssage.FILL_EMAIL_SUCCESS}
        while True:
            try:
                next_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, ElementsStr.mailbtn)))
                print(f"{Fore.GREEN}Next button is clickable.")
                next_button.click()
                print(f"{Fore.CYAN}Clicked the next button.")
                return {names.status: 200, names.message: Responsemesssage.FILL_EMAIL_SUCCESS}
            except:
                print(f"{Fore.YELLOW}Next button not clickable, retrying in 1 second...")
                time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return {names.status: 400, names.message: Responsemesssage.FILL_EMAIL_FAILED+ str(e)}
#fill Username
def FillUsername(user_username):
    max_retries = 5
    retries = 0

    try:
        while True:
            try:
                input_field = driver.find_element(By.XPATH, ElementsStr.usenameinput)
                input_field.clear()
                input_field.send_keys(user_username)
                print(f"{Fore.GREEN}Username field found, cleared, and username entered.")
                break
            except:
                retries += 1
                if retries >= max_retries:
                    print(f"{Fore.RED}Username input field not found within the allowed time.")
                    return {names.status: 400, names.message: "Username input field not found within the allowed time"}
                print(f"{Fore.YELLOW}Username input field not found, retrying in 1 second...")
                time.sleep(1)
        while True:
            try:
                next_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ElementsStr.usernamebtn)))
                print(f"{Fore.GREEN}Next button is clickable.")
                next_button.click()
                print(f"{Fore.CYAN}Next button clicked.")
                return {names.status: 200, names.message: Responsemesssage.USERNAME_ADDED}
            except:
                print(f"{Fore.YELLOW}Next button not clickable, retrying in 1 second...")
                time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return {names.status: 400, names.message: Responsemesssage.USERNAME_NOT_FOUND+str(e)}

#fill password
def FillPassword(user_password):
    try:
        max_retries = 15
        retries = 0
        while True:
            try:
                password_input = driver.find_element(By.NAME, ElementsStr.passinput)
                password_input.clear()
                password_input.send_keys(user_password)
                print(f"{Fore.GREEN}Password field found, cleared, and password entered.")
                break
            except:
                retries += 1
                print(f"{Fore.YELLOW}Password input field not found, retrying in 1 second...")
                time.sleep(1)

        while True:
            try:
                login_button = driver.find_element(By.XPATH,ElementsStr.loginbtn)
                print(f"{Fore.GREEN}Login button is clickable.")
                login_button.click()
                print(f"{Fore.CYAN}Login button clicked.")
                return {names.status: 200, names.message: Responsemesssage.PASS_FILLED}
            except:
                print(f"{Fore.YELLOW}Login button not clickable, retrying in 1 second...")
                time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return {names.status: 400, names.message: Responsemesssage.PASS_NOT_FILLED+str(e)}
#function for logging in
def LogIn(email,user_pass,username):
    try:
        
        nameresp = FillMail(email)
        print(nameresp[names.message])
        usernameresp = FillUsername(username)
        print(usernameresp[names.message])
        passresp= FillPassword(user_pass)
        print(passresp[names.message])
        print("Login button clicked.")
        return {names.status:200 ,names.message: Responsemesssage.LOGIN_SUCCESS + username}
    except Exception as e:
        return {names.status:400 ,names.message: Responsemesssage.LOGIN_FAILED + str(e)}

scrapingresp = StartScrape()
print(scrapingresp[names.message])