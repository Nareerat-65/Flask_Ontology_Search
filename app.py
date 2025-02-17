from flask import Flask, request, render_template
from rdflib import Graph, URIRef, Namespace

app = Flask(__name__)

g = Graph()
g.parse('mytourism.owl', format='xml')

ns = Namespace("http://www.my_ontology.edu/mytourism#")

# เพิ่ม dictionary สำหรับแปลงชื่อ property
property_names = {
    'hasNameOfProvince': {'th': 'ชื่อจังหวัด', 'en': 'Province Name'},
    'hasTraditionalNameOfProvince': {'th': 'ชื่อดั้งเดิม', 'en': 'Traditional Name'},
    'hasMotto': {'th': 'คำขวัญ', 'en': 'Motto'},
    'hasTree': {'th': 'ต้นไม้ประจำจังหวัด', 'en': 'Provincial Tree'},
    'hasFlower': {'th': 'ดอกไม้ประจำจังหวัด', 'en': 'Provincial Flower'},
    'hasSeal': {'th': 'ตราประจำจังหวัด', 'en': 'Provincial Seal'},
    'hasLatitudeOfProvince': {'th': 'ละติจูด', 'en': 'Latitude'},
    'hasLongitudeOfProvince': {'th': 'ลองจิจูด', 'en': 'Longitude'},
    'hasImageOfProvince': {'th': 'รูปภาพ', 'en': 'Image'},
    'hasURLOfProvince': {'th': 'เว็บไซต์', 'en': 'Website'}
}

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
                                # แปลงชื่อ property ให้เป็นภาษาไทยหรืออังกฤษ
                                prop_name = pred.split('#')[-1]
                                display_name = property_names.get(prop_name, {}).get(lang, prop_name)
                                results.append(f"{display_name} -> {obj}")
        if not results:
            results.append("ไม่พบข้อมูลที่ค้นหา" if lang == 'th' else "No data found")
    return render_template('index.html', results=results, lang=lang, current_lang=lang)

if __name__ == '__main__':
    app.run(debug=True)