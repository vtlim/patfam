
//JSON object with the data
var iconUS = "/static/images/icon_us.png";
var iconUN = "/static/images/icon_un.png";
var iconEU = "/static/images/icon_eu.png";
var iconJP = "/static/images/icon_jp.png";

var treeData = {"appNo":"123456789", "pubNo":"abcdefgh", "title":"Do the best you can until you know better. Then when you know better, do better.", "img":iconUS, "children" : [
    {"appNo":"234567891", "pubNo":"bcdefghi", "title":"Your level of success will seldom exceed your level of personal development.", "img":iconUN },
    {"appNo":"345678912", "pubNo":"cdefghij", "title":"The most courageous decision that you can make each day is to be in a good mood.", "img":iconEU },
    {"appNo":"456789123", "pubNo":"defghjik", "title":"Anger has a honey tip, but a poison source.", "img":iconJP, "children": [
        {"appNo" : "567891234", "pubNo" : "efghijkl", "title" : "Success hinges less on getting everything right than on how you handle getting things wrong.", "img": iconUS },
        {"appNo" : "678912345", "pubNo" : "fghijklm", "title" : "We don’t see things as they are; we see them as we are.", "img": iconEU }
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
// marginh defines space bt tree and canvas edge
// https://stackoverflow.com/q/16265123
var canvas = {
  //width: 600,
  //height: 400,
  width: window.screen.width / 1.3,
  height: window.screen.height / 1.1,
  marginh: window.screen.height / 6,
};

// Define properties for node rectangles
// rx and ry define corner curvature
var rectnode = {
  width : window.screen.width / 6.5,
  height : window.screen.height / 6.5,
  textMargin : 5,
  rx : 6,
  ry : 6,
};


// Define properties for icon size
var icon = {
  w: rectnode.height/1.7,
  h: rectnode.height/1.7,
};

// Create a svg canvas (order matters)
var vis = d3.select("#outdiv").append("svg:svg")
            //.attr("width", x/2)
            //.attr("height", y/3)
            .attr("viewBox", "0 0 " + canvas.width + " " + canvas.height)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .append("svg:g")
            .attr("transform", "translate(-120, 130)");

//  // Add border around the svg canvas
//  var borderPath = vis.append("rect")
//  .attr("width", canvas.width)
//  .attr("height", canvas.height)
//  .attr("class", "canvas-border");

// Create a tree "canvas"
var treeMap = d3.tree()
//.size([500, 300]);
.size([ canvas.width+canvas.marginh , canvas.height-2*canvas.marginh ]);

// Add tooltip div
var tdiv = d3.select("body").append("div")
.attr("class", "tooltip")
.style("opacity", 1e-6);

// Define filter for black drop shadow
// https://stackoverflow.com/a/26964445
var defs = vis.append("defs");

var filter = defs.append("filter")
    .attr("id", "drop-shadow")
filter.append("feGaussianBlur")
    .attr("in", "SourceAlpha")
    .attr("stdDeviation", 2)
    .attr("result", "blur");
filter.append("feOffset")
    .attr("in", "blur")
    .attr("dx", 4)
    .attr("dy", 4)
    .attr("result", "offsetBlur");
filter.append("feFlood")
    .attr("in", "offsetBlur")
    .attr("flood-color", "#3d3d3d")
    .attr("flood-opacity", "0.5")
    .attr("result", "offsetColor");
filter.append("feComposite")
    .attr("in", "offsetColor")
    .attr("in2", "offsetBlur")
    .attr("operator", "in")
    .attr("result", "offsetBlur");

var feMerge = filter.append("feMerge");
feMerge.append("feMergeNode")
    .attr("in", "offsetBlur")
feMerge.append("feMergeNode")
    .attr("in", "SourceGraphic");

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
    return "translate(" + (d.x-(rectnode.width/2)) + "," + (d.y-(rectnode.height/2)) + ")";
  }
)

// Add a rectangle at every node
node.append("rect")
    .on("mouseover", mouseover)
    .on("mousemove", function(event,d){mousemove(event,d);})
    .on("mouseout", mouseout)
    .attr("class", "rectnode")
    .attr("width", rectnode.width)
    .attr("height", rectnode.height)
    .attr('rx', rectnode.rx)
    .attr('ry', rectnode.ry)
    .style("filter", "url(#drop-shadow)");

// Add text in two parts since new lines are hard in svg
var textnode = node.append("svg:text")
    .on("mouseover", mouseover)
    .on("mousemove", function(event,d){mousemove(event,d);})
    .on("mouseout", mouseout)
    .style("fill", "white")
    .style("font-size", "28px")
textnode.append("tspan")
    .text(d => "App: " + d.data.appNo)
    .attr("x", rectnode.width/8) // use 0 for left edge of rectangles
    .attr("dy", rectnode.height/2.6)
textnode.append("tspan")
    .text(d => "Pub: " + d.data.pubNo)
    .attr("x", rectnode.width/8) // use 0 for left edge of rectangles
    .attr("dy", rectnode.height/3)

node.append("svg:image")
    .attr("xlink:href", function(d) { return d.data.img; })
    .attr("width", icon.w)
    .attr("height", icon.h)
    .attr('x', -20)
    .attr('y', -50);

// tooltip fade-in
function mouseover() {
    tdiv.transition()
    .duration(300)
    .style("opacity", 1);
}

function mousemove(event, d) {
    tdiv
    //.html("<b>Title: </b>" + d.data.title)
    .html(d.data.title)
    .style("left", (event.pageX + 8) + "px")
    .style("top", (event.pageY + 12) + "px");
}

//tooltip fade-out
function mouseout() {
    tdiv.transition()
    .duration(300)
    .style("opacity", 1e-6);
}
