import re

Operators = set(['&', '|', '-', '(', ')' ])  # collection of Operators

Priority = {'&':1, '|':1, '-':2} # dictionary having priorities of Operators
 

# Complexity - 
#   Time - O(q) where q = length of query expression
#   Space - O(q)
def processQueryToPostfix(expression: str) -> str: 

    stack = [] # initialization of empty stack

    output = '' 

    expression = expression.replace("!", "# - ")
    expression = re.sub(r"\((?!\s)","( ",expression)
    expression = re.sub(r"(?!\s)\)"," )",expression)
    exp_list = expression.split(" ")
    

    for character in exp_list:

        if character not in Operators:  # if an operand append in postfix expression

            output += character.lower() + " "

        elif character=='(':  # else Operators push onto stack

            stack.append('(')

        elif character==')':

            while stack and stack[-1]!= '(':

                output+= stack.pop() + " "

            stack.pop()

        else: 

            while stack and stack[-1]!='(' and Priority[character]<=Priority[stack[-1]]:

                output+=stack.pop() + " "

            stack.append(character)
        


    while stack:

        output+=stack.pop() + " "

    #print("OUtput: "+output)
    return output.rstrip().lstrip()


def main():
    expression = "Neeva & hello | !(But | no)"

    print('infix notation: ',expression)

    print('postfix notation: ', processQueryToPostfix(expression))

if __name__ == "__main__":
    main()