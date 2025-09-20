from selene import browser, be, have
import os
from utils import attach
image_path = os.path.abspath("resources/test_check.txt")
import allure
from selene.support.shared import browser

def test_fill_form(setup_browser):
    browser = setup_browser
    browser.open('https://demoqa.com/automation-practice-form')

    attach.add_screenshot(browser)
    with allure.step("Fill name"):
        browser.element('[id="firstName"]').should(be.visible).type("Alisha")
    with allure.step("Fill surname"):
        browser.element('[id="lastName"]').should(be.visible).type("Meier")
    with allure.step("Fill email"):
        browser.element('[id="userEmail"]').should(be.visible).type("alisha.meyerr@gmail.com")
    with allure.step("Choose gender"):
        browser.element('label[for="gender-radio-2"]').click()
    with allure.step("Fill phone"):
        browser.element('[id="userNumber"]').should(be.visible).type("7078083369")
    with allure.step("Choose BD"):
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type('November')
        browser.element('.react-datepicker__year-select').type('1995')
        browser.element('.react-datepicker__day--003').click()
    with allure.step("Choose subject"):
        browser.element('#subjectsInput').should(be.visible).type('Computer Science').press_enter()
    with allure.step("Choose hobbies"):
        browser.element('label[for ="hobbies-checkbox-3"]').click()
    with allure.step("Upload image"):
        browser.element('[id = "uploadPicture"]').should(be.visible).send_keys(image_path)
    with allure.step("Fill address"):
        browser.element('[id="currentAddress"]').should(be.visible).type("Almaty")
    with allure.step("Choose state"):
        browser.element('#state input').type('NCR').press_enter()
    with allure.step("Choose city"):
        browser.element('[id="city"]').should(be.visible).click()
        browser.element('[id="react-select-4-input"]').type('Delhi').press_enter()
    with allure.step("Send form"):
        browser.element('#submit').click()
    with allure.step("Check sending form"):
        browser.element('[id="example-modal-sizes-title-lg"]').should(be.visible).should(have.text('Thanks for submitting the form'))

def test_successfully_filling(setup_browser):
    with allure.step("Check form"):
        test_fill_form(setup_browser)
        attach.add_screenshot(browser)
        table_element = browser.all('table.table-dark tbody tr')
        table_element.element_by(have.text('Student Name')).all('td').second.should(have.text('Alisha Meier'))
        table_element.element_by(have.text('Student Email')).all('td').second.should(have.text('alisha.meyerr@gmail.com'))
        table_element.element_by(have.text('Gender')).all('td').second.should(have.text('Female'))
        table_element.element_by(have.text('Mobile')).all('td').second.should(have.text('7078083369'))
        table_element.element_by(have.text('Date of Birth')).all('td').second.should(have.text('03 November,1995'))
        table_element.element_by(have.text('Subjects')).all('td').second.should(have.text('Computer Science'))
        table_element.element_by(have.text('Hobbies')).all('td').second.should(have.text('Music'))
        table_element.element_by(have.text('Picture')).all('td').second.should(have.text('test_check.txt'))
        table_element.element_by(have.text('Address')).all('td').second.should(have.text('Almaty'))
        table_element.element_by(have.text('State and City')).all('td').second.should(have.text('NCR Delhi'))