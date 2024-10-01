
open = 0
closed = 1
a = open
b = closed


def splash():
    splash_length = 30
    row_1 = "Biathlon"
    row_2 = "A hit or miss game"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

def is_open(value):
    if(value == open):
        return True
    elif(value == closed):
        return False
        
def is_closed(value):
    if(value == closed):
        return True
    elif(value == open):
        return False
    
print(is_open(a))

def new_targets():
    targets = []
    for x in range(0, 5):
        targets.append(open)
    return(targets)
print(new_targets())
    
splash()
        
