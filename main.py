import pickle  # we use this library to work with address book files
import datetime  # getting the current time for greeting


class AddressBook:
    def __init__(self):
        with open('addressbook', 'rb') as file:  # loading saved contacts
            self.address_book = pickle.load(file)

    def saving(self, name_file):

        """The function is used to save changes"""

        with open(name_file, 'wb') as file:
            pickle.dump(self.address_book, file)

    @staticmethod
    def phone_number_conversion(number):

        """The function converts the phone number into a more readable one"""

        phone_number = ''  # for later saving a phone number consisting only of digits

        for symbol in number:  # we extract only digits from the entered number,
            try:  # because the user could enter additional characters
                int(symbol)
                phone_number += symbol
            except ValueError:
                continue

        if number[:2] != 's-' or number[:2] != 'S-':  # called only if a contact is added
            while 0 <= len(number) < 11:  # Be sure to enter the phone number
                number = input('You haven\'t entered phone number, try again --> ')

        # add separators to the phone number for easy reading (12345678901 --> 1 234 567-89-01)
        phone_number = f'{phone_number[0]} {phone_number[1:4]} {phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}'
        if number[:2] == 's-':
            counter = -1  # used to go through the number in reverse order in the case of a search
            while True:
                if phone_number[counter].isdigit():  # truncating the number when searching to the first digit
                    counter -= 1
                    break
                counter -= 1
            phone_number = phone_number[:counter + 1]

        if phone_number[0] == '8':  # we are replacing the country code for Russia
            phone_number = '+7' + phone_number[1:]
        elif number[0] == '7':  # we are replacing the country code for Russia
            phone_number = '+' + phone_number[:]
        return phone_number

    def add(self):

        """The function adds new contacts to the address book, saving them in a convenient form for further use"""

        print('==' * 70)  # separate
        print('Adding a new contact:')
        name = input('Name --> ')
        last_name = input('Last name (if there is a name) --> ')
        number = input('Phone number --> ')
        email = input('Email (if there is a name) --> ')

        while len(name) == 0:  # Be sure to enter the name
            name = input('You didn\'t enter a name, try again --> ')

        phone_number = self.phone_number_conversion(number)  # adding separators to a phone number

        contact_details = dict(phone_number=phone_number,  # we collect the data of a new contact in one dictionary
                               email=email if email != '' else 'No data available')

        try:
            self.address_book[name[0].upper()][name + ' ' + last_name] = contact_details
        except KeyError:
            self.address_book[name[0].upper()] = {name + ' ' + last_name: contact_details}

        self.saving('addressbook')  # Saving a new contact

        print('--' * 70)  # separate
        print('Contact successfully added.')
        print('==' * 70)  # separate

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
                    print('\nContact successfully deleted')
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
        # search by phone number
        if information[2].isdigit() or information[3].isdigit():
            # the type of the number changes to loaded in the dictionary
            phone_number = self.phone_number_conversion(information)
            keys = sorted(self.address_book)  # sort the first letters alphabetically
            for key in keys:
                for name, details in sorted(self.address_book[key].items()):  # we go through all the dictionary values
                    if details['phone_number'].startswith(phone_number):
                        contacts.append(name)
        else:  # search by name
            # we find all matching contacts
            information = information[2:]
            for key in self.address_book[information[0].upper()].keys():
                if key.startswith(information):
                    contacts.append(key)

        # output the number of found contacts
        if len(contacts) == 0:
            print('\nThe search yielded no results')
            return
        print(f'\n{len(contacts)} of contacts were found' if len(contacts) > 1 else
              f'\n{len(contacts)} contact was found')
        number = 1  # counters
        # output all found contacts
        for name in contacts:
            details = self.address_book[name[0].upper()][name]  # contact details
            print('==' * 70)  # separated
            print(f'{number})', end=' ')
            print(f'{name} (phone: {details["phone_number"]}', end='')
            print(', email: ' + details["email"] + ")" if details["email"] != "No data available" else ')')
            print('==' * 70)  # separated
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

    now = datetime.datetime.now().hour  # time at the moment
    # the output of the greeting depends on the time of day
    if 5 <= now < 12:
        print('Good morning!')
    elif 12 <= now < 17:
        print('Good afternoon')
    elif 17 <= now < 22:
        print('Good evening')
    elif 22 <= now < 5:
        print('Good night')

    # instructions for using the program
    print(
        'Instruction manual:\n'
        '\t- To add a contact, enter "+" and fill in the appropriate fields.\n'
        '\t- To view the entire contact list, enter "w" (watch)\n'
        '\t- To find the contact you need, enter "s-[contact name/phone number]" (search-...)\n'
        '\t- To delete a contact, enter "-[Contact name/first letter of the name and serial number]"\n'
        '\t- To exit, enter "e"(exit)')

    while True:  # program cycle
        print('What do you want to do')
        line = input('--> ')  # interaction string

        if line[0] == '+':  # adding a new contact
            user.add()

        elif line[0] == 'w' or line[0] == 'W' or line[0] == 'ц' or line[0] == 'Ц':  # view the entire contact book
            print(user)

        elif line[0] == '-':  # deleting a contact
            user.remove(line[1:])

        elif line[0:2] == 's-' or line[0:2] == 'S-':  # search for contact
            user.search(line)

        elif line[0] == 'e' or line[0] == 'E' or line[0] == 'у' or line[0] == 'У':  # exiting the program
            print('--' * 70)  # separate
            print('Good luck!')
            print('--' * 70)  # separate
            break
