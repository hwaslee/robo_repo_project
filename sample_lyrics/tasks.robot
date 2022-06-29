*** Comments ***
# https://robocorp.com/docs/development-guide
# AD page appears during the execution, but it doesn't when accessing directly from the browser
# don't know why?


*** Settings ***
Documentation       Google Translate song lyrics from source to target language.
...                 Save the original and the translated lyrics as text files

Library             RPA.Browser
Library             OperatingSystem
Library             RPA.Windows
Library             RPA.Hubspot
# Task Teardown    Close All Browsers


*** Variables ***
${SONG_NAME}=               %{SONG_NAME=Peaches}
${SOURCE_LANG}=             %{SOUERCE_LANG=en}
${TAR_LANG}=                %{TAR_LANG=ko}
${button_class_name}=       btn skip


*** Tasks ***
Google Translate song lyrics from source to target language
    ${lyrics}=    Get lyrics
    ${translation}=    Translate    ${lyrics}
    Save lyrics    ${lyrics}    ${translation}


*** Keywords ***
Get lyrics
    # Open Available Browser    https://www.lyrics.com/lyrics/${SONG_NAME}    Edge
    # Open Browser    https://www.lyrics.com/lyrics/${SONG_NAME}    browser=Edge
    Open Available Browser    https://www.lyrics.com/lyrics    browser_selection=Chrome
    Press Keys    //*[@id="search"]    ${SONG_NAME}
    Click Button    //*[@id="page-word-search-button"]
    Click Element When Visible    css:.best-matches a
    Log To Console    \n---- 1

    # "AD" screen popped up --> to close AD screen
    ${x}=    Set Variable    ${0}
    WHILE    ${x} < 3
        # IF    ${x} == 2    CONTINUE    # Skip this iteration.
        # Log    x = ${x}    # x = 1, x = 3
        TRY
            # Click Button When Visible    //*[@id="dismiss-button"]
            # Click Element When Visible    //*[@id="dismiss-button"]
            # Click Element When Visible    css:#dismiss-button
            Click Element When Visible    id:dismiss-button
        EXCEPT
            Log To Console    --- Exception occurred..
        END
        ${x}=    Evaluate    ${x} + 1
        Log To Console    ---- 2
    END
    Log To Console    ---- 3

    ${lyrics_element}=    Set Variable    css:#lyric-body-text
    Wait Until Element Is Visible    ${lyrics_element}
    Log To Console    ---- 4

    ${lyrics}=    RPA.Browser.Get Text    ${lyrics_element}
    RETURN    ${lyrics}

Translate
    [Arguments]    ${lyrics}
    # No Operation
    Go To    https://translate.google.co.kr/?hl=ko&tab=rT&sl=${SOURCE_LANG}&tl=${TAR_LANG}&text=${lyrics}&op=translate
    ${translation_element}=    Set Variable    css:.Q4iAWc
    Wait Until Element Is Visible    ${translation_element}
    ${translation}=    RPA.Browser.Get Text    ${translation_element}
    RETURN    ${translation}

Save lyrics
    [Arguments]    ${lyrics}    ${translation}
    # No Operation
    Create File    ${OUTPUT_DIR}${/}${SONG_NAME}-${SOURCE_LANG}-original.txt    ${lyrics}
    Create File    ${OUTPUT_DIR}${/}${SONG_NAME}-${TAR_LANG}-translation.txt    ${translation}
