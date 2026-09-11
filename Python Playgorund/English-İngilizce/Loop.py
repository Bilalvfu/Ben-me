import random

secret_number = random.randint(1, 20)
print('I am thinking of a number between 1 and 20.')


for guesses_taken in range(1, 7):
    print('Take a guess.')
    guess = int(input('>'))

    if guess == secret_number:
        break

    # Farkı hesapla
    fark = abs(guess - secret_number)

    if guess == secret_number // 2:
        print('Half, too close!')
    elif fark <= 2:
        print('Too close.')
    elif fark <= 5:
        print('Getting close.')
    elif guess < secret_number:
        print('Your guess is too low.')
    else:
        print('Your guess is too high.')

if guess == secret_number:
    print('Good job! You got it in ' + str(guesses_taken) + ' guesses!')
else:
    print('Nope. The number was ' + str(secret_number))
