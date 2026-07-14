*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${URL}          https://example.com
${BROWSER}      chrome


*** Test Cases ***
User Login Test

    Open Browser    ${URL}    ${BROWSER}
    Input Text      id=username    admin
    Input Text      id=password    ${PASSWORD}
    Click Button    id=login
    Page Should Contain    Dashboard
    Close Browser