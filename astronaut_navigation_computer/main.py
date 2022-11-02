from keypad import get_user_input
from led_bar import set_all, show
from code_logic import handle_user_input

set_all(0, 0, 255, 0.04)
show()

valid_strings_list = ['*' + x + '#' for x in 
    [
        "8276",
        "2149",
        "8349"
    ]
]

inputstring = ""
valid_result = False


while True:
    user_input = get_user_input()
    print(user_input)
    inputstring += user_input
    print(inputstring)
    inputstring, valid_result = handle_user_input(inputstring, valid_strings_list)
    if valid_result:
        valid_strings_list.remove(inputstring)
        inputstring = ""
        valid_result = False
    if len(inputstring) == 0:
        set_all(0, 0, 255)
        show()
