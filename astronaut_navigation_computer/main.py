from keypad import get_user_input
from led_bar import set_all, show
from code_logic import handle_user_input

set_all(0, 0, 255, 0.04)
show()

valid_strings_list = [
    "*1794#",
    "*1403#",
    "*4845#",
    "*5860#",
    "*0076#",
    "*9765#",
    "*6900#",
    "*4258#",
    "*5902#",
    "*1262#",
    "*2719#",
    "*8508#",
    "*2422#",
    "*3735#",
    "*2538#",
    "*6083#",
    "*7297#",
    "*3919#",
    "*1372#",
    "*6993#",
    "*6790#",
    "*4609#",
    "*2730#",
    "*0365#",
    "*9316#",
    "*9357#",
    "*9038#",
    "*3507#",
    "*5766#",
    "*6027#",
    "*1747#",
    "*8310#",
    "*2987#",
    "*0690#",
    "*3024#",
    "*9629#",
    "*7070#",
    "*4640#",
    "*5524#",
    "*4582#",
    "*0623#",
    "*8879#",
    "*8515#",
    "*5953#",
    "*7622#",
    "*2169#",
    "*9657#",
    "*1646#",
    "*9958#",
    "*8527#"
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
