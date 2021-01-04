import random
import sqlite3


class Banking:

    def __init__(self, con, cursor):
        self.card = cursor.execute("""CREATE TABLE IF NOT EXISTS card 
                                    (id INTEGER,
                                    number TEXT, 
                                    pin TEXT,
                                    balance INTEGER DEFAULT 0)
                                    ;""")
        self.db_conn = con
        self.db_cursor = cursor
        self.current_user = {}

    @staticmethod
    def generate_pin():
        pin = str(random.randint(0, 9)) + \
              str(random.randint(0, 9)) + \
              str(random.randint(0, 9)) + \
              str(random.randint(0, 9))
        return pin

    @staticmethod
    def validation(card_number):
        num_list = list(card_number)
        for dig in range(0, len(num_list)):
            num_list[dig] = int(num_list[dig])
        check_list = []
        for i, j in enumerate(num_list):
            i += 1
            if i % 2 != 0:
                j *= 2
                if j > 9:
                    j -= 9
            check_list.append(j)
        s = sum(check_list)
        for i in range(10):
            if (s + i) % 10 == 0:
                return i

    def generate_card_number(self):
        card_number = '400000' + \
                      str(random.randint(int(1e8), int(9.99e8)))
        valid_number = card_number + str(self.validation(card_number))
        return valid_number

    def first_menu(self):
        print("1. Create an account\n2. Log into an account\n0. Exit")
        request = int(input())
        if request == 1:
            self.create_db_entry()
            self.first_menu()
        elif request == 2:
            self.request_db_entry()
            if len(self.current_user) != 0:
                print('You have successfully logged in!')
                self.second_menu()
            else:
                print('Wrong card number or PIN!')
                self.first_menu()
        elif request == 0:
            self.exit()

    def second_menu(self):
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        request1 = int(input())
        if request1 == 1:
            print(f"Balance: {self.check_balance()}")
            self.second_menu()
        elif request1 == 2:
            self.add_income()
            print('Income was added!')
            self.second_menu()
        elif request1 == 3:
            self.do_transfer()
            self.second_menu()
        elif request1 == 4:
            self.close_account()
            self.second_menu()
        elif request1 == 5:
            self.log_out()
            self.first_menu()
        elif request1 == 0:
            self.exit()

    def update_current_user(self, ids, number, pin, balance):
        self.current_user['id'] = ids
        self.current_user['number'] = number
        self.current_user['pin'] = pin
        self.current_user['balance'] = balance

    def create_db_entry(self):
        new_card_number = self.generate_card_number()
        new_pin = self.generate_pin()
        int_id = int(new_card_number)
        self.db_cursor.execute(f"INSERT INTO card VALUES ({int_id}, {new_card_number}, {new_pin}, 0)")
        self.db_conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{new_card_number}')
        print(f'Your card PIN:\n{new_pin}\n')

    def request_db_entry(self):
        print('Enter your card number: ')
        card_number = input()
        print('Enter your PIN: ')
        pin = input()
        q_number = str(card_number)
        q_pin = str(pin)
        try:
            self.db_cursor.execute(f"SELECT id, number, pin, balance "
                                   f"FROM card "
                                   f"WHERE number = {q_number} AND pin = {q_pin}")
            current_data = self.db_cursor.fetchone()
            self.update_current_user(ids=current_data[0],
                                     number=current_data[1],
                                     pin=current_data[2],
                                     balance=current_data[3])
        except Exception as e:
            pass

    def check_balance(self):
        cid = self.current_user['id']
        self.db_cursor.execute(f"SELECT balance FROM card WHERE id = {cid};")
        return self.db_cursor.fetchone()[0]

    def add_income(self):
        print('Enter income:')
        income = int(input())
        card_id = self.current_user['id']
        self.db_cursor.execute(f"UPDATE card "
                               f"SET balance = balance + {income} "
                               f"WHERE id = {card_id};")
        self.db_conn.commit()

    def do_transfer(self):
        print('Transfer')
        print('Enter card number: ')
        target = int(input())
        to_validate = str(target)
        error = 0
        self.db_cursor.execute(f"SELECT id FROM card WHERE id = {target};")
        check = self.db_cursor.fetchone()
        if target == self.current_user['id']:
            print("You can't transfer money to the same account!")
            error += 1
        elif self.validation(to_validate[:-1]) != int(to_validate[-1]):
            print("Probably you made a mistake in the card number. Please try again!")
            error += 1
        elif check is None:
            print("Such a card does not exist.")
            error += 1
        if error == 0:
            print('Enter how much money you want to transfer:')
            amount = int(input())
            if amount > self.check_balance():
                print('Not enough money!')
            else:
                self.db_cursor.execute(f"UPDATE card "
                                       f"SET balance = balance - {amount} "
                                       f"WHERE id = {self.current_user['id']};")
                self.db_conn.commit()
                self.db_cursor.execute(f"UPDATE card "
                                       f"SET balance = balance + {amount} "
                                       f"WHERE id = {target};")
                self.db_conn.commit()
                print("Success!")

    def close_account(self):
        self_id = self.current_user['id']
        self.db_cursor.execute(f"DELETE FROM card WHERE id = {self_id}")
        self.db_conn.commit()
        print("The account has been closed!")

    def reset_balance_to_zero(self):
        self.db_cursor.execute("UPDATE card SET balance = 0;")
        self.db_conn.commit()

    @staticmethod
    def log_out():
        print('You have successfully logged out!')

    @staticmethod
    def exit():
        print("Bye!")

    def run_app(self):
        self.first_menu()


if __name__ == '__main__':
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    bank = Banking(conn, cur)
    bank.run_app()
