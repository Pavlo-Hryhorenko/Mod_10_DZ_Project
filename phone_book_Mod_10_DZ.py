from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Field:
    pass


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.value = phone


class Record:

    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for elem in self.phones:
            if elem.value == phone:
                self.phones.remove(elem)

    def delete_phone_index(self, index):
        self.phones.pop(index)

    def edit_phone(self, old_phone, new_phone):
        for elem in self.phones:
            if elem.value == old_phone:
                elem.value = new_phone




RECORDS = AddressBook()

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner


@error_handler
def add(*args):
    command_list = args[0]
    if not len(command_list) == 2:
        print("Give me name and phone please")
        return
    contact_name = command_list[0]
    contact_phone = command_list[1]
    if not RECORDS.get(contact_name):
        new_record = Record(contact_name, contact_phone)
        RECORDS.add_record(new_record)
    else:
        RECORDS[contact_name].add_phone(contact_phone)

@error_handler
def change_phone(*args):
    command_list = args[0]
    if not len(command_list) == 3:
        print("Give me name, old and new phone please")
        return

    contact_name = command_list[0]
    contact_old_phone = command_list[1]
    contact_new_phone = command_list[2]
    RECORDS[contact_name].edit_phone(contact_old_phone, contact_new_phone)

@error_handler
def delete_phone(*args):
    command_list = args[0]
    if not len(command_list) == 2:
        print("Give me name and phone please")
        return

    contact_name = command_list[0]
    contact_phone = command_list[1]
    RECORDS[contact_name].delete_phone(contact_phone)


@error_handler
def show():
    for key, data in RECORDS.items():
        print(f"Name: {key} - Phone: {', '.join(phone.value for phone in data.phones)}")

@error_handler
def phone(*args):
    command_list = args[0]
    if not len(command_list) == 1:
        print("Enter user name")
        return

    contact_name = args[0][0]
    print(RECORDS[contact_name])

def hello(_):
    return "How can I help you?"

def exit(_):
    return "Good bye!"

@error_handler
def get_handler(command_list):
    return read_command_list(command_list)


def read_command_list(command_list: list):
    command = OPERATIONS[command_list.pop(0).lower()]
    command = read_command_list(command_list) if command == read_command_list else command
    return command

HANDLERS = {
    "hello": hello,
    "good_bye": exit,
    "close": exit,
    "exit": exit,
    "add": add,
    "change": change_phone,
    "show_all": show,
    "show": read_command_list,
    "phone": phone,
    "delete": delete_phone
}

def parser_input(user_input):
    cmd, *args = user_input.split()
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        if args:
            cmd = f"{cmd} {args[0]}"
            args = args[1:]
        handler = HANDLERS[cmd.lower(), "Unknown command"]
    return handler, args

def main():
    while True:
        user_input = input(">>>")
        handler, *args = parser_input(user_input)
        result = handler(*args)
        if not result:
            print("Good bye!")
            break
        print(result)


if __name__ == "__main__":
    main()