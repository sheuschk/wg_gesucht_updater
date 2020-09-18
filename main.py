from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import argparse


def init_parser():
    """ Parse arguments for the script"""
    parser = argparse.ArgumentParser(description='Update all wg_gesucht offers')
    parser.add_argument("--mail", '-m', help="Enter your wg gesucht mail")
    parser.add_argument("--pw", '-pw', help="Enter your wg gesucht pw")

    args = parser.parse_args()

    # 5 params are the name of the script the mail and pw with their tags
    if len(sys.argv) != 5:
        sys.stdout.write('Not all parameters given')
        exit()

    return args


def init_driver():
    """ Initialize the web driver for the headless browser"""
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.wg-gesucht.de/')
    return driver, wait


def accept_cookies(wait):
    """ If necessary accept the cookies"""
    try:
        cookie_btn = wait.until(EC.visibility_of_element_located((By.ID, 'cmpwelcomebtnyes')))
        cookie_btn.click()
        time.sleep(3)
    except TimeoutException:
        sys.stdout.write('Cookies already accepted\n')


def login(driver, wait, args):
    """ Login to wg gesucht with the parsed arguments"""
    try:
        login = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'LOGIN')))
        login.click()
    except:
        sys.stdout.write('Login button was moved')
        driver.close()
        exit()
    time.sleep(1)

    mail = driver.find_element_by_id('login_email_username')
    mail.click()
    mail.send_keys(args.mail)
    pw = driver.find_element_by_id('login_password')
    pw.click()
    pw.send_keys(args.pw)
    driver.find_element_by_id('login_submit').click()
    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'profile_image_menu')))
    except TimeoutException:
        sys.stdout.write('Credentials were wrong or server is not responding\n')
        exit()

    sys.stdout.write('Logged in\n')


def update_all_offers(driver):
    """ Find all offers an iterate through the active once"""
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    wrapper = driver.find_element_by_id('my_offers')
    list_offers = wrapper.find_element_by_id('list_group_offers')
    offers = list_offers.find_elements_by_class_name('list-group-item')

    # Update every offer

    offers_ids = []
    for offer in offers:
        offer_class = offer.get_attribute("class")
        raw_id = offer.get_property('id')
        if 'list-group-item-deactivated' in offer_class:
            sys.stdout.write(f"Offer: {raw_id[3:]} is deactivated\n")
        else:
            offers_ids.append(raw_id[3:])

    for index, offer in enumerate(offers_ids):
        update_offer(driver, offers_ids, index)


def update_offer(driver, offers_ids, index):
    """ Open the offer and update it"""
    offer_id = offers_ids[index]

    # get to the update page
    link = f"/angebot-bearbeiten.html?action=update_offer&offer_id={offer_id}"
    driver.get(f'https://www.wg-gesucht.de/{link}')
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)

    # Update it
    driver.find_element_by_id('update_offer').click()
    time.sleep(1)

    sys.stdout.write(f'Updated {offer_id}\n')


if __name__ == '__main__':
    """ Start the script and execute all necessary steps """
    args = init_parser()
    driver, wait = init_driver()
    time.sleep(1)
    accept_cookies(wait)
    login(driver, wait, args)
    update_all_offers(driver)
    sys.stdout.write('Successfully finished\n')

    # Shut down browser
    driver.close()
