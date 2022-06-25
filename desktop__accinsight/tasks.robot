*** Comments ***
# Accessibility Insight 이용하여 APPLICATION 관련 정보를 획득하고
# 이를 이용하여 automation


*** Settings ***
Library     RPA.Windows
Library     RPA.Desktop.Windows

*** Tasks ***
Automate MiPlatform
    Start The Miplatform
    Login MiPlatform
    Click grid    # Using The AutomationId Property Value

*** Keywords ***
Start The Miplatform
    Log    "start"
    Open Executable    # from Desktop.Windows
    ...    C:\\Users\\LnY\\AppData\\Local\\TOBESOFT\\MiPlatform320U\\MiPlatform320U.exe
    ...    CodeSamples - [sample01]

Login MiPlatform

Click grid    # Using The AutomationId Property Value
    Log    "click"
    ${rows}=    Get Elements    class:AfxWnd80u
    # ${rows} is a list of `WindowsElement`s
    # Log    ${rows}    # ${rows.length}, ${rows.size} not working
    FOR    ${row}    IN    @{rows}
        Log To Console    ""
        Log To Console    "row.item:" ${row.item}
        Log To Console    "row.locator:" ${row.locator}
        Log To Console    "row.name:" ${row.name}    # access `WindowsElement`
        Log To Console    "row.automation_id:" ${row.automation_id}
        Log To Console    "row.control_type:" ${row.control_type}
        Log To Console    "row.class_name:" ${row.class_name}
        Log To Console    "row.item.AutomationId: ${row.item.AutomationId}    # access `WindowsElement.item` directly
        Log To Console    "row.item.Name:" ${row.item.Name}    # same as `${row.name}`
    END
    Log    Successfully done !!!
