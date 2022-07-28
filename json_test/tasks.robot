*** Settings ***
Library     RPA.JSON
Library     Collections
Library     BuiltIn


*** Tasks ***
JSON Handling
    JSON operations


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
