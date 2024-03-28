from flask import Flask, render_template, request
import ezdxf
import math

app = Flask(__name__)

def find_area_of_polygon(vertices):
    n = len(vertices)
    if n < 3:
        return 0  # Return 0 if there are not enough vertices to form a polygon
    area = 0
    for i in range(n):
        j = (i + 1) % n
        x_i, y_i = vertices[i]['start_point'].x, vertices[i]['start_point'].y  # Extract x, y coordinates from start_point
        x_j, y_j = vertices[j]['start_point'].x, vertices[j]['start_point'].y  # Extract x, y coordinates from end_point
        area += x_i * y_j
        area -= x_j * y_i
    area = abs(area) / 2.0
    return area

def find_perimeter_of_polygon(vertices):
    perimeter = 0
    for vertex in vertices:
        start_point = vertex['start_point']
        end_point = vertex['end_point']
        length = math.sqrt((end_point.x - start_point.x)**2 + (end_point.y - start_point.y)**2)
        perimeter += length
    return perimeter

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'static/uploads/{f.filename}')
        doc = ezdxf.readfile(f'static/uploads/{f.filename}')
        msp = doc.modelspace()
        layer_vertices = {}
        for e in msp:
            if e.dxftype() == "LINE":
                layer = e.dxf.layer
                start_point = e.dxf.start
                end_point = e.dxf.end
                if layer not in layer_vertices:
                    layer_vertices[layer] = {'vertices': [], 'lines': []}
                layer_vertices[layer]['vertices'].append({
                    'start_point': start_point,
                    'end_point': end_point
                })
                layer_vertices[layer]['lines'].append(f"Line starts from {start_point} ends on {end_point}")

        layer_info = []
        for layer, data in layer_vertices.items():
            vertices = data['vertices']
            lines = data['lines']
            print(vertices)
            area = find_area_of_polygon(vertices)
            perimeter = find_perimeter_of_polygon(vertices)
            layer_info.append({
                'layer': layer,
                'area': area,
                'perimeter': perimeter,
                'lines': lines
            })
        return render_template('result.html', layer_info=layer_info)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
