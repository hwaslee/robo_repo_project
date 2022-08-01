*** Comments ***
# Collections 관련 python 보조 기능


*** Settings ***
Documentation       Template robot main suite.

Library             collection_handler.py
Library             Collections
Library             OperatingSystem
Library             BuiltIn
Library             RPA.JSON
Library             RPA.FileSystem


*** Variables ***
${k_val}            ${EMPTY}
${v_val}            ${EMPTY}
${sorted_list}      ${EMPTY}
&{GLOBAL_DICT}


*** Tasks ***
Work On Dictionary
    ${GLOBAL_DICT}=    Create Dictionary    1000=[1,2,3,4,5,6]    1002=[2,4,6,8,10]
    Log To Console    \n----1-1. created..
    Log To Console    ----1-2 ${GLOBAL_DICT}[1000]
    Log To Console    ----1-3. &{GLOBAL_DICT}
    Log To Console    ----1-4. ${GLOBAL_DICT}
    ${length}=    Get Length    ${GLOBAL_DICT}
    Log To Console    ----1-5. ${length}

    ${k_val}=    Set Variable    1024
    ${v_val}=    Set Variable    [2,4,8,6,10]

    Set To Dictionary    ${GLOBAL_DICT}    ${k_val}    ${v_val}
    Log To Console    ----3-1. ${GLOBAL_DICT}
    Log To Console    ----3-2. ${GLOBAL_DICT}[1024]

    # ${GLOBAL_DICT}=    Add To Dict    ${k_val}    ${v_val}    &{GLOBAL_DICT}    # failed: expected 4 arguments, got 2.
    # Log To Console    ----5-1. &{GLOBAL_DICT}
    # ${GLOBAL_DICT}=    Add To Dict    ABC    {1,2,3}    &{GLOBAL_DICT}    # failed: expected 4 arguments, got 2.
    # Log To Console    ----5-2. &{GLOBAL_DICT}
    # ${GLOBAL_DICT}=    Add To Dict    'ABC'    '{1,2,3}'    &{GLOBAL_DICT}    # failed: expected 4 arguments, got 2.
    # Log To Console    ----5-3. &{GLOBAL_DICT}

    ${k_val}=    Set Variable    1023
    ${v_val}=    Set Variable    {1,5,3,7,9}
    Set To Dictionary    ${GLOBAL_DICT}    ${k_val}    ${v_val}
    Log To Console    ----4. ${GLOBAL_DICT}

    ${ord}=    Set Variable    ASC
    ${sorted_list}=    Sort Dict To List    ${GLOBAL_DICT}    ${ord}
    Log To Console    ----8-1. ${sorted_list}
    Log To Console    ----8-2. ${ord}

    ${new_list}=    Sort Dict By Key    ${GLOBAL_DICT}    ${ord}
    Log To Console    ----9-1. ${new_list}
    Log To Console    ----9-2. ${ord}

    Log To Console    ----9-3. &{GLOBAL_DICT}
    Log To Console    ----9-4. ${GLOBAL_DICT}

    # Log To Console    ----9-5. &{GLOBAL_DICT.'1024'}    # SyntaxError: invalid syntax (<string>, line 1)
    # Log To Console    ----9-5. &{GLOBAL_DICT.1024}    # SyntaxError: invalid syntax (<string>, line 1)
    # Log To Console
    # ...    ----9-6. ${GLOBAL_DICT.'1024'}    # failed: SyntaxError: unexpected EOF while parsing (<string>, line 1)/
    # Log To Console
    # ...    ----9-6. ${GLOBAL_DICT.1024}    # failed: SyntaxError: unexpected EOF while parsing (<string>, line 1)/

    Search Value From Dict    &{GLOBAL_DICT}


*** Keywords ***
Sort Dict To List
    [Arguments]    ${dict}    ${ord}
    Log To Console    ----5.    ${ord}
    ${the type}=    Evaluate    type(${dict})
    Log To Console    ----6. The argument is of type ${the type}
    # Log To Console    ----6.    &{dict_variable}
    ${sorted_list}=    Sort Dict By Key    ${dict}    ${ord}
    Log To Console    ----7. ${sorted_list}
    RETURN    ${sorted_list}

Search Value From Dict
    [Arguments]    &{dict}
    Log To Console    ----11-1. &{GLOBAL_DICT}
    Log To Console    ----11-1. ${GLOBAL_DICT}
    Log To Console    ----11-1. ${dict}
    ${the type}=    Evaluate    type(${dict})
    Log To Console    ----11-2. The argument is of type ${the type}

    @{nums}=    Create List    1023    1000    1025
    FOR    ${val}    IN    @{nums}
        TRY
            ${value}=    Get From Dictionary    ${dict}    ${val}
            Log To Console    ----11-3. ${value} found
        EXCEPT
            Log To Console    ----11-4. ${val} not in keys
        END
    END
    Log To Console    ----11.5 ${nums}
    ${the type}=    Evaluate    type(${nums})
    Log To Console    ----11-6. The type of 1st argument: ${the type}
    ${size}=    Get Length    ${nums}
    Log To Console    ----11-7. Size: ${size}
    Log To Console    ----11.8 @{nums}
    ${the type}=    Evaluate    type(@{nums})
    Log To Console    ----11-9. The type of 1st argument: ${the type}
    # ${size}=    Get Length    @{nums}
    # Log To Console    ----11-10. Size: ${size}

    ${as_list}=    Create List    1    2
    &{as_dict}=    Create Dictionary    first_arg=1    second_arg=2

    Example Calls    1    2
    Example Calls    @{as_list}
    Example Calls    ${as_list}    dummy
    Example Calls    &{as_dict}
    Example Calls    ${as_dict}    dummy

    ${key_list}=    Create List    first_arg    second_arg
    FOR    ${val}    IN    @{key_list}
        TRY
            ${value}=    Get From Dictionary    ${as_dict}    ${val}
            Log To Console    ----13-1. ${value} found
        EXCEPT
            Log To Console    ----13-2. ${val} not in keys
        END
    END

Example Calls
    [Arguments]    ${first_arg}    ${second_arg}
    Log To Console    ----12.1 Got arguments ${first_arg} and ${second_arg}
    ${the type}=    Evaluate    type(${first_arg})
    Log To Console    ----12-2. The type of 1st argument: ${the type}
    ${size}=    Get Length    ${first_arg}
    Log To Console    ----12.3 Size: ${size}
