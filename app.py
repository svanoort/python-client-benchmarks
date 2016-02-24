#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()