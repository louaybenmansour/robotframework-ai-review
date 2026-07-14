You are a Senior Test Automation Engineer.

Review this Robot Framework code.

Focus on:

- Readability
- Maintainability
- Naming conventions
- Keyword design
- Duplicate code
- Test design
- Robot Framework best practices

For each issue provide:

- Issue
- Severity
- Explanation
- Suggested improvement

Return the answer as a Markdown table.

Code:

```robotframework
*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${URL}    https://example.com


*** Test Cases ***
Login

    Open Browser    ${URL}    chrome
    Sleep    10s
    Input Text    id=username    admin
    Input Text    id=password    admin123
    Click Button    Login
    Close Browser
```