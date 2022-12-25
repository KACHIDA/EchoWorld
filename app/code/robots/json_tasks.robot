*** Settings ***
Library           Collections

*** Tasks ***
JSON Processing
    ${json_string}=    catenate
    ...    {
    ...    "p": "10",
    ...    "v": 100,
    ...    "vt": {
    ...    "dp": "Field to be edited"
    ...    }
    ...    }
    log to console    \nOriginal JSON:\n${json_string}
    ${json}=    evaluate    json.loads('''${json_string}''')    json
    set to dictionary    ${json["vt"]}    dp=the new value
    ${json_string}=    evaluate    json.dumps(${json})    json
    log to console    \nNew JSON string:\n${json_string}
