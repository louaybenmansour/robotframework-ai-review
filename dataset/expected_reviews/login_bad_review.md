# Expected Review - login_bad.robot


## Issues


### 1. Use of Sleep

Severity: High

Explanation:
Fixed waits make tests slow and unstable.

Suggested improvement:
Replace Sleep with explicit waits.


### 2. Hardcoded credentials

Severity: High

Explanation:
Sensitive data is stored directly in the test.

Suggested improvement:
Use variables or secret management.


### 3. Missing validation

Severity: High

Explanation:
The test does not verify successful login.

Suggested improvement:
Add assertions after login.


### 4. No reusable keywords

Severity: Medium

Explanation:
The login flow cannot be reused.

Suggested improvement:
Create Login keyword in a resource file.