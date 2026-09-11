import random

secret_number = random.randint(1, 20)
print('1 ile 20 arasında bir sayı tuttum.')

for guesses_taken in range(1, 7):
    print('Bir tahminde bulun.')
    guess = int(input('>'))

    if guess == secret_number:
        break

    fark = abs(guess - secret_number)

    if guess == secret_number // 2:
        print('Tam yarısı, çok yaklaştın!')
    elif fark <= 2:
        print('Çok yaklaştın!')
    elif fark <= 5:
        print('Yaklaşıyorsun...')
    elif guess < secret_number:
        print('Tahminin çok düşük.')
    else:
        print('Tahminin çok yüksek.')

if guess == secret_number:
    print('Tebrikler! ' + str(guesses_taken) + ' tahminde bildin!')
else:
    print('Maalesef. Tuttuğum sayı ' + str(secret_number) + ' idi.')
