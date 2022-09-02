import pickle  # we use this library to work with address book files


class AddressBook:
    def __init__(self):
        with open('addressbook', 'rb') as file:  # loading saved contacts
            self.address_book = pickle.load(file)

    def saving(self, name_file):

        """The function is used to save changes"""

        with open(name_file, 'wb') as file:
            pickle.dump(self.address_book, file)

    def phone_number_conversion(self, number):

        """The function converts the phone number into a more readable one"""

        phone_number = ''  # for later saving a phone number consisting only of digits

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
        elif number[0] == '7':  # we are replacing the country code for Russia
            phone_number = '+' + phone_number[:]
        return phone_number

    def add(self):

        """The function adds new contacts to the address book, saving them in a convenient form for further use"""

        print('Adding a new contact:')
        name = input('Name --> ')
        last_name = input('Last name (if there is a name) --> ')
        number = input('Phone number --> ')
        email = input('Email (if there is a name) --> ')

        while len(name) == 0:  # Be sure to enter the name
            name = input('You didn\'t enter a name, try again --> ')

        while 0 <= len(number) < 11:  # Be sure to enter the phone number
            number = input('You haven\'t entered phone number, try again --> ')

        phone_number = self.phone_number_conversion(number)  # adding separators to a phone number

        contact_details = dict(phone_number=phone_number,  # we collect the data of a new contact in one dictionary
                               email=email if email != '' else 'No data available')

        try:
            self.address_book[name[0].upper()][name + ' ' + last_name] = contact_details
        except KeyError:
            self.address_book[name[0].upper()] = {name + ' ' + last_name: contact_details}

        self.saving('addressbook')  # Saving a new contact

        print('Contact successfully added.')

    def remove(self, information):

        """The function deletes the contact by the entered number and the first letter or by part of the entered name"""

        try:
            # if the contact numbers is entered
            contact_number = int(information[1])
            number = 1  # counter
            # we sort through the contacts and find the right one in order
            for name in sorted(self.address_book[information[0].upper()].keys()):
                if contact_number == number:  # matching numbers
                    self.address_book[information[0].upper()].pop(name)
                    self.saving('addressbook')  # Saving changes
                    print('Contact successfully deleted')
                    break
                number += 1

        except ValueError:
            # if the contact name is entered
            # contacts starting with the first letter entered
            possible_contact = self.address_book[information[0].upper()]
            # we sort through all possible contacts and delete the one that starts the same way
            for key in possible_contact.keys():
                if key.startswith(information[:]):
                    self.address_book[information[0].upper()].pop(key)
                    self.saving('addressbook')  # Saving changes
                    print('Contact successfully deleted')
                    break

    def search(self, information):

        """The function searches for a contact by name or by phone number"""

        contacts = []
        try:  # search by phone number
            int(information[3])
            phone_number = self.phone_number_conversion(information)  # replacing the country code for Russia
            keys = sorted(self.address_book)  # sort the first letters alphabetically
            for key in keys:
                for name, details in sorted(self.address_book[key].items()):  # we go through all the dictionary values
                    if details['phone_number'].startswith(phone_number):
                        contacts.append(name)

        except ValueError:  # search by name
            # we find all matching contacts
            for key in self.address_book[information[0].upper()].keys():
                if key.startswith(information):
                    contacts.append(key)

        # output the number of found contacts
        if len(contacts) == 0:
            print('The search yielded no results')
            return
        print(f'{len(contacts)} of contacts were found' if len(contacts) > 1 else
              f'{len(contacts)} contact was found')
        number = 1  # counters
        # output all found contacts
        for name in contacts:
            details = self.address_book[name[0].upper()][name]  # contact details
            print(f'{number})', end=' ')
            print(f'{name} (phone: {details["phone_number"]}', end='')
            print(', email: ' + details["email"] + ")" if details["email"] != "No data available" else ')')
            number += 1

    def __str__(self):

        """Displays the entire contact list in order"""

        keys = sorted(self.address_book)  # sort the first letters alphabetically
        print('==' * 70)  # separated
        for key in keys:
            print(' ' * 2 + key)  # output the first letters
            number = 1  # counter
            for name, details in sorted(self.address_book[key].items()):  # going through the dictionary of each letter
                # output only available data
                print(f'{number})', end=' ')
                print(f'{name} (phone: {details["phone_number"]}', end='')
                print(', email: ' + details["email"] + ")" if details["email"] != "No data available" else ')')
                number += 1
        return '==' * 70  # separated


if __name__ == '__main__':
    user = AddressBook()

    while True:  # program cycle
        print('Если Вы хотите добавить контакт, введите: "+"')
        line = input('--> ')  # interaction string

        if line[0] == '+':
            user.add()

        elif line[0] == 'e':
            break

        elif line[0] == 'w':
            print(user)

        elif line[0] == '-':
            user.remove(line[1:])

        elif line[0:2] == 's-':
            user.search(line[2:])
