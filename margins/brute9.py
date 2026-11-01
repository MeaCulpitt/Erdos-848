import sys
exec(open('brute.py').read().replace("return (k*3+mu)*7+[0,1,2,0,3,4,0,5,6][a%9]","return (k*3+mu)*7"))
