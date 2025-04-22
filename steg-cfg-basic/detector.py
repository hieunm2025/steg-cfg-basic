#!/usr/bin/env python3

import sys
import re
import hashlib

class StegDetector:
    def __init__(self, grammar_file):
        self.grammar = {}
        self.load_grammar(grammar_file)
        
    def load_grammar(self, grammar_file):
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
                self.grammar[current_symbol].append(line)
    
    def detect(self, text):
        pattern_matches = []
        
        for symbol, options in self.grammar.items():
            if len(options) >= 2 and symbol != 'Start':
                for i, option in enumerate(options):
                    pattern = r'\b' + re.escape(option) + r'\b'
                    if re.search(pattern, text, re.IGNORECASE):
                        if len(options) == 2:
                            pattern_matches.append((symbol, option, str(i)))
                        else:
                            binary = format(i, '02b')
                            pattern_matches.append((symbol, option, binary))
        
        binary = ''.join([match[2] for match in pattern_matches])
        
        if len(binary) >= 1:  # Giảm ngưỡng để phát hiện thông tin ẩn
            print(f"[+] Detected potential hidden bits: {binary}")
            print(f"[+] Detected {len(binary)} bits of hidden information")
            return True, binary
        return False, ""
    
    def try_decode(self, text, possible_keys):
        pattern_matches = []
        
        for symbol, options in self.grammar.items():
            if len(options) >= 2 and symbol != 'Start':
                for i, option in enumerate(options):
                    pattern = r'\b' + re.escape(option) + r'\b'
                    if re.search(pattern, text, re.IGNORECASE):
                        if len(options) == 2:
                            pattern_matches.append((symbol, option, str(i)))
                        else:
                            binary = format(i, '02b')
                            pattern_matches.append((symbol, option, binary))
        
        binary_data = ''.join([match[2] for match in pattern_matches])
        
        print(f"Extracted bits: {binary_data}")
        
        for key in possible_keys:
            possible_message = self.binary_to_message(binary_data, key)
            print(f"Using key '{key}': {possible_message}")
    
    def binary_to_message(self, binary, key):
        return f"Potential message with key '{key}'"

def main():
    if len(sys.argv) < 3:
        print("Usage: python detector.py <grammar_file> <text_file> [possible_keys]")
        return
        
    grammar_file = sys.argv[1]
    text_file = sys.argv[2]
    
    possible_keys = []
    if len(sys.argv) > 3:
        possible_keys = sys.argv[3].split(',')
    
    with open(text_file, 'r') as f:
        text = f.read()
    
    detector = StegDetector(grammar_file)
    detected, binary = detector.detect(text)
    if detected:
        print("\n[+] Hidden information detected!")
        
        if possible_keys:
            print("\nAttempting to decode with provided keys:")
            detector.try_decode(text, possible_keys)
        else:
            print("\nProvide possible keys to attempt decoding.")
    else:
        print("[-] No hidden information detected using the provided grammar")

if __name__ == "__main__":
    main()
