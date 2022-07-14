with open('f1.txt', 'r') as f1, open('f2.txt', 'w') as f2:
    f2.writelines(f1.readlines())
