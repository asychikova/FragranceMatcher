from flask import Flask, render_template, request
import csv
import os
app = Flask(__name__)

app = Flask(__name__, static_url_path='/')

def load_perfumes():
    perfumes = []
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            perfumes.append(row)
    return perfumes

@app.route('/', methods=['GET', 'POST'])
def home():
    perfumes = load_perfumes()
    attributes = {
        'Top Notes': [ 'Orange', 'Lotus', 'Juniper Berries', 'Apple', 'Bergamot', 'Pineapple', 'Spices', 'Mint', 'Peach', 'Neroli', 'Coconut', 'Sour Cherry' ],
        'Base Notes': ['Tobacco', 'Amber', 'Patchouli', 'Musk', 'Lily-of-the-Valley', 'Sandalwood', 'Vanilla', 'Woody Notes', 'Oakmoss', 'Leather', 'Coconut' , 'Vetiver'],
        'Middle Notes': ['Jasmine', 'Rose', 'Amber', 'Musk', 'Lily-of-the-Valley', 'Leather', 'Peach', 'Magnolia', 'Vanilla', 'Lotus', 'Raspberry' , 'Ylang-Ylang']
        
    }
    
    if request.method == 'POST':
        selected_attributes = request.form.getlist('attribute')
        selected_gender = request.form.getlist('gender')
        matched_perfumes = []
        for perfume in perfumes:
            top_notes = perfume['top'].split(',')
            base_notes = perfume['base'].split(',')
            middle_notes = perfume['middle'].split(',')
            if all(attr.strip() in top_notes or attr.strip() in base_notes or attr.strip() in middle_notes for attr in selected_attributes):
                matched_perfumes.append(perfume)


            if selected_gender:
                 matched_perfumes = [perfume for perfume in matched_perfumes if perfume['gender'] in selected_gender]

        return render_template('results.html', perfumes=matched_perfumes)

    return render_template('home.html', attributes=attributes)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


'''if __name__ == '__main__':
    app.run(debug=True)'''
