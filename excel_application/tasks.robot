*** Settings ***
Library             RPA.Excel.Application

Task Setup          Open Application
Task Teardown       Quit Application


*** Tasks ***
Manipulate Excel application
    log To Console    ""
    Log To Console    \n---- Manipulate Excel application started
    Open Workbook    ${CURDIR}${/}output${/}workbook.xlsx
    Set Active Worksheet    sheetname=new stuff
    FOR    ${index}    IN RANGE    1    10
        Write To Cells    row=${index}
        ...    column=1
        ...    value=${index}
    END
    Save Excel

Run Excel Macro
    Log To Console    \n---- Run Excel Macro started
    Open Workbook    ${CURDIR}${/}output${/}orders_with_macro.xlsm
    Run Macro    Sheet1.CommandButton1_Click

Export Workbook as PDF
    Log To Console    \n---- Export Workbook as PDF started
    Open Workbook    ${CURDIR}${/}output${/}workbook.xlsx
    Export as PDF    ${CURDIR}${/}output${/}workbook.pdf
