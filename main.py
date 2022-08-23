import pickle  # we use this library to work with address book files


class AddressBook:
    def __init__(self):
        with open('addressbook', 'rb') as f:  # loading saved contacts
            self.address_book = pickle.load(f)

    def add(self):  # adding new contacts
        print('Adding a new contact:\n')
        name = input('Name --> ')
        last_name = input('Last name (if there is a name) --> ')
        phone_number = input('Phone number --> ')
        email = input('Email (if there is a name) --> ')

        while len(name) == 0:  # Be sure to enter the name
            name = input('You didn\'t enter a name, try again --> ')

        while len(phone_number) == 0:  # Be sure to enter the phone number
            phone_number = input('You haven\'t entered phone number, try again --> ')


if __name__ == '__main__':
    user = AddressBook()

    while True:  # program cycle
        print('Если вы хотите добавить контакт, введите "+"\n')
        user.line = input('--> ')  # interaction string
        if user.line[0] == '+':
            user.add()
        if user.line[0] == 'e':
            break
