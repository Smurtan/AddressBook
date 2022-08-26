import pickle  # we use this library to work with address book files


class AddressBook:
    def __init__(self):
        with open('addressbook', 'rb') as f:  # loading saved contacts
            self.address_book = pickle.load(f)
            print(self.address_book)

    def add(self):

        """The function adds new contacts to the address book, saving them in a convenient form for further use"""

        print('Adding a new contact:')
        name = input('Name --> ')
        last_name = input('Last name (if there is a name) --> ')
        number = input('Phone number --> ')
        email = input('Email (if there is a name) --> ')

        phone_number = ''  # for later saving a phone number consisting only of digits

        while len(name) == 0:  # Be sure to enter the name
            name = input('You didn\'t enter a name, try again --> ')

        while len(number) == 0:  # Be sure to enter the phone number
            number = input('You haven\'t entered phone number, try again --> ')

        for symbol in number:  # we extract only digits from the entered number,
            try:  # because the user could enter additional characters
                int(symbol)
                phone_number += symbol
            except ValueError:
                continue

        phone_number = f'{phone_number[0]} {phone_number[1:4]} {phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}'
        # add separators to the phone number for easy reading (12345678901 --> 1 234 567-89-01)

        if phone_number[0] == '8':  # we are replacing the country code for Russia
            phone_number = '+7' + phone_number[1:]

        contact_details = dict(phone_number=phone_number,  # we collect the data of a new contact in one dictionary
                               last_name=last_name if last_name != '' else 'No data available',
                               email=email if email != '' else 'No data available')

        try:
            self.address_book[name[0].upper()][name] = contact_details
        except KeyError:
            self.address_book[name[0].upper()] = {name:contact_details}

        with open('addressbook', 'wb') as f:  # Saving a new contact
            pickle.dump(self.address_book, f)

        print('Contact successfully added.')


if __name__ == '__main__':
    user = AddressBook()

    while True:  # program cycle
        print('Если Вы хотите добавить контакт, введите: "+"')
        line = input('--> ')  # interaction string

        if line[0] == '+':
            user.add()

        elif line[0] == 'e':
            break
