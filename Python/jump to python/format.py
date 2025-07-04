a = "{0:!^12}" .format("Python")
print(a)
b = f'{"Python":!^12}'
print(b)

number = 1234567890
formatted_number = f"{number:=^15,}"
print(formatted_number)

name = "Alice"
age = 25
a = f'"My name is {name} and I am {age} years old."'
print(a)

lang = "Python"
adj1 = "fun"
adj2 = "powerful"
a = ("{0} is {1} and {2}") .format(lang, adj1, adj2)
print(a)


name1 = "Alice"
name2 = "Bob"
print("Hello {0}, Hello {1}".format(name1, name2))

numbers = [1, 23, 456]
for n in numbers:
    print(f"{n:>3}")