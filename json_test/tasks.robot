*** Settings ***
Library     RPA.JSON
Library     Collections
Library     BuiltIn
Library     RPA.FileSystem


*** Variables ***
${filename}         ${OUTPUT_DIR}${/}dict_data.json
&{all_picks}
&{loaded_picks}


*** Tasks ***
JSON Handling
    JSON operations
    Save To JsonFile
    ${contents}=    Load Data From JsonFile
    Search Pick By Key    ${contents}
    Search Value From Dict    ${contents}


*** Keywords ***
# Scenario: Add Objects
#    ${current_record}    Load JSON From File    C:\\Python\\robo_repo\\json_test\\output\\example.json
#    Delete Object From Json    ${current_record}    $..address

#    ${coords}    Create Dictionary    latitude=13.1234    longitude=130.1234

#    # Check if the "address" key is in the object
#    ${is_address_key}    Run Keyword And Return Status
#    ...    Dictionary Should Contain Key
#    ...    ${current_record}
#    ...    address

#    # If address key not exists then add coords to dictionary with key address and add to object directly
#    IF    ${is_address_key}
#    Add Object To Json    ${current_record}    $..address    ${coords}
#    ELSE
#    ${address}    Create Dictionary    address=${coords}
#    Add Object To Json    ${current_record}    $    ${address}
#    END

#    Dictionary Should Contain Key    ${current_record}[address]    latitude
#    Log To Console    \n${current_record}

Save To JsonFile
    @{picks}=    Create List    1000    1001    10002    10003    1004
    FOR    ${pick}    IN    @{picks}
        TRY
            Set To Dictionary    ${all_picks}    ${pick}    {1,2,3,4,5,6}
            Log To Console    ----A. ${all_picks}
        EXCEPT
            Log To Console    ----A-1. exception ....
        END
    END
    Save JSON to file    ${all_picks}    ${filename}

Load Data From JsonFile
    ${file_content}=    Read File    ${filename}
    Log To Console    ----B. ${file_content}
    # RETURN    ${file_content}    # Expected arg1 to be dict-like, got string instead.

    # &{loaded_picks}=    Convert To Dictionary    ${file_content}    # dictionary update sequence element #0 has length 1; 2 is required
    &{loaded_picks}=    Evaluate    ${file_content}
    Log To Console    ----C-1. ${loaded_picks}

    ${the type}=    Evaluate    type(${loaded_picks})
    Log To Console    ----C-2. The argument is of type ${the type}

    RETURN    ${loaded_picks}
    # RETURN    &{loaded_picks}

Search Pick By Key
    [Arguments]    ${contents}
    ${the type}=    Evaluate    type(${contents})
    Log To Console    ----D. The argument is of type ${the type}

    # ${value}=    Get From Dictionary    ${loaded_picks}    1001    # Dictionary does not contain key '1001'.
    ${value}=    Get From Dictionary    ${contents}    1001    # OK
    Log To Console    ----E. ${value}

Search Value From Dict
    [Arguments]    ${dict}
    ${the type}=    Evaluate    type(${dict})
    Log To Console    ----H. The argument is of type ${the type}

    @{nums}=    Create List    1001    1002    1004
    FOR    ${val}    IN    @{nums}
        TRY
            ${value}=    Get From Dictionary    ${dict}    ${val}
            Log To Console    ----I. ${value} found
        EXCEPT
            Log To Console    ----J. No number ${val}
        END
    END

Save string to file
    ${value}=    Set Variable
    ...    [{'1024': ['1', '3', '5', '7', '9', '11']}, {'1023': ['11', '13', '15', '17', '19', '21']}]
    ${key}=    Set Variable    "picks"

    ${mark}=    Set variable    {"name": "Mark", "mail": "mark@example.com"}
    Save JSON to file    ${mark}    mark.json

JSON operations
    ${key}=    Set Variable    Picks
    ${val_list}=    Set Variable
    ...    [{'1024': ['1', '3', '5', '7', '9', '11']}, {'1023': ['11', '13', '15', '17', '19', '21']}]
    &{dict}=    Create Dictionary    ${key}=${val_list}
    Log To Console    \n----0. dict:&{dict}, key:${key}, value:${val_list}

    Save JSON to file    ${dict}    picks1.json
    Log To Console    ----0-1. Saved to file

    # ${dict_str}=    Convert To String    ${dict}
    # Log To Console    ----0-2. ${dict_str}

    # Save JSON to file    ${dict_str}    picks2.json
    # Log To Console    ----0-3. Saved to file

    ${json}=    Convert String to JSON    {"orders": [{"id": 1},{"id": 2}]}
    Log To Console    ----1. ${json}
    # ${json} = {'orders': [{'id': 1}, {'id': 2}]}

    ${first_order_id}=    Get value from JSON    ${json}    $.orders[0].id
    Log To Console    ----2. ${first_order_id}
    # ${first_order_id} = 1

    ${all_ids}=    Get values from JSON    ${json}    $..id
    Log To Console    ----3. ${all_ids}
    # ${all_ids} = [1, 2]

    ${json1}=    Add to JSON    ${json}    $.orders    {"id": 3}
    Log To Console    ----4. ${json1}
    # ${json} = {'orders': [{'id': 1}, {'id': 2}, '{"id": 3}']}

    ${json2}=    Delete from JSON    ${json}    $.orders[-1:]
    Log To Console    ----5. ${json2}
    # ${json} = {'orders': [{'id': 1}, {'id': 2}]}

    ${json3}=    Update value to JSON    ${json}    $.orders[1].id    4
    Log To Console    ----6. ${json3}
    # ${json} = {'orders': [{'id': 1}, {'id': '4'}]}

    ${json_as_string}=    Convert JSON to String    ${json}
    Log To Console    ----7. ${json_as_string}
    # ${json_as_string} = {"orders": [{"id": 1}, {"id": "4"}]}

    Save JSON to file    ${json_as_string}    orders.json
    ${json4}=    Load JSON from file    orders.json
    Log To Console    ----9. ${json4}
    # ${json} = {'orders': [{'id': 1}, {'id': '4'}]}
