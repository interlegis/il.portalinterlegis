from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

def highlight(element):
    """Highlights (blinks) a Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)

def login(base_url, driver):
    driver.get(base_url + "/login")
    driver.find_element_by_id("__ac_name").clear()
    driver.find_element_by_id("__ac_name").send_keys("iladmin")
    driver.find_element_by_id("__ac_password").clear()
    driver.find_element_by_id("__ac_password").send_keys("zope e o que manda")
    driver.find_element_by_name("submit").click()
    driver.get(base_url + "/")

def fill(id, text):
    driver.find_element_by_id(id).clear()
    driver.find_element_by_id(id).send_keys(text)

def fill_carousel_panel(url, target, image, title, text):
    driver.get(url)
    driver.find_element_by_id("form-widgets-target-widgets-query").click()
    driver.find_element_by_id("form-widgets-target-widgets-query").send_keys(target)
    li = driver.find_element_by_tag_name('li')
    li.click()
    fill("form-widgets-image", image)
    fill("form-widgets-title", title)
    fill("form-widgets-text", text)
    driver.find_element_by_id("form-buttons-apply").click()

def fill_carousel(edit_link, data):
    driver.get(base_url + "/")
    driver.find_element_by_css_selector(edit_link).click()
    for i in range(len(data)):
        driver.find_element_by_id("carousel-add-button").click()
    links = driver.find_elements_by_class_name('editable-box-link-overlay')
    urls_carousels = [l.get_attribute('href') for l in links]
    for url, params in zip(urls_carousels, data):
        fill_carousel_panel(url, **params)
    driver.get(base_url + "/")

def populate_carousels():

    # Main Carousel
    fill_carousel("#carousel_0 a.editable-box-link", [
        dict(target="news",
             image="/++theme++il.portalinterlegis/temp/images/1.jpg",
             title=u"Lorem <b>ipsum</b>",
             text=u"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat."),
        dict(target="news",
             image="/++theme++il.portalinterlegis/temp/images/interlegis.jpg",
             title=u"Duis <b>autem</b> vel eum",
             text=u"Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis."),
        dict(target="news",
            image="/++theme++il.portalinterlegis/temp/images/caneca.jpg",
            title=u"Nam <b>liber</b> tempor cum soluta",
            text=u"Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam."),
            ])

    # Product and Services
    fill_carousel("#products-and-services_0 a.editable-box-link", [
        dict(target="news",
             image="/++theme++il.portalinterlegis/temp/images/1.jpg",
             title=u"Portal <b>Modelo</b>",
             text=u"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat."),
        dict(target="news",
             image="/++theme++il.portalinterlegis/temp/images/interlegis.jpg",
             title=u"Domínio <b>leg.br</b>",
             text=u"Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis."),
        dict(target="news",
            image="/++theme++il.portalinterlegis/temp/images/caneca.jpg",
            title=u"SAPL",
            text=u"Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam."),
            ])

################################################################
# run this preferably interactively (line by line in a prompt)
################################################################
driver = webdriver.Firefox()
driver.implicitly_wait(1)
base_url = "http://portalh.interlegis.leg.br"
driver.get(base_url + "/")
login(base_url, driver)

populate_carousels()
