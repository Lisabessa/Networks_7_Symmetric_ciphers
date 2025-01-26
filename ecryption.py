from collections import Counter
import random
import string

class CaesarCipher:
    def encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if 'A' <= char <= 'Z':  # Заглавные латиницы 
                encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':  # Строчные латиница
                encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif 'А' <= char <= 'Я':  # Заглавные кириллица
                encrypted_text += chr((ord(char) - ord('А') + shift) % 32 + ord('А'))
            elif 'а' <= char <= 'я':  # Строчные кириллица
                encrypted_text += chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
            else:
                encrypted_text += char  # Не изменяем не буквенные символы
        return encrypted_text


    def decrypt(self, encrypted_text, shift):
        return self.encrypt(encrypted_text, -shift)  # Дешифрование = шифрование с отрицательным сдвигом
    

    def decrypt_without_key_enumeration(self, encrypted_text):
        possible_results = []
        for shift in range(1, 33):  # Перебор сдвигов от 1 до 32
            decrypted = self.decrypt(encrypted_text, shift)
            possible_results.append((shift, decrypted))
        return possible_results
    

    def frequency_analysis(self, encrypted_text):
        letter_counts = Counter(filter(str.isalpha, encrypted_text.upper())) # Подсчет частоты букв
        most_common = letter_counts.most_common(1)
    
        if most_common: # Предполагаем, что самая частая буква в тексте - это 'е'
            common_letter = most_common[0][0]
            shift = (ord(common_letter) - ord('е')) % 32
            return shift
        return None


    def decrypt_without_key_fa(self, encrypted_text):
        shift = self.frequency_analysis(encrypted_text)
        if shift is not None:
            return self.decrypt(encrypted_text, shift)
        return "Не удалось восстановить текст."

    
class VernamCipher():
    def encrypt(self, text, key):
        if len(text) != len(key):
            raise ValueError("Длина ключа должна совпадать с длиной текста")
        encrypted = ''.join(chr(ord(t) ^ ord(k)) for t, k in zip(text, key))
        return encrypted

    def decrypt(self, encrypted_text, key):
        return self.encrypt(encrypted_text, key)  # XOR-симметрия


def main():
    phrase1 = 'Неет, нельзя не ехать, точно быть.'
    phrase2 = 'Joe and Josh went to the market and bought a secret gift for Mathew - it is a new laptop!!!'
    print('Фразы:', phrase1, phrase2, sep='\n', end='\n\n')

    caesar = CaesarCipher()

    enc1 = caesar.encrypt(phrase1, 3)
    enc2 = caesar.encrypt(phrase2, 10)
    print('Зашифрованные фразы шифром Цезаря:', enc1, enc2, sep='\n', end='\n\n')

    dec1 = caesar.decrypt(enc1, 3)
    dec2 = caesar.decrypt(enc2, 10)
    print('Расшифрованные фразы шифром Цезаря:', dec1, dec2, sep='\n', end='\n\n')

    dec1_wk = caesar.decrypt_without_key_fa(enc1)
    print('Расшифрованная первая фраза с помощью частотного анализа:', dec1_wk, sep='\n', end='\n\n')

    variants2 = caesar.decrypt_without_key_enumeration(enc2)
    print('Варианты расшифровки второй фразы подбором:', variants2, sep='\n', end='\n\n')

    vernam = VernamCipher()
    key_vernam1 = ''.join(random.choice(string.ascii_letters) for _ in range(len(phrase1)))
    key_vernam2 = ''.join(random.choice(string.ascii_letters) for _ in range(len(phrase2)))

    enc1 = vernam.encrypt(phrase1, key_vernam1)
    enc2 = vernam.encrypt(phrase2, key_vernam2)
    print('Зашифрованные фразы шифром Вернама:', enc1, enc2, sep='\n', end='\n\n')

    dec1 = vernam.decrypt(enc1, key_vernam1)
    dec2 = vernam.decrypt(enc2, key_vernam2)
    print('Расшифрованные фразы шифром Вернама:', dec1, dec2, sep='\n', end='\n\n')


main()