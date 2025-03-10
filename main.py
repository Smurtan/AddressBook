import pickle  # we use this library to work with address book files
import datetime  # getting the current time for greeting


class AddressBook:

    """The class combines all the functions of the address book, presented in the form of functions"""

    def __init__(self):
        with open('addressbook', 'rb') as file:  # loading saved contacts
            self.address_book = pickle.load(file)
        self.separator = '==' * 70
        self.separator_ = '--' * 70
        # instructions for using the program
        self.instruction = (
            '\u001b[33mInstruction manual:\n'
            '\t- To add a contact, enter "\u001b[31m+\u001b[33m" and fill in the appropriate fields.\n'
            '\t- To view the entire contact list, enter "\u001b[31mw\u001b[33m" (watch)\n'
            '\t- To find the contact you need, enter "\u001b[31ms-[contact name/phone number]" (search-...)\u001b[33m\n'
            '\t- To delete a contact, enter '
            '"\u001b[31m-[Contact name/first letter of the name and serial number]\u001b[33m"\n'
            '\t- To exit, enter "\u001b[31me\u001b[33m"(exit)\n'
            '\t- If you want to look at the instructions again, enter "\u001b[31mI\u001b[33m" (Instruction)')

    def saving(self, name_file):

        """The function overwrites the file and saves all changes"""

        with open(name_file, 'wb') as file:
            pickle.dump(self.address_book, file)

    @staticmethod
    def phone_number_conversion(number):

        """The function converts the phone number into a more readable one (XXXXXXXXXXX --> X XXX XXX-XX-XX)"""

        phone_number = ''  # for later saving a phone number consisting only of digits

        for symbol in number:  # we extract only digits from the entered number,
            try:  # because the user could enter additional characters
                int(symbol)
                phone_number += symbol
            except ValueError:
                continue

        if number[:2] != 's-' and number[:2] != 'S-':  # called only if a contact is added
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

        print(self.separator)  # separate
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

        print(self.separator_)  # separate
        print('Contact successfully added.')
        print(self.separator)  # separate

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
                    # delete the letter if no more contacts start on it
                    if len(self.address_book[information[0].upper()]) == 0:
                        del self.address_book[information[0].upper()]
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
                    # delete the letter if no more contacts start on it
                    if len(self.address_book[information[0].upper()]) == 0:
                        del self.address_book[information[0].upper()]
                    break

    def search(self, information):

        """The function searches for a contact by name or phone number and displays all the contacts found"""

        contacts = []
        # search by phone number
        if information[2].isdigit() or information[2] == '+':
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
            try:
                for key in self.address_book[information[0].upper()].keys():
                    if key.startswith(information):
                        contacts.append(key)
            except KeyError:
                pass

        # output the number of found contacts
        if len(contacts) == 0:
            print(self.separator_)  # separated
            print('The search yielded no results')
            print(self.separator_)  # separated
            return
        print(f'\n{len(contacts)} of contacts were found' if len(contacts) > 1 else
              f'\n{len(contacts)} contact was found')
        number = 1  # counters
        # output all found contacts
        print(self.separator)  # separated
        for name in contacts:
            details = self.address_book[name[0].upper()][name]  # contact details
            print(f'{number})', end=' ')
            print(f'{name} (phone: {details["phone_number"]}', end='')
            print(', email: ' + details["email"] + ")" if details["email"] != "No data available" else ')')
            number += 1
        print(self.separator)  # separated

    def __str__(self):

        """Displays the entire contact list in order"""

        keys = sorted(self.address_book)  # sort the first letters alphabetically
        print(self.separator)  # separate
        for key in keys:
            print(' ' * 2 + key)  # output the first letters
            number = 1  # counter
            for name, details in sorted(self.address_book[key].items()):  # going through the dictionary of each letter
                # output only available data
                print(f'{number})', end=' ')
                print(f'{name} (phone: {details["phone_number"]}', end='')
                print(', email: ' + details["email"] + ")" if details["email"] != "No data available" else ')')
                number += 1
        return '==' * 70  # separate


if __name__ == '__main__':
    user = AddressBook()

    now = datetime.datetime.now().hour  # time at the moment
    # the output of the greeting depends on the time of day
    if 5 <= now < 12:
        print('\u001b[32mGood morning!')
    elif 12 <= now < 17:
        print('\u001b[32mGood afternoon')
    elif 17 <= now < 22:
        print('\u001b[32mGood evening')
    elif 22 <= now < 5:
        print('\u001b[32mGood night')

    # instructions for using the program
    print(user.instruction)

    while True:  # program cycle
        print('\n\u001b[31mWhat do you want to do')
        line = input('--> \u001b[0m')  # interaction string

        if line[0] == '+':  # adding a new contact
            user.add()

        elif line[0] == 'w' or line[0] == 'W' or line[0] == 'ц' or line[0] == 'Ц':  # view the entire contact book
            print(user)

        elif line[0] == '-':  # deleting a contact
            user.remove(line[1:])

        elif line[0:2] == 's-' or line[0:2] == 'S-':  # search for contact
            user.search(line)

        elif line[0] == 'i' or line[0] == 'I':  # outputs the instruction
            print(user.instruction)

        elif line[0] == 'e' or line[0] == 'E' or line[0] == 'у' or line[0] == 'У':  # exiting the program
            print(user.separator_)  # separate
            print('\u001b[32;1mGood luck!\u001b[0m')
            print(user.separator_)  # separate
            break

        else:
            print('\u001b[31mThe command entered is not correct.\nLook at the instructions and try again.\u001b[0m')
