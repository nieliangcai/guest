from zope.interface import Interface
from zope.interface.declarations import implementer

class IHost(Interface):
    def goodmorning(self,host):
        '''Say  Good morning to host'''

@implementer(IHost)
class Host:
    def goodmorning(self,guest):
        return 'Good morning ,%s ' %guest

if __name__=="__main__":
    p = Host()
    hi = p.goodmorning('Tom')
    print(hi)