*** Settings ***
Library     RPA.Tables
Library     RPA.Excel.Files


*** Variables ***
${ORDERS_FILE}          ./output/excel.xlsx
${EXCEL_DICT_FILE}      ./output/excel_dict.xlsx
${EXCEL_LIST_FILE}      ./output/excel_list.xlsx
${EXCEL_FILE}           ./output/excel.xlsx
@{heading}              Row No    Amount
@{rows}                 ${heading}


*** Tasks ***
Create excel Files
    [Setup]    Open Workbook    ${EXCEL_FILE}
    Log To Console    \n****T1 Create excel Files TASK started
    Creating new Excel dict
    ${orders_ret}=    Read orders as table
    FOR    ${order}    IN    ${orders_ret}
        Log To Console    T2. ${order}\n
    END
    Rows in the sheet


*** Keywords ***
Creating new Excel dict
    Log To Console    \n----1. Creating new Excel dict started
    Create Workbook    ${EXCEL_DICT_FILE}
    FOR    ${index}    IN RANGE    20
        &{row}=    Create Dictionary
        ...    Row No    ${index}
        ...    Amount    ${index * 25}
        Append Rows to Worksheet    ${row}    header=${TRUE}
    END
    Save Workbook

# Creating new Excel list
#    Log To Console    \n----2. Creating new Excel list started
#    Create Workbook    ${EXCEL_LIST_FILE}
#    FOR    ${index}    IN RANGE    1    20
#    @{row}=    Create List    ${index}    ${index * 25}
#    Append To List    ${rows}    ${row}
#    END
#    Append Rows to Worksheet    ${rows}
#    Save Workbook

Read orders as table
    Log To Console    \n----3. Read orders as table started
    # Open workbook    ${ORDERS_FILE}
    Open workbook    ${EXCEL_DICT_FILE}
    ${worksheet}=    Read worksheet    header=${TRUE}
    Log To Console    3.1 ${worksheet}
    ${orders}=    Create table    ${worksheet}
    Log To Console    3.2 ${orders}
    RETURN    ${orders}
    [Teardown]    Close workbook

Rows in the sheet
    Log To Console    \n----4. Rows in the sheet started
    Open workbook    ${EXCEL_DICT_FILE}
    @{sheets}=    List Worksheets
    FOR    ${sheet}    IN    @{sheets}
        ${count}=    Get row count in the sheet    ${sheet}
        Log To Console    Worksheet '${sheet}' has ${count} rows
        Log    Worksheet '${sheet}' has ${count} rows
    END

Get row count in the sheet
    [Arguments]    ${SHEET_NAME}
    Log To Console    \n----5. Get row count in the sheet started
    ${sheet}=    Read Worksheet    ${SHEET_NAME}
    ${rows}=    Get Length    ${sheet}
    RETURN    ${rows}
