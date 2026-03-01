import random
def generate_pass():
    ascii=list(range(97,123))
    alpha=[chr(i) for i in ascii]
    digit=list(range(0,10))
    symbol=['_','$','@','#']

    p1=random.choices(alpha,k=2)+random.choices(digit,k=2)+random.choices(symbol,k=1)
    random.shuffle(p1)
    pwd=''
    for i in p1:
        pwd+=str(i)
    
    return pwd
generate_pass()