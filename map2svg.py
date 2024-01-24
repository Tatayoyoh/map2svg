import os
import yaml
import json 
import psycopg2
from drawsvg import Drawing, Rectangle, Lines
import typer
from typing_extensions import Annotated
from rich.progress import Progress

DEFAULT_OUTPUT_FILE = 'map.svg'
DEFAULT_OUTPUT_PATH = os.path.join(os.getcwd(), DEFAULT_OUTPUT_FILE)

def main(
    config_file: Annotated[str, typer.Argument(help="OSM .pbf file path")],
    output_path: Annotated[str, typer.Argument(help="SVG generation path file. Default:\n %s"%(DEFAULT_OUTPUT_PATH), rich_help_panel="Secondary Arguments")] = DEFAULT_OUTPUT_PATH):
    
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.getcwd(), output_path)
    
    try:
        with open(config_file,'r') as f:
            config = yaml.safe_load(f)
    except:
        print('Config file must be YAML format and readable')
    
    bbox = config['bbox']

    if 'xyRatio' in bbox:
        bbox['yLength'] = bbox['xLength'] / bbox['xyRatio'] / config['heightMult']

    if 'middle' in bbox and 'xLength' in bbox and 'yLength' in bbox:
        bbox['xMin'] = bbox['middle'][1]-bbox['xLength']/2
        bbox['yMin'] = bbox['middle'][0]-bbox['yLength']/2
        bbox['xMax'] = bbox['middle'][1]+bbox['xLength']/2
        bbox['yMax'] = bbox['middle'][0]+bbox['yLength']/2
    
    with Progress() as progress: # display progress bars
        global PROGRESS, TASK1, TASK2
        PROGRESS = progress
        
        TASK1 = progress.add_task("[blue]Querying...", total=len(config['requests']))
        results = dbRequests(config)
        
        TASK2 = progress.add_task("[green]Generating...", total=len(results))
        draw:Drawing = createSVG(config, results)
        draw.save_svg(output_path)
    
    print('SVG output : %s'%(output_path))
    

def dbRequests(config:dict):
    conn = psycopg2.connect(database="openmaptiles",
                        host="localhost",
                        user="openmaptiles",
                        password="openmaptiles",
                        port=5432)
    
    cursor = conn.cursor()

    bboxString = "%s, %s, %s, %s"%(config['bbox']['xMin'], config['bbox']['yMin'], config['bbox']['xMax'], config['bbox']['yMax'])
    
    results = []

    for request in config['requests'] :
        query = buildQueryString(bboxString, request)
        
        cursor.execute(query)
        res = cursor.fetchall()

        geometry = []
        for row in res:
            geometry.append(json.loads(row[0]))

        results.append({
            'geometry': geometry,
            'request': request
        })
        
        PROGRESS.update(TASK1, advance=1)
            
    return results

def buildQueryString(bboxString, request):
  queryArray = [
    'SELECT ST_AsGeoJSON(ST_Transform(geometry, 4326)) AS geometry FROM',
    request['table'],
    'WHERE geometry && ST_Transform(ST_MakeEnvelope(',
    bboxString,
    ', 4326), 3857)'
  ]

  if 'restrictions' in request and request['restrictions']:
    queryArray.append("AND (%s)"%(request.restrictions))

  return ' '.join(queryArray) + ";"

def createSVG(config, results):
    bbox = config['bbox']

    svgWidth = config['svgWidth']
    heightMult = config['heightMult']

    bboxWidth = bbox['xMax']-bbox['xMin']
    bboxHeight = (bbox['yMax']-bbox['yMin'])*heightMult
    scaleValue = svgWidth / bboxWidth

    svgHeight = bboxHeight * scaleValue

    draw = Drawing(svgWidth, svgHeight)
    draw.append(Rectangle(0, 0, svgWidth, svgHeight, fill=config["background-color"]))

    def convert_lines(lines):
        res = []
        newlines = list(map(lambda p: [(p[0]-bbox['xMin'])*scaleValue,(-p[1]+bbox['yMax'])*scaleValue*heightMult], lines))
        for l in newlines:
            res += l
        return res

    for result in results:
        for geo in result['geometry']:
            if geo['type'] == "LineString":
                res = convert_lines(geo['coordinates'])
                draw.append(
                    Lines(
                        *res, 
                        stroke=result['request']['stroke'], 
                        fill=result['request']['fill'], 
                        stroke_width=result['request']['stroke-width'],
                        stroke_linecap='round'
                    )
                )
            elif geo['type'] == "Polygon":
                for lines in geo['coordinates']:
                    res = convert_lines(lines)
                    draw.append(
                        Lines(
                            *res, 
                            stroke=result['request']['stroke'], 
                            fill=result['request']['fill'], 
                            stroke_width=result['request']['stroke-width'],
                            stroke_linecap='round'
                        )
                    )
            PROGRESS.update(TASK2, advance=1)
    
    return draw

if __name__ == '__main__':
    typer.run(main)