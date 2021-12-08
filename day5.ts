const raw = await Deno.readTextFile("./data5.lst");

interface Point {
    type: "point";
    x: number;
    y: number;
}
function Point(x: number, y: number) : Point{
    const type = "point";
    return {type, x, y} as Point;
}

interface Line {
    type: "line";
    start: Point;
    finish: Point;
}

function Line(start: Point, finish: Point) : Line {
    const type = "line";
    return {type, start, finish} as Line;
}

function isLine(x: Line | null): x is Line {
    return x?.type == "line";
}

function between(x: number, left: number, right:number): boolean{
    return x >= Math.min(left, right) && x <= Math.max(left, right)
}

function isPointOn(p: Point, l: Line){
    // Only works for flat rectangles
    const slope = (l.finish.y - l.start.y)/(l.finish.x - l.start.x)
    const zero = l.start.y - slope * l.start.x
    
    const isHorizontal = p.x == l.start.x &&  p.x == l.finish.x
    const isVertical   = p.y == l.start.y &&  p.y == l.finish.y
    const isInScope = between(p.x, l.start.x, l.finish.x) && between(p.y, l.start.y, l.finish.y)
    const satisfySlope = slope * p.x + zero == p.y;

    return isInScope && (isHorizontal || isVertical || satisfySlope)

}

const lines = raw.split("\n")
                 .map(lraw => lraw.match(new RegExp('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')))
                 .map(coords => {
                     if(coords == null) return null;
                     const [_, x1, y1, x2, y2] = coords.map(s => parseInt(s))
                     return Line(Point(x1,y1), Point(x2, y2))
                 })
                 .filter(isLine)
                 
const width = Math.max(...lines.map(l => [l.start.x, l.finish.x]).flat()) + 1
const height = Math.max(...lines.map(l => [l.start.y, l.finish.y]).flat()) + 1

const straight = lines.filter(l => {
    return l.start.x == l.finish.x 
        || l.start.y == l.finish.y
})

// const work_on = straight
const work_on = lines;

const matrix = Array.from(Array(height), (_,y) => y)
                    .map( (y) => Array.from(Array(width), (_,x) => [x,y]))
                    .flat()
const res = matrix.map( ([x,y]) => work_on.filter( l => isPointOn(Point(x,y), l)).length )
      .filter( t => t >= 2)
      .length
console.log(res)
export {}