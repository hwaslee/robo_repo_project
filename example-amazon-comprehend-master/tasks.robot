*** Comments ***
# IMDB에서 다른 방법으로 RoboCop 검색
# AWS id는 없으니, excel로 저장
# excel file을 email로 전송


*** Settings ***
Documentation       IMDB review sentiment robot.

Library             Browser
...                 jsextension=${CURDIR}${/}keywords.js
...                 strict=False
Library             Collections
Library             RPA.Cloud.AWS    robocloud_vault_name=aws
Library             RPA.Tables
Library             RPA.Browser.Selenium


*** Variables ***
${AWS_REGION}=              us-east-2
${MOVIE}=                   RoboCop
${REVIEW_MAX_LENGTH}=       ${2000}
${SENTIMENTS_FILE_PATH}=    ${OUTPUT_DIR}${/}imdb-sentiments-${MOVIE}.csv


*** Tasks ***
Analyze IMDB movie review sentiments
    Open IMDB
    Search for movie    ${MOVIE}
    @{reviews}=    Get reviews
    @{sentiments}=    Analyze sentiments    ${reviews}
    ${table}=    Create Table    ${sentiments}
    Write Table To Csv    ${table}    ${SENTIMENTS_FILE_PATH}


*** Keywords ***
Open IMDB
    Log To Console    ""
    Log To Console    Hwa *** Open IMDB started
    New Page    https://www.imdb.com/    # playwright

Search for movie
    [Arguments]    ${movie}
    Log To Console    Hwa *** Search for movie started
    Type Text    css=#suggestion-search    ${movie}    # Playwright
    # Click    css=.react-autosuggest__suggestion--first a    # Playwright, (working)
    Click    css=#suggestion-search-button    # Playwright, (O, error later)
    # Click Button    css=#suggestion-search-button    # Selenium, (X-No browser open)
    # Click Element    /html/body/div[2]/nav/div[2]/div[1]/form/button    # Selenium, (X-No browser open)

Scroll page
    Log To Console    Hwa *** Scroll page started
    FOR    ${i}    IN RANGE    5
        Scroll By    vertical=100%
        Sleep    100 ms
    END

Get reviews
    Log To Console    Hwa *** Get reviews started
    Click    text=USER REVIEWS
    ${review_locator}=    Set Variable    css=.review-container .text
    Log To Console    Hwa review_locator --- ${review_locator}
    Wait For Elements State    ${review_locator}
    Scroll page
    @{reviews}=    getTexts    ${review_locator}
    Log To Console    Hwa reviews --- ${reviews}
    RETURN    ${reviews}

Analyze sentiments
    [Arguments]    ${reviews}
    Log To Console    Hwa *** Analyze sentiments started
    Init Comprehend Client    use_robocloud_vault=True    region=${AWS_REGION}
    @{sentiments}=    Create List
    FOR    ${review}    IN    @{reviews}
        ${sentiment_score}=
        ...    Comprehend sentiment
        ...    ${review}[:${REVIEW_MAX_LENGTH}]
        &{sentiment}=    Create Dictionary
        ...    review=${review}
        ...    sentiment=${sentiment_score}
        Append To List    ${sentiments}    ${sentiment}
    END
    RETURN    ${sentiments}

Comprehend sentiment
    [Arguments]    ${text}
    Log To Console    Hwa *** Comprehend sentiment started
    ${sentiment}=    Detect Sentiment    ${text}
    ${sentiment_score}=    Set Variable If
    ...    "${sentiment["Sentiment"]}" == "NEGATIVE"
    ...    ${-1}
    ...    ${1}
    RETURN    ${sentiment_score}
