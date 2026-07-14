*** Keywords ***

Open Login Page

    Open Browser    ${URL}    ${BROWSER}
    Wait Until Page Contains Element    id=username


Login With Valid Credentials

    Input Text    id=username    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button  id=login


Dashboard Should Be Visible

    Wait Until Page Contains    Dashboard
    Close Browser