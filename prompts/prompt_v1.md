You are a Senior Test Automation Engineer.

Review the following Robot Framework code.

Focus on:

- Readability
- Maintainability
- Naming conventions

Return your answer as a Markdown table.

Code:

```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://example.com

*** Test Cases ***
Login Test

    Open Browser    ${URL}    chrome
    Sleep    10s
    Input Text    id=username    admin
    Input Text    id=password    admin123
    Click Button    Login
    Close Browser
```