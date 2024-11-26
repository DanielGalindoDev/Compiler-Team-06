

# Introduction

For this project, we will develop the compiler in a way that allows us to implement and understand each of its phases, gaining insight into how high-level code is transformed into machine-readable code. Throughout the process, we will explore how Python, along with its libraries, can be utilized for the construction of the compiler. Additionally, we will delve into its internal architecture and examine the functionality of each phase in detail.

The compiler is a fundamental tool that reveals the internal processes linking programming languages to hardware. This includes lexical analysis, syntax analysis, semantic analysis, intermediate code generation, code optimization, and final code generation. The project aims to tackle the challenges of implementing each phase while addressing any issues that arise during the process, with the goal of understanding their importance and functionality.

Furthermore, it highlights the essential role compilers play in modern software development and language engineering, enabling the efficient execution of programs and making programming more accessible through high-level languages. By combining theoretical knowledge with practical implementation, this project not only emphasizes the complexities of building a compiler but also underscores its relevance, as it serves as a bridge between human-readable code and hardware execution.

## 1.1 Motivation

After studying each phase of the compiler and completing the Lexical, Syntax, and Semantic Analysis stages, our challenge is to continue with the remaining phases to complete the compiler development process. This goal not only represents a challenge but also an opportunity to reinforce the knowledge we have been studying throughout the course or acquiring through programming languages. It provides an opportunity to not just create programs but also to understand how they work internally, how the source code we write is processed by the computer to be executed, and how it connects to the computer’s hardware.

We will gain a practical understanding of the fundamental concepts of the remaining phases, such as intermediate code generation, code optimization, and target code generation. This project will also allow us to test our abilities to analyze and resolve difficulties that arise during the compiler development process, collaborate as a team, and ultimately achieve the goal of creating a functional compiler.
# Theoretical Framework

## 2.1 Compiler

A compiler is a specialized program designed to translate a source program written in one programming language (the source language) into an equivalent program in another language (the target language), such as machine code, bytecode, or even another high-level language. This translation enables the code written by a programmer to be executed either directly by the computer's hardware or within an intermediate runtime environment.

Compilers carry out this process through multiple stages, including lexical analysis, syntax analysis, semantic analysis, optimization, and code generation. Additionally, an essential function of a compiler is to identify and report any errors in the source code that are detected during the translation process, ensuring the correctness and reliability of the generated program.

---

## 2.2 Compiler Architecture

### 2.2.1 Lexical Analysis
The first phase of a compiler is called lexical analysis or scanning. The lexical analyzer reads the stream of characters that make up the source program and groups them into meaningful sequences, known as lexemes. For each lexeme, the lexical analyzer produces an output token in the form: `(token-name, attribute-value)`, which is passed to the next phase, syntax analysis.

In the token, the first component, *token-name*, is an abstract symbol used during syntax analysis, while the second component, *attribute-value*, points to an entry in the symbol table for that token.

---

### 2.2.2 Syntax Analysis
The second phase of the compiler, the parser, uses the first components of the tokens produced by the lexical analyzer to create a tree-like intermediate representation that depicts the grammatical structure of the token stream. A typical representation is a syntax tree in which each interior node represents an operation and the children of the node represent the arguments of the operation.

---

### 2.2.3 Semantic Analysis
The semantic analyzer uses the syntax tree and the information in the symbol table to check the source program for semantic consistency with the language definition. It also gathers type information and saves it in either the syntax tree or the symbol table for subsequent use during intermediate-code generation. An important part of semantic analysis is type checking, where the compiler checks that each operator has matching operands.

---

### 2.2.4 Intermediate Code Generation
During the translation of a source program into the object code for a target machine, a compiler often generates an intermediate representation, also known as intermediate code or intermediate text. This intermediate code is typically a low-level or machine-like representation that can be viewed as a program for an abstract machine.

---

### 2.2.5 Three Address Code
As we already know, there are two main types of intermediate code generation: graph-based representations such as the AST (Abstract Syntax Tree) and DAG (Directed Acyclic Graph), and linear representations such as Three-Address Code. The basic instruction of three-address code is designed to represent the evaluation of arithmetic expressions, although not exclusively, and has the following general form:
x = y op z

Main types of three-address code statements:
- Binary and unary assignments (e.g., `x = op y` or `x = y op z`).
- Copy instructions (e.g., `x = y`).
- Indexed copy instructions (e.g., `x = T[b]` and `T[b] = x`).

---

### 2.2.6 Code Optimization
The machine-independent code-optimization phase attempts to improve the intermediate code so that better target code will result. Usually, better means faster, but other objectives may be desired, such as shorter code or target code that consumes less power.

---

### 2.2.7 Target Code Generation
This phase takes as input a program in an intermediate representation (such as stack code, three-address code, or tree-structured representations) and translates it into machine code for the target machine. The code generator maps the intermediate instructions into sequences of machine instructions that perform the same tasks. During this process, registers or memory locations are selected for the variables used in the program.

---

### 2.2.8 Backpatching
In machine code generation, two main types of code generators can be distinguished: single-pass and multi-pass generators, which differ in the number of times they need to process the intermediate code to produce the final object code. During this process, one of the most important challenges is handling forward jumps, which occur when a reference to a label appears before the label is defined.

To address this, careful management of labels and their corresponding memory addresses is required. The most commonly used strategies are:
1. **Backpatching (Single-Pass)**: Uses a table to store instructions that reference labels not yet defined. Once all intermediate code is processed, the code generator revisits the table to resolve pending jumps.
2. **Multi-Pass Generators**: Divides the process into several stages. The first stage records label definitions, and the subsequent stages replace references to those labels with the correct memory addresses.

