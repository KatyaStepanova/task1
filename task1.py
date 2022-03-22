from dataclasses import dataclass, field


@dataclass
class Lwr_alphabet:
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
        'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    size: int = len(alphabet)


@dataclass
class Uppr_alphabet:
    alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
        'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
    size: int = len(alphabet)


class Endpoint():
    def __init__(self, p: int, g: int, private_key: int) -> None:
       self.__p = p
       self.__g = g
       self.__private_key = private_key
       self.__public_key = self.__generate_public_key()
       self.__endpoint_public_key = None
       self.__shift = None
       self.endpoint_message = ""

    def __generate_public_key(self) -> int:
        return self.__g ** self.__private_key % self.__p

    def __generate_general_secret_key(self) -> int:
        return self.__endpoint_public_key ** self.__private_key % self.__p

    def send_key(self, endpoint: "Endpoint"):
        endpoint.__endpoint_public_key = self.__public_key

    def __encryptCaesar(self, msg: str) -> str:
        res: str = ""
        for symbol in msg:
            if symbol.islower():
                idx = Lwr_alphabet.alphabet.index(symbol) % Lwr_alphabet.size
                res += Lwr_alphabet.alphabet[(idx + self.__shift) % Lwr_alphabet.size]
            elif symbol.isupper():
                idx = Uppr_alphabet.alphabet.index(symbol) % Uppr_alphabet.size
                res += Uppr_alphabet.alphabet[(idx + self.__shift) % Uppr_alphabet.size]
            else:
                res += symbol
        return res

    def __decryptCaesar(self, msg: str) -> str:
        res: str = ""
        for symbol in msg:
            if symbol.islower():
                idx = Lwr_alphabet.alphabet.index(symbol)
                res += Lwr_alphabet.alphabet[idx - self.__shift]
            elif symbol.isupper():
                idx = Uppr_alphabet.alphabet.index(symbol)
                res += Uppr_alphabet.alphabet[idx - self.__shift]
            else:
                res += symbol
        return res

    def establish_conn(self, endpoint: "Endpoint"):
        self.__shift = self.__generate_general_secret_key()

    def send_message(self, endpoint: "Endpoint", msg: str) -> str:
        endpoint.endpoint_message = self.__encryptCaesar(msg)

    def print_message(self):
        msg = self.__decryptCaesar(self.endpoint_message)
        print(f"{msg}")





if __name__ == '__main__':
    message_to_Bob = "Очень секретное сообщение."
    message_to_Alice = "Я принял."
    Alice_private = 4
    Bob_private = 3


    Alice = Endpoint(23, 9, Alice_private)
    Bob = Endpoint(23, 9, Bob_private)
    Alice.send_key(Bob)
    Bob.send_key(Alice)
    Alice.establish_conn(Bob)
    Bob.establish_conn(Alice)

    Alice.send_message(Bob, message_to_Bob)
    Bob.print_message()

    Bob.send_message(Alice, message_to_Alice)
    Alice.print_message()
