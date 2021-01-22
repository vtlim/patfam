
//JSON object with the data
var iconUS = "/static/images/icon_us.png";
var iconUN = "/static/images/icon_un.png";
var iconEU = "/static/images/icon_eu.png";
var iconJP = "/static/images/icon_jp.png";

var treeData = {"name" : "Root", "info" : "1", "img": iconUS,
    "children" : [
        {"name" : "A", "info" : "2", "img": iconUN },
        {"name" : "B", "info" : "3", "img": iconEU },
        {"name" : "C", "info" : "4", "img": iconJP, "children": [

                {"name" : "C1", "info" : "5", "img": iconUS },
                {"name" : "C2", "info" : "6 and I am a very long info", "img": iconEU }
            ]}
    ]};

// Define diagonal for edge lines
// VL update from https://stackoverflow.com/a/65819327
var diagonal = function link(d) {
  return "M" + d.source.x + "," + d.source.y
      + " " + d.source.x + "," + (d.source.y + d.target.y) / 2
      + " " + d.target.x + "," + (d.source.y + d.target.y) / 2
      + " " + d.target.x + "," + d.target.y;
};

// Define dimensions for svg canvas by size of browser window
// https://stackoverflow.com/q/16265123
var canvas = {
  //width: 600,
  //height: 400,
  width: window.screen.width / 2,
  height: window.screen.height / 1.5,
  marginw: window.screen.width / 10,
  marginh: window.screen.height / 7,
};

// Define properties for node rectangles
// rx and ry define corner curvature
var rectNode = {
  width : canvas.marginw/1.05,
  height : canvas.marginh/1.5,
  textMargin : 5,
  rx : 6,
  ry : 6,
};


// Define properties for icon size
var icon = {
  w: rectNode.height/1.4,
  h: rectNode.height/1.4,
};

// Create a svg canvas (order matters)
var vis = d3.select("#outdiv").append("svg:svg")
            //.attr("width", x/2)
            //.attr("height", y/3)
            .attr("viewBox", "0 0 " + canvas.width + " " + canvas.height)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .append("svg:g")
            .attr("transform", "translate(-10, 90)");

// Add tooltip div
var div = d3.select("body").append("div")
.attr("class", "tooltip")
.style("opacity", 1e-6);

//  // Add border around the svg canvas
//  var borderPath = vis.append("rect")
//  .attr("x", -10)
//  .attr("y", -90)
//  .attr("width", canvas.width)
//  .attr("height", canvas.height)
//  .attr("class", "canvas-border");

// Create a tree "canvas"
var treeMap = d3.tree()
//.size([500, 300]);
.size([canvas.width , canvas.height-2*canvas.marginh ]);

// Preparing the data for the tree layout, convert data into an array of nodes
// assigns the data to a hierarchy using parent-child relationships
// VL update from https://bl.ocks.org/d3noob/5259f38ebcf5659f39ef18d726d4ec21
var nodes = d3.hierarchy(treeData, function(d) {
    return d.children;
  });

// maps the node data to the tree layout
nodes = treeMap(nodes);

// Create an array with all the links
// VL update from https://stackoverflow.com/a/47298752
var links = treeMap(nodes).links();

console.log("Raw:")
console.log(treeData)
console.log("Nodes:")
console.log(nodes)
console.log("Links:" )
console.log(links)

// Show me a link in raw and its path version
console.log(links[0])
console.log(diagonal(links[0]))

var link = vis.selectAll("pathlink")
.data(links)
.enter().append("svg:path")
.attr("class", "link")
.attr("d", diagonal)

var node = vis.selectAll("g.node")
.data(nodes)
.enter().append("svg:g")
.attr("transform",
  function(d) {
    return "translate(" + (d.x-(rectNode.width/2)) + "," + (d.y-(rectNode.height/2)) + ")";
  }
)

// Add a rectangle at every node
node.append("rect")
.on("mouseover", mouseover)
.on("mousemove", function(event,d){mousemove(event,d);})
.on("mouseout", mouseout)
.attr("width", rectNode.width)
.attr("height", rectNode.height)
.attr('rx', rectNode.rx)
.attr('ry', rectNode.ry)
.attr("fill","red");

node.append("svg:text")
.on("mouseover", mouseover)
.on("mousemove", function(event,d){mousemove(event,d);})
.on("mouseout", mouseout)
.attr("dx", rectNode.width/3)
.attr("dy", rectNode.height/3)
.text(function(d) { return d.data.name; })

node.append("svg:image")
.attr("xlink:href", function(d) { return d.data.img; })
.attr("width", icon.w)
.attr("height", icon.h)
.attr('x', -20)
.attr('y', -40)

function mouseover() {
    div.transition()
    .duration(300)
    .style("opacity", 1);
}

function mousemove(event, d) {
    console.log(d);
    div
    .html("<b>Title: </b>" + d.data.info)
    .style("left", (event.pageX ) + "px")
    .style("top", (event.pageY - 15) + "px");
}

function mouseout() {
    div.transition()
    .duration(300)
    .style("opacity", 1e-6);
}