---

## 2.3 Context-Free Grammar
A context-free grammar is a formal system for defining a class of languages. It is a set of formal rules that describe how to construct valid strings in a language. These grammars are widely used in the creation of programming languages and in the syntactic analysis of compilers.

---

## 2.4 Automaton
An automaton is a mathematical model for a finite state machine, in which, given an input of symbols, it transitions through a series of states according to a transition function (which can be expressed as a table). This transition function specifies which state to move to based on the current state and the symbol read.

---

## 2.5 Deterministic Finite Automaton
A Deterministic Finite Automaton (DFA) is defined as a mathematical model consisting of a set of states, an initial state, an alphabet, a set of accepting states, and a transition function. It uses the transition function to determine the next state based on the input it receives. A DFA accepts a word if the final state reached by the DFA after reading the word is one of the accepting states.

---

## 2.6 Regular Expressions
A regular expression is a pattern that the regular expression engine attempts to match in input text. A pattern consists of one or more character literals, operators, or constructs.

---

## 2.7 Token
A token is a predefined sequence of characters that cannot be broken down further. It is like an abstract symbol that represents a unit. A token can have an optional attribute value.

Aquí tienes un resumen del desarrollo en formato Markdown:

# Development

## 3.1 Grammar
To develop our compiler, we implemented a grammar capable of generating all required structures, including blocks like the `main` function, conditional structures (`if`), and arithmetic operations (`+`, `-`, `*`, `/`). This grammar was designed to handle the syntax and semantics of variable declarations, expressions, and flow control.

### 3.1.1 Expanded Grammar

Program → TYPE MAIN LP RP LB StatementList RB
StatementList → Statement | Statement StatementList
Statement → VariableDeclaration EQUAL Expression SEMICOLON
           | VariableDeclaration SEMICOLON
           | IF LP BooleanExpression RP LB StatementList RB
VariableDeclaration → TYPE ID
Expression → Expression PLUS Factor
            | Expression MINUS Factor
            | Factor
Factor → Factor MULT Term
        | Factor DIV Term
        | Term
Term → LP Expression RP
     | CONSTANT
     | ID
BooleanExpression → Expression RELATION Expression

- **Terminals**: `TYPE`, `MAIN`, `IF`, `LP`, `RP`, `LB`, `RB`, `EQUAL`, `SEMICOLON`, `ID`, `CONSTANT`, `PLUS`, `MINUS`, `MULT`, `DIV`, `RELATION`.
- **Non-Terminals**: `Program`, `StatementList`, `Statement`, `VariableDeclaration`, `Expression`, `Factor`, `Term`, `BooleanExpression`.
- **Start Symbol**: `Program`.

---

## 3.2 Lexical Analysis
The lexical analyzer tokenizes the input source code using regular expressions. Each token is identified by a type and, if applicable, an associated value. This stage simplifies the analysis by breaking down the code into components such as keywords (`int`, `if`, `main`), operators (`+`, `-`, `*`, `/`), identifiers, and constants.

Example:
```
int main() {
    int num = 25;
    int count = 0;

    if (count == 0) {
        count = 3;
    }
}
```

**Tokens Generated**:
```
TYPE, MAIN, LP, RP, LB, TYPE, ID, EQUAL, CONSTANT, SEMICOLON, ...
```

---

## 3.3 Syntax Analysis
The syntax analyzer validates the structure of the token stream using the defined grammar. It generates a parse tree or Abstract Syntax Tree (AST) to represent the hierarchical structure of the code.

### Workflow:
- **Parsing Algorithm**: Implemented using PLY (`yacc.py`), which supports LALR(1) parsing.
- **Error Handling**: Reports syntax errors and attempts to recover by identifying invalid token sequences.

---

## 3.4 Semantic Analysis
Semantic analysis ensures the program's logical consistency and adherence to rules defined in the grammar. It validates:
1. Variable declarations before use.
2. Type compatibility in expressions and assignments.
3. Correct structure of conditional statements and loops.

### Semantic Rules:
- Variable types must match assigned values.
- Boolean expressions in conditions must evaluate to a boolean value.
- Arithmetic operations must involve compatible types.

Example:
```c
int num = 25; // Valid
int count = "hello"; // Invalid: type mismatch
```

---

## 3.5 Intermediate Code Generation
The compiler generates Three-Address Code (TAC) as an intermediate representation. This code is easier to optimize and translate into machine code.

Example of TAC for the statement `int c = 3 * b + a;`:
```
t1 = 3 * b
t2 = t1 + a
c = t2
```

---

## 3.6 Code Optimization
The intermediate code is optimized for performance and efficiency. Techniques include:
- **Constant Folding**: Precomputing constant expressions.
- **Dead Code Elimination**: Removing unreachable or unused code.
- **Strength Reduction**: Replacing expensive operations with cheaper alternatives.

Example:
```c
if (1 == 1) { count = 3; }
// Optimized to:
count = 3;
```

---

## 3.7 Target Code Generation
The final stage translates TAC into target code that can be executed on a specific architecture or runtime. In this project, Python bytecode is used as the target representation for simplicity.

Example of Python bytecode:
```python
LOAD_CONST 3
LOAD_NAME b
BINARY_MULTIPLY
LOAD_NAME a
BINARY_ADD
STORE_NAME c
```

For more information, download the full documentation [here]().
