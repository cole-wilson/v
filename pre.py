import re
import glob
from collections import defaultdict

WIDTH = 5
WIDTHS = {"spc": 5}
setup = open('setup.kbd').read()
userbase = open('base.txt').read()
acount = 0
base = [i.split() for i in userbase.split("\n")]

def layer_to_str(name, layer, transparent):
	o = f"(deflayer {name}\n"
	for row in base:
		o += "\t"
		for basechar in row:
			w = WIDTH
			func = str.ljust
			if basechar == "spc":
				w *= 5
				func = str.center
			char = "_" if basechar in transparent else "XX"
			if basechar in layer:
				char = layer[basechar]
			o += func(char, w)
		o += "\n"
	o += ")\n"
	print(o)

def parsemapping(layername, mapping):
    global acount
    layers = defaultdict(dict)
    aliases = {}
    top, mapping = mapping.split("\n---\n", 1)
    transparent = set(map(str.strip, top.split()))

    for line in mapping.split('\n'):
        if " " not in line: continue
        combokey, value = line.split(" ", 1)
        combokey = combokey.lower().replace("cmd", "lmet").replace("shift", "lsft")
        lastkey = ""
        delim = "+"
        splits = re.split(r"([\+\,\-])", combokey)
        for count, item in enumerate(splits):
            if item in "+,-": continue
            delim = splits[count + 1] if count + 1 < len(splits) else ""
            button = f"(layer-next {layername + lastkey + '_' + item})"
            if delim in "+-":
                button = f"(layer-toggle {layername + lastkey + '_' + item})"
            if count + 1 == len(splits):
                button = value
            alias = "" + str(acount)
            acount += 1
            layers[layername + lastkey][item] = "@" + alias
            aliases[alias] = button
            lastkey += "_" + item
    for k, v in layers.items():
        layer_to_str(k, v, transparent)
    for k, v in aliases.items():
        print(f"(defalias {k} {v})")

print(setup + "\n")
print(f"(defsrc\n{userbase}\n)")
for filename in glob.glob("*.map"):
    parsemapping(filename.rstrip('.map'), open(filename).read())
