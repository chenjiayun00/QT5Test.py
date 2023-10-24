import re
import math

def jzcToJzdtxt(jzcstr):
    resultstr = ""
    arrystr = str.split(jzcstr, "\n")
    for line in arrystr:
        arry = ""
        a = re.search("[0-9a-fA-F]{2,}", line).group()
        if len(a)%2 == 0:
            for i in range(math.floor(len(a)/2)):
                # print(a[i*2:i*2+2])
                arry = str.format(arry + "0x" + a[i*2:i*2+2] + ",")
        else:
            print("ERROR:请检查长度是否正确")
        print(arry.strip(","))
if __name__ == "__main__":
    jzcstr = "s_w(7785000443054218E70584AD6C05C742\n320609D2054E77DE83B0025011FB83009BA822026F)"
    jzcToJzdtxt(jzcstr)
