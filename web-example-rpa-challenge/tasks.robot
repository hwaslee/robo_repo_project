*** Settings ***
Documentation       Robot to solve the first challenge at rpachallenge.com, which
...                 consists of filling a form that randomly rearranges itself,
...                 with data taken from a provided Microsoft Excel file.

Library             RPA.Browser.Selenium
Library             RPA.Excel.Files
Library             RPA.HTTP


*** Tasks ***
Start the challenge
    Open Available Browser    http://rpachallenge.com/    maximized=${TRUE}
    Download    http://rpachallenge.com/assets/downloadFiles/challenge.xlsx    overwrite=True
    Click Button    Start
    @{people}=    Get The List Of People From The Excel File
    FOR    ${person}    IN    @{people}
        Fill And Submit The Form    ${person}
    END
    Capture Element Screenshot    css:div.congratulations
    Close All Browsers


*** Keywords ***
Get The List Of People From The Excel File
    Open Workbook    challenge.xlsx
    ${table}=    Read Worksheet As Table    header=True
    Close Workbook
    RETURN    ${table}

Set Value By Xpath
    [Arguments]    ${xpath}    ${value}
    ${result}=    Execute Javascript
    ...    document.evaluate('${xpath}',document.body,null,9,null).singleNodeValue.value='${value}';
    RETURN    ${result}

Fill And Submit The Form
    [Arguments]    ${person}
    Set Value By Xpath    //input[@ng-reflect-name="labelFirstName"]    ${person}[First Name]
    Set Value By Xpath    //input[@ng-reflect-name="labelLastName"]    ${person}[Last Name]
    Set Value By Xpath    //input[@ng-reflect-name="labelCompanyName"]    ${person}[Company Name]
    Set Value By Xpath    //input[@ng-reflect-name="labelRole"]    ${person}[Role in Company]
    Set Value By Xpath    //input[@ng-reflect-name="labelAddress"]    ${person}[Address]
    Set Value By Xpath    //input[@ng-reflect-name="labelEmail"]    ${person}[Email]
    Set Value By Xpath    //input[@ng-reflect-name="labelPhone"]    ${person}[Phone Number]
    Click Button    Submit
