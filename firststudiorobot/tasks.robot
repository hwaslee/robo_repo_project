*** Settings ***
Library     Collections
Library     BuiltIn
Library     RPA.JSON
Library     RPA.FileSystem
Library     RPA.Browser.Selenium


*** Tasks ***
main
    Log To Console    1

second task
    Log To Console    2


*** Keywords ***
Load Data
