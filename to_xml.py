import xml.etree.cElementTree as ET

def write_xml(program, name):
    root = ET.Element("root")
    root.set("kind", "XML")
    
    write_node(program, root)
    
    tree = ET.ElementTree(root)
    
    tree.write(name + ".xml")
    
    


def write_node(node, parent):

    node_xml = ET.SubElement(parent, str(node['kind']))
    
    used_tokens = []
    for child in node['children']:
        used_tokens += write_node(child, node_xml)
        
    #get unique set of tokens
    tokens = node['tokens']
    
    #for t in tokens:
    #    print("==\t\t" + str(t))
        
        
    for t in used_tokens:
        if t == None:
            continue
        tokens.remove(t)
    
    for attrib in node:
        if attrib == "children" or attrib == "tokens":
            continue
            
        if attrib == "spelling" and node[attrib] == None:
            continue
        
        if attrib == "location" and node[attrib] == None:
            continue
            
        node_xml.set(attrib, str(node[attrib]))

    
    node_kind = str(node['kind'])
    #print(node_kind)
    
    tokens_to_use = []
    
    
    
    if "LITERAL" in node_kind:
        if node_kind == "CursorKind.CXX_BOOL_LITERAL_EXPR":
            #needs to find true/false
            #note that this is C++
            tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        else:
            tokens_to_use.append(remove_token_kind("TokenKind.LITERAL", tokens))
    
    elif node_kind == "CursorKind.DECL_REF_EXPR":
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
    elif node_kind == "CursorKind.BINARY_OPERATOR" or node_kind == "CursorKind.UNARY_OPERATOR":
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = ';'))
    
    elif node_kind == "CursorKind.DECL_STMT":
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '='))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';', required = False))
        
    elif node_kind == "CursorKind.VAR_DECL":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        
        #could be 'long long'
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens, required = False))
        
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = '*'))
        
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
    
        
    elif node_kind == "CursorKind.COMPOUND_ASSIGNMENT_OPERATOR":
        #examples: '/=', '+='
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';'))
        
        
    elif node_kind == "CursorKind.COMPOUND_STMT":
    
        
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '{'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '}'))
        
        
        while True:
            t = remove_token_kind("TokenKind.COMMENT", tokens, required = False)
            if t == None:
                break
            tokens_to_use.append(t)
        
    elif node_kind == "CursorKind.PAREN_EXPR":
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '('))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')'))
        
    elif node_kind == "CursorKind.IF_STMT":
    
        #remove 'if' and '(' and ')' but don't output to XML
        used_tokens.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'if'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '('))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')'))
        
        used_tokens.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'else', required = False))
        
    elif node_kind == "CursorKind.FOR_STMT":
        used_tokens.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'for'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '('))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';', required = False))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';', required = False))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')'))
        
    elif node_kind == "CursorKind.WHILE_STMT":
        used_tokens.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'while'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '('))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')'))
        
    elif node_kind == "CursorKind.CALL_EXPR":
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '('))
        
        #remove all commas from the call expression
        while True:
            t = remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ',', required = False)
            if t == None:
                break
            used_tokens.append(t)
            
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';', required = False))
        
    elif node_kind == "CursorKind.PARM_DECL":
    

        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
        #keep pointer and array info
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = '&'))
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = '*'))
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = '['))
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = ']'))
        
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, required = False, spelling = ','))
        
    elif node_kind == "CursorKind.BREAK_STMT":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'break'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';'))    
        
    elif node_kind == "CursorKind.RETURN_STMT":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens, spelling = 'return'))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ';'))
        
    elif node_kind == "CursorKind.FUNCTION_DECL":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
        #from params
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '(', required = False))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = ')', required = False))
        
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '{', required = False))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens, spelling = '}', required = False))
        
    #mark the token as consumed and output it to XML
    #keep ordering of tokens
    for t in tokens_to_use:
        if t == None:
            continue
        
        node_xml.set(t.kind, t.spelling)
        used_tokens.append(t)
        
    #for t in tokens:
    #    print("\t\t" + str(t))
    
    return used_tokens
    

def remove_token_kind(kind, tokens, reverse = False, required = True, spelling = None):
    if reverse:
        tokens = reversed(tokens)
    
    for t in tokens:
        #make sure kind matches, and potentially do a spelling check (for punctuation)
        if t.kind == kind and (spelling == None or t.spelling == spelling):
            tokens.remove(t)
            #print("\tFound: " + str(t))
            return t
            
    if required:
        raise ValueError('Kind: ' + kind + ' was not found in the token list. Spelling: ' + str(spelling))
    return None
        
        
