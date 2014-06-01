class ASTToken:

    def __init__(self, t):
        self.kind = str(t.kind)
        self.spelling = str(t.spelling)
        
    def __eq__(self, obj):
        return isinstance(obj, ASTToken) and obj.kind == self.kind and obj.spelling == self.spelling 
    
    def __ne__(self, obj):
        return not self == obj
        
    def __str__(self):
        return self.kind + " : " + self.spelling
