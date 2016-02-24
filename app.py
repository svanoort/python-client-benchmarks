#!/usr/bin/env python
from os import urandom
from flask import Flask
app = Flask(__name__)

response_cache = dict()

@app.route("/ping")
def hello():
    return "pong"

# Returns larger sample JSON from http://json.org/example.html to exercise performance with larger payloads
@app.route("/bigger")
def big_response():
	return '''{ 
    "glossary": { 
        "title": "example glossary", 
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}'''

@app.route("/length/<int:response_bytes>")
def fix_length_response(response_bytes):
    if response_bytes < 1:
        raise Exception("Forbidded response length: {0}".format(response_bytes))
    try:
        response = response_cache[response_bytes]
        return response
    except KeyError:
        response = urandom(response_bytes)
        response_cache[response_bytes] = response
        return response    

if __name__ == "__main__":
    app.run()