import sys
from pathlib import Path

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from antlr4 import *
from choreography.ChoreographyLexer import ChoreographyLexer
from choreography.ChoreographyParser import ChoreographyParser
from machine.MyChoreographyVisitor import MyChoreographyVisitor

def main():
    # Read input from file
    with open("/Users/chukrisoueidi/Src/lena/machine/machine-lena/test/sample.chor", "r") as file:
        input_stream = InputStream(file.read())

    # Create a lexer and parser
    lexer = ChoreographyLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ChoreographyParser(stream)

    # Parse the input and create a parse tree
    tree = parser.choreography()

    # Create and apply the visitor
    visitor = MyChoreographyVisitor()
    visitor.visit(tree)

if __name__ == "__main__":
    main()


 