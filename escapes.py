"""
Generates a dictionary of ANSI escape codes

http://en.wikipedia.org/wiki/ANSI_escape_code

Uses colorama as an optional dependency to support color on Windows
"""

try:
    import colorama
except ImportError:
    pass
else:
    colorama.init()
    
# Returns escape codes from format codes
esc = lambda x: '\033[' + (';'.join(str(t) for t in x)) + 'm'

# The initial list of escape codes
escape_codes = {
    'reset': esc('0')
}

# The color names
FGs = ['k', 'r', 'g', 'y', 'b', 'p', 'c', 'w']

# The bg names
BGs = ['K', 'R', 'G', 'Y', 'B', 'P', 'C', 'W']

#Attributes
ATTRIBS = ['n', 'b', 'd', 'i', 'u']

for bgcode, bgname in enumerate(BGs):
    for fgcode, fgname in enumerate(FGs):
        for attrcode, attrname in enumerate(ATTRIBS):
            escape_codes[attrname + fgname + bgname] = esc([40 + bgcode, attrcode, 30 + fgcode])
