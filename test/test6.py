class Demo:
    a = 9
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, value):
        setattr(self, key)
    def __delitem__(self, key):
        delattr(self, key)
    

a = Demo()
print(a["a"])
