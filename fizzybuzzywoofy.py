

def fizzybuzzywoofy(meow):
    returnerthingy = ""
    array = [3,5,7]
    if meow % (3*5*7)   == 0:
        returnerthingy = "fizzbuzzwoof"
    elif  meow % (3*5)  == 0:
        returnerthingy = "fizzbuzz"
    elif meow % (3*7) ==0:
        returnerthingy = "fizzwolf"
    elif  meow  % (5*7)  == 0:
        returnerthingy = "buzzwolf"
    elif meow % 3  == 0:
        print("fizz")
    elif meow % 5 == 0:
        print("buzz")
    elif meow % 7 == 0:
        print("wolf")
    else:
        print("this sucks")
    print(returnerthingy)

fizzybuzzywoofy(5)
