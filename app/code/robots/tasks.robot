*** Settings ***
Documentation     program to receive the json input
...               and echo the message in console
Library           RPA
Library           Collections
Library           XML
Library           OperatingSystem
Library           String

*** Variables ***
${dict_args}      test

*** Tasks ***
Process Input Message
    Echo Input Message    ${dict_args}

*** Keywords ***
Echo Input Message
    [Arguments]    ${dict_args}
    ${input_data}=    evaluate    json.loads('''${dict_args}''')    json
    Log To Console    ${input_data}
    FOR    ${key}    ${value}    IN    &{input_data}
        Log To Console    key = ${key}, value = ${value}
    END
