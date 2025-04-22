#!/usr/bin/env python3
import sys
import re
import random
import hashlib

class CFGSteganography:
    def __init__(self, grammar_file):
        self.grammar = {}
        self.load_grammar(grammar_file)
        
    def load_grammar(self, grammar_file):
        """Load and parse the grammar file."""
        with open(grammar_file, 'r') as f:
            lines = f.readlines()
            
        current_symbol = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if '→' in line:
                parts = line.split('→')
                current_symbol = parts[0].strip()
                self.grammar[current_symbol] = []
                
                if len(parts) > 1:
                    options = parts[1].strip()
                    if '||' in options:
                        self.grammar[current_symbol] = [opt.strip() for opt in options.split('||')]
                    else:
                        self.grammar[current_symbol] = [options]
            elif current_symbol:
                # If this is a continuation of a previous rule
                self.grammar[current_symbol].append(line)
    
    def encode(self, binary_data):
        """Encode binary data using the context-free grammar."""
        # Start with the Start rule template
        if 'Start' not in self.grammar:
            print("Error: Grammar must have a 'Start' rule")
            sys.exit(1)
            
        # Get template from Start rule (either the first option or join all lines)
        if len(self.grammar['Start']) == 1 and '||' in self.grammar['Start'][0]:
            template = random.choice(self.grammar['Start'][0].split('||')).strip()
        else:
            template = "\n".join(self.grammar['Start'])
            
        # Track bits used
        bit_index = 0
        
        # Find all non-terminal symbols in the template
        non_terminals = set(key for key in self.grammar.keys() if key != 'Start')
        
        # Replace each non-terminal with a choice based on binary data
        for symbol in non_terminals:
            if symbol in template and len(self.grammar[symbol]) >= 2:
                # Get options for this symbol
                options = self.grammar[symbol]
                
                # Check if we have enough bits left
                if bit_index < len(binary_data):
                    # Get the next bit
                    bit = binary_data[bit_index]
                    bit_index += 1
                    
                    # Choose based on the bit
                    selected = options[int(bit)] if int(bit) < len(options) else options[0]
                else:
                    # If we've used all bits, choose randomly
                    selected = random.choice(options)
                    
                # Replace all occurrences of the symbol in the template
                template = template.replace(symbol, selected)
        
        return template
    
def str_to_binary(message, key):
    """Convert a message to binary using a key."""
    h = hashlib.sha256((message + key).encode()).hexdigest()
    binary = bin(int(h, 16))[2:]
    return binary.zfill(48)[:48]

def main():
    if len(sys.argv) < 4:
        print("Usage: python generator.py <grammar_file> <secret_message> <key>")
        return
        
    grammar_file = sys.argv[1]
    secret_message = sys.argv[2]
    key = sys.argv[3]
    
    binary_data = str_to_binary(secret_message, key)
    print(f"Binary representation of the secret ({len(binary_data)} bits): {binary_data}")
    
    steg = CFGSteganography(grammar_file)
    encoded_text = steg.encode(binary_data)
    
    print("Encoded text:")
    print(encoded_text)

if __name__ == "__main__":
    main()
