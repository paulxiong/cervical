""" ……波斯国王一定要智慧王子死，又要当众侮辱卖弄一番，就对王子说：有两种死法，
猜对就绞死，猜错就砍死，猜猜你会怎么死？猜对了就赦免你……王子答：我会被你砍死…… """
#!/usr/bin/python

import sys, getopt

def main(argv):
    doc = '……波斯国王一定要智慧王子死，又要当众侮辱卖弄一番，就对王子说：有两种死法，猜对就绞死，猜错就砍死，猜猜你会怎么死？猜对了就赦免你……王子答：我会被你砍死……'

    print (doc)
    inputChoice = ''
    outputDecision = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["选择="])
    except getopt.GetoptError:
        print ('king-prince.py -i  <选择：绞死或者砍死>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('king-prince.py -i <选择>')
            sys.exit()
        elif opt in ("-i"):
            if arg in ("绞死", "砍死"):
                inputChoice = arg
                execution(inputChoice)
                sys.exit()
    print ('king-prince.py -i  <选择：绞死或者砍死>' )

def execution(inputChoice):
    exec = '绞死'
    print('你选择了：'+inputChoice)
    print('如果国王'+ exec+"你")
    if inputChoice == exec:
        print('----猜对就绞死，国王应该绞死你')
        if exec == '绞死':
            sys.exit()
    else:
        print('----猜错就砍死 国王应该砍死你')
        if exec == '砍死':
            sys.exit()
    exec = '砍死'
    print('如果国王'+ exec+"你")
    if inputChoice == exec:
        print('----猜对就绞死，国王应该绞死你')
        if exec == '绞死':
            sys.exit()
    else:
        print('----猜错就砍死， 国王应该砍死你')
        if exec == '砍死':
           sys.exit()
    print("自相矛盾，国王无法行刑！！！")       

if __name__ == "__main__":
    main(sys.argv[1:])