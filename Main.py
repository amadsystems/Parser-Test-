# A very basic arithmetic expression parser, evaluating expression directly.

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Here we create Lexer that reads raw text & converts it into tokens.


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token("NUMBER", self.integer())

            if self.current_char == '+':
                self.advance()
                return Token("PLUS", '+')

            if self.current_char == '-':
                self.advance()
                return Token("MINUS", '-')

            if self.current_char == '*':
                self.advance()
                return Token("MUL", '*')

            if self.current_char == '/':
                self.advance()
                return Token("DIV", '/')

            if self.current_char == '(':
                self.advance()
                return Token("LPAREN", '(')

            if self.current_char == ')':
                self.advance()
                return Token("RPAREN", ')')

            raise Exception(f"Invalid Character: {self.current_char}")
        return Token("EOF", None)

    def tokenize_all(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == "EOF":
                break
        return tokens

# Paser Evaluator


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"Syntax Error: expected {token_type}, got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return token.value
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            result = self.expr()
            self.eat("RPAREN")
            return result

        else:
            raise Exception(f"Syntax error in factor near {token}")

    def term(self):
        result = self.factor()

        while self.current_token.type in ("MUL", "DIV"):
            token = self.current_token

            if token.type == "MUL":
                self.eat("MUL")
                result = result * self.factor()

            elif token.type == "DIV":
                self.eat("DIV")
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("Math error: division by zero")
                result = result / divisor
        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token

            if token.type == "PLUS":
                self.eat("PLUS")
                result = result + self.term()

            elif token.type == "MINUS":
                self.eat("MINUS")
                result = result - self.term()

        return result

    def parse(self):
        result = self.expr()
        if self.current_token.type != "EOF":
            raise Exception(
                f"Unexpected token after expression: {self.current_token}")
        return result

# Main Program


def main():
    print("Basic Parser Demo")
    print("Supports integers, +, -, *, /, and parentheses")
    print("Type 'exit' to stop. \n")

    while True:
        text = input("Enter expression; ")

        if text.lower() == "exit":
            print("Thank You!.")
            break

        try:
            lexer_for_display = Lexer(text)
            tokens = lexer_for_display.tokenize_all()
            print("Tokens", tokens)

            lexer_for_parse = Lexer(text)
            parser = Parser(lexer_for_parse)
            result = parser.parse()

            print("Result:", result)
            print()

        except Exception as e:
            print("Error", e)
            print()


if __name__ == "__main__":
    main()
