*** Settings ***
Documentation       Google Translate song lyrics from source to target language.
...                 Save the original and the translated lyrics as text files

Library             RPA.Browser
Library             OperatingSystem
Library             RPA.Windows
Library             RPA.Hubspot
Library             RPA.Browser.Selenium


*** Variables ***
${SONG_NAME}            %{SONG_NAME=Peaches}
${SOURCE_LANG}          %{SOUERCE_LANG=en}
${TAR_LANG}             %{TAR_LANG=ko}
${button_class_name}    btn skip


*** Tasks ***
Google Translate song lyrics from source to target language
    ${lyrics}=    Get Lyrics
    ${translation}=    Translate    ${lyrics}
    Save Lyrics    ${lyrics}    ${translation}


*** Keywords ***
Get Lyrics
    Open Available Browser    url=https://www.lyrics.com/lyrics    browser_selection=Chrome
    Press Keys    //*[@id="search"]    ${SONG_NAME}
    Click Button    //*[@id="page-word-search-button"]
    Click Element When Visible    css:.best-matches a
    Log To Console    \n---- 1
    ${x}=    Set Variable    ${0}
    WHILE    ${x} < 3
        TRY
            Click Element When Visible    id:dismiss-button
        EXCEPT
            Log To Console    --- Exception occurred..${x}
        END
        ${x}=    Evaluate    ${x} + 1
    END
    Log To Console    ---- 3
    ${lyrics_element}=    Set Variable    css:#lyric-body-text
    Wait Until Element Is Visible    ${lyrics_element}
    Log To Console    ---- 4
    ${lyrics}=    RPA.Browser.Get Text    ${lyrics_element}
    RETURN    ${lyrics}

Translate
    [Arguments]    ${lyrics}
    Go To    https://translate.google.co.kr/?hl=ko&tab=rT&sl=${SOURCE_LANG}&tl=${TAR_LANG}&text=${lyrics}&op=translate
    ${translation_element}=    Set Variable    css:.Q4iAWc
    Wait Until Element Is Visible    ${translation_element}
    ${translation}=    RPA.Browser.Get Text    ${translation_element}
    RETURN    ${translation}

Save Lyrics
    [Arguments]    ${lyrics}    ${translation}
    Create File    ${OUTPUT_DIR}${/}${SONG_NAME}-${SOURCE_LANG}-original.txt    content=${lyrics}
    Create File    ${OUTPUT_DIR}${/}${SONG_NAME}-${TAR_LANG}-translation.txt    content=${translation}
