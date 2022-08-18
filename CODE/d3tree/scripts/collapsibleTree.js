const margin = { top: 20, right: 120, bottom: 20, left: 120 },
  width = 960 - margin.right - margin.left,
  height = 800 - margin.top - margin.bottom

var i = 0,
  duration = 750,
  root
var tree = d3.layout.tree().size([height, width])
var diagonal = d3.svg.diagonal().projection(function (d) {
  return [d.y, d.x]
})
var svg = d3
  .select('body')
  .append('svg')
  .attr('width', width + margin.right + margin.left)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
var nodes, links

const backendUrl = 'http://127.0.0.1:5000'
const depthLimit = 3
var queryMode = 'movie'

d3.json('./data/default_root.json', function (error, rootNode) {
  if (error) throw error
  loadRoot(rootNode)
  updateTree(root)
})
d3.select(self.frameElement).style('height', '800px')

function loadRoot(newRoot) {
  root = newRoot
  root.x0 = height / 2
  root.y0 = 0
  root.children.forEach(collapseRecursive)
}

function collapseRecursive(d) {
  if (d.children) {
    d._children = d.children
    d._children.forEach(collapseRecursive)
    d.children = null
  }
}

function filterChildren(children) {
  var existingEntries, existingIDs
  if (children.length == 0) return children
  if (children[0].type === 'movie') {
    existingEntries = nodes.filter((n) => n.type === 'movie')
  } else if (children[0].type === 'music') {
    existingEntries = nodes.filter((n) => n.type === 'music')
  } else {
    console.error(`Error: collapsibleTree: filterChildren:
    cannot recognize children type: ${children[0].type}`)
    return children
  }
  existingIDs = existingEntries.map((e) => e.movie_id)
  return children.filter((c) => !existingIDs.includes(c.movie_id))
}

function updateTree(source) {
  // Compute the new tree layout.
  nodes = tree.nodes(root).reverse()
  links = tree.links(nodes)

  // Normalize for fixed-depth.
  nodes.forEach(function (d) {
    d.y = d.depth * 180
    // if (d == root)
    //   d.y = 0;
    // else if (root.children.map(c => c.movie_id).includes(d.movie_id))
    //   d.y = 50
    // else {
    //   console.log(d.parent.y)
    //   d.y = d.depth *  - 120;
    // }
  })

  // Update the nodes…
  var node = svg.selectAll('g.node').data(nodes, function (d) {
    return d.id || (d.id = ++i)
  })

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', function (d) {
      return 'translate(' + source.y0 + ',' + source.x0 + ')'
    })
    .on('click', click)

  // Add circle + text on nodes
  nodeEnter.append('circle').attr('r', 1e-6)
  // .style('fill', function (d) {
  //   // return d._children ? 'lightsteelblue' : '#fff'
  //   return 'red'
  // })
  nodeEnter
    .append('text')
    .attr('x', function (d) {
      return d.children || d._children ? -10 : 10
    })
    .attr('dy', '.35em')
    .attr('text-anchor', function (d) {
      return d.children || d._children ? 'end' : 'start'
    })
    .text(function (d) {
      return d.name
    })
    .style('fill-opacity', 1e-6)

  // Transition nodes to their new position.
  var nodeUpdate = node
    .transition()
    .duration(duration)
    .attr('transform', function (d) {
      return 'translate(' + d.y + ',' + d.x + ')'
    })

  // Add circle + text to new nodes
  nodeUpdate
    .select('circle')
    .attr('r', 4.5)
    .style('fill', (d) => (d._children ? 'lightsteelblue' : '#fff'))
    .style('stroke', (d) => (d.type == 'movie' ? 'steelblue' : 'orange'))
  nodeUpdate.select('text').style('fill-opacity', 1)

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node
    .exit()
    .transition()
    .duration(duration)
    .attr('transform', function (d) {
      return 'translate(' + source.y + ',' + source.x + ')'
    })
    .remove()

  nodeExit.select('circle').attr('r', 1e-6)
  nodeExit.select('text').style('fill-opacity', 1e-6)

  // Update the links…
  var link = svg.selectAll('path.link').data(links, function (d) {
    return d.target.id
  })

  // Enter any new links at the parent's previous position.
  link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link')
    .attr('d', function (d) {
      var o = { x: source.x0, y: source.y0 }
      return diagonal({ source: o, target: o })
    })

  // Transition links to their new position.
  link.transition().duration(duration).attr('d', diagonal)

  // Transition exiting nodes to the parent's new position.
  link
    .exit()
    .transition()
    .duration(duration)
    .attr('d', function (d) {
      var o = { x: source.x, y: source.y }
      return diagonal({ source: o, target: o })
    })
    .remove()

  // Stash the old positions for transition.
  nodes.forEach(function (d) {
    d.x0 = d.x
    d.y0 = d.y
  })
}

// Toggle children on click.
function click(d) {
  // Collapse tree node
  if (d.children) {
    d._children = d.children
    d.children = null
  }
  // Expand tree node
  else {
    if (d.depth >= 3) {
      alert('We now support <=3 layers recommendations')
      return
    }
    if (d._children == null) {
      if (d.type === 'music') {
        alert(
          'Cannot expand tree, recommendations from music tracks' +
            'to movies are not available for now.'
        )
        return
      }
      const queryUrl = `${backendUrl}/${queryMode}/${d.name}`
      fetch(queryUrl)
        .then((data) => data.json())
        .then((response) => {
          filteredChildren = filterChildren(response.children)
          d.children = filteredChildren.map((c) => tree.nodes(c).reverse()[0])
          updateTree(d)
        })
        .catch((e) => {
          console.error('ERROR: d3tree: http request error while expanding:', e)
        })
    } else {
      d.children = d._children
      d._children = null
    }
  }
  updateTree(d)
}

window.addEventListener(
  'message',
  (event) => {
    if (typeof event.data != 'object') {
      console.error(`Error: collapsibleTree: postMessage() did not 
    pass a valid event.data object, event.data: ${event.data}`)
    } else if (event.data.call == 'reloadD3Tree') {
      const queryUrl = `${backendUrl}/${queryMode}/${event.data.value.searchContent}`
      fetch(queryUrl)
        .then((data) => data.json())
        .then((response) => {
          response.name = response.movie_name
          response.type = 'movie'
          loadRoot(response)
          updateTree(root)
        })
        .catch((e) => {
          console.error(
            'ERROR: d3tree: http request error while loading root:',
            e
          )
        })
    } else if (event.data.call == 'toggleD3QueryMode') {
      queryMode = event.data.value.queryMode
      console.log(`collapsibleTree: queryMode changed to '${queryMode}'`)
    }
  },
  false
)
