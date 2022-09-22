class Stack:
      
    def __init__(self):
        self.stack =[]
        self.top =-1

    def pop(self):
        if self.top ==-1:
            return
        else:
            self.top-= 1
            return self.stack.pop()
            
    def push(self, i):
        self.top+= 1
        self.stack.append(i)
  