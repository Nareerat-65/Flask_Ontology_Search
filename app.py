from flask import Flask, render_template, request, jsonify
from rdflib import Graph, URIRef

app = Flask(__name__)

g = Graph()
g.parse("mytourism.owl", format="xml")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = []

    for s, p, o in g:
        subject = str(s).lower()
        obj = str(o).lower()

        if query in subject or query in obj:
            # หากเจอชื่อจังหวัดหรือคำที่ตรง ให้ดึงข้อมูลทั้งหมดของ NamedIndividual นั้น
            for sub, pred, obj_ in g.triples((s, None, None)):
                results.append({
                    "predicate": str(pred),
                    "object": str(obj_)
                })
            break

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
