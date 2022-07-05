*** Comments ***
Documentation    An example robot that reads and writes data
...    into a Google Sheet document.

Library    RPA.Cloud.Google


*** Settings ***
Library     RPA.Cloud.Google


*** Tasks ***
Init Google services
    Init Vision    C:\\Python\\robo_repo\\z.doc\\GoogleCloudVision\\visionpilot-eadd89fa0d23.json

Minimal task
    Log    Done.
