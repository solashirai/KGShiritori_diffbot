// var nodes = null;
// var edges = null;
var network = null;

function draw() {

  // Instantiate our network object.
  var container = document.getElementById("mynetwork");
  var data = {
    nodes: nodes,
    edges: edges,
  };
  var options = {
    nodes: {
      size: 40,
      borderWidth: 4,
      shape: "circularImage",
      scaling: {
        customScalingFunction: function (min, max, total, value) {
          return value / total;
        },
        min: 5,
        max: 150,
      },
      physics:{
        enabled: false
        // repulsion: {
        //   nodeDistance: 200
        // }
      },
      font: {
        size: 16
      }
    },
      edges: {
        arrows: {
          to: {
            enabled: true
          }
        },
        font: {
          size: 14 //px
        }
      }
  };
  network = new vis.Network(container, data, options);
}

window.addEventListener("load", () => {
  draw();
});
