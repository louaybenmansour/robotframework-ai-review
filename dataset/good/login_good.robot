*** Settings ***
Library    SeleniumLibrary
Resource    resources/login.resource


*** Test Cases ***
User Can Login With Valid Credentials

    [Documentation]    Verify that a valid user can login successfully

    Open Login Page
    Login With Valid Credentials
    Dashboard Should Be Visible