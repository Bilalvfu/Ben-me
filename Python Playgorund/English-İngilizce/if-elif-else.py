name = input(">")
age = int(input(">"))

if name == 'David':
    print('Hi, David.')
elif age < 12:
    print('You are not David, kid.')
elif age > 122:
    print('Nobody lived until this age.')

else:
    print('You are neither David nor a little kid.')
