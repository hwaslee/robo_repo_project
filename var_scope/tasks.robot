*** Settings ***
Documentation       Template robot main suite.

Library             Collections


*** Variables ***
&{DICK_DATA}


*** Tasks ***
entry point
    Initialize Dictionary
    Get Dictionary From Othe Keyword
    Work After Creating

    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----60. has ${len} records


*** Keywords ***
Initialize Dictionary
    Log To Console    ..
    # ${DICK_DATA}=    Create Dictionary    "1001"="[1,3,4,5]"    "1002"="[2,4,6,8,0]"
    Set To Dictionary    ${DICK_DATA}    1001    [1,3,4,5]
    Set To Dictionary    ${DICK_DATA}    1002    [2,4,6,8,0]
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----10. initialized ... ${len}

Get Dictionary From Othe Keyword
    ${DICK_DATA}=    My Own Keyword returning
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----20. ${len} From returning
    log To Console    ----21. ${DICK_DATA}

    My Own Keyword no return
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----22. ${len} from without returning
    ${len}=    Get Length    ${DICK_DATA}
    log To Console    ----23. ${DICK_DATA}

My Own Keyword returning
    # ${DICK_DATA}=    Create Dictionary    "1001"="[1,1,1,1,1]"    "1003"="[2,2,2,2,2]"    "1005"="[2,2,2,2,2]"
    Set To Dictionary    ${DICK_DATA}    1001    [1,1,1,1,1]
    Set To Dictionary    ${DICK_DATA}    1003    [3,3,3,3,3]
    Set To Dictionary    ${DICK_DATA}    1005    [5,5,5,5,5]
    Set To Dictionary    ${DICK_DATA}    1007    [7,7,7,7,7]
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----30. will return ${len} records
    RETURN    ${DICK_DATA}

My Own Keyword no return
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----40. Initially, ${len} records
    Set To Dictionary    ${DICK_DATA}    1010    [10,10,10]
    Set To Dictionary    ${DICK_DATA}    1020    [20,20,20]
    Log To Console    ----41. ${DICK_DATA}
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----42. has ${len} records

Work After Creating
    ${DICK_DATA}=    Create Dictionary    "2001"="[10,10,10,10]"    "2003"="[30,30,30,30]"    "2005"="[50,50,50,50]"
    Set To Dictionary    ${DICK_DATA}    2010    [AA,AA,AA,AA]
    ${len}=    Get Length    ${DICK_DATA}
    Log To Console    ----50. has ${len} records

Minimal task
    Log    Done.
