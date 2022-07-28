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
&{local_dict}


*** Tasks ***
Work On Dictionary
    &{local_dict}=    Create Dictionary
    ${length}=    Get Length    ${local_dict}
    Log To Console    \n----1.    ${length},    &{local_dict}
    Log To Console    ----2.    ${length},    ${local_dict}

    ${k_val}=    Set Variable    1024
    ${v_val}=    Set Variable    {2,4,8,6,10}

    # ${local_dict}=    Add To Dict    ${k_val}    ${v_val}    &{local_dict}
    # ${local_dict}=    Add To Dict    'ABC'    '{1,2,3}'    &{local_dict}    # failed....
    # Log To Console    ----5. ${local_dict}

    Set To Dictionary    ${local_dict}    ${k_val}    ${v_val}
    Log To Console    ----3. ${local_dict}

    ${k_val}=    Set Variable    1023
    ${v_val}=    Set Variable    {1,5,3,7,9}
    Set To Dictionary    ${local_dict}    ${k_val}    ${v_val}
    Log To Console    ----4. ${local_dict}

    ${ord}=    Set Variable    ASC
    ${sorted_list}=    Sort Dict To List    ${local_dict}    ${ord}
    Log To Console    ----8-1. ${sorted_list}
    Log To Console    ----8-2. ${ord}

    ${new_list}=    Sort Dict By Key    ${local_dict}    ${ord}
    Log To Console    ----9-1. ${new_list}
    Log To Console    ----9-2. ${ord}

    Search Value From Dict    ${local_dict}


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
    [Arguments]    ${dict}
    ${the type}=    Evaluate    type(${dict})
    Log To Console    ----10. The argument is of type ${the type}

    @{nums}=    Create List    1023    1000    1024
    FOR    ${val}    IN    @{nums}
        TRY
            ${value}=    Get From Dictionary    ${dict}    ${val}
            Log To Console    ----11. ${value} found
        EXCEPT
            Log To Console    ----11. No number ${val}
        END
    END
