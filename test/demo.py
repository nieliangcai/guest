class Host(object):
    def goodmorning(self,name):

        return "goodmorning %s" %name

if __name__=="__main__":
    h = Host()
    hi = h.goodmorning('yyy')
    print(hi)