from typing import List


class Stack:
    def __init__(self, *args):
        self.elements: List = list(args)

    def push(self, e):
        self.elements.append(e)

    def pop(self):
        return self.elements.pop()

    def peek(self):
        return self.elements[-1] if self.elements else None


stack = Stack()
