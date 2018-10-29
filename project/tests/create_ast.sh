#!/bin/bash

# defines needed variables.
ANTLR_JAR="antlr4.jar"
GRAMMAR="Solidity"
DLANGUAGE="-Dlanguage=Python3"
START_RULE="sourceUnit"
TYPE="-tree"
FILE=$1

# makes sure that antlr4 is installed.
if [ ! -e "$ANTLR_JAR" ]; then
  curl http://www.antlr.org/download/antlr-4.7-complete.jar -o "$ANTLR_JAR"
fi

# creates a directory for the parsing tools, -p is so it can be used as an operand.
mkdir -p parsetools/

# creates Solidity lexer, parser and listeners.
java -jar $ANTLR_JAR $GRAMMAR.g4 -o src/

# creates the Solidity parsing tools and adds them to parsetool.
javac -classpath $ANTLR_JAR src/*.java -d parsetools/

# creates the AST from the given contract file.
java -classpath $ANTLR_JAR:parsetools/ org.antlr.v4.gui.TestRig "$GRAMMAR" "$START_RULE" "$TYPE" < "$FILE" 2>&1 

