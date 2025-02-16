from flask import Flask, request, render_template
from rdflib import Graph, URIRef, Namespace

app = Flask(__name__)

g = Graph()
g.parse('mytourism.owl', format='xml')

ns = Namespace("http://www.my_ontology.edu/mytourism#")

@app.route('/', methods=['GET', 'POST'])
def search_province():
    results = []
    seen = set()
    lang = request.form.get('lang', request.args.get('lang', 'th'))
    if request.method == 'POST':
        query = request.form['query'].lower()
        for s, p, o in g:
            if isinstance(s, URIRef) and ns.ThaiProvince in g.objects(s, None):
                if query in str(s).lower() or query in str(o).lower():
                    for pred, obj in g.predicate_objects(s):
                        if pred != ns.type and pred != URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type") and str(obj) not in seen:
                            if not hasattr(obj, 'language') or obj.language == lang:
                                seen.add(str(obj))
                                results.append(f"{pred.split('#')[-1]} -> {obj}")
        if not results:
            results.append("ไม่พบข้อมูลที่ค้นหา" if lang == 'th' else "No data found")
    return render_template('index.html', results=results, lang=lang, current_lang=lang)

if __name__ == '__main__':
    app.run(debug=True)