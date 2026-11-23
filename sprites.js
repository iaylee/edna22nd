(function () {
  var palette = {
    o: "#5A4574",
    c: "#F4E4D4",
    p: "#F3B6C8",
    w: "#FFFDF8",
    k: "#3A2E4A",
    n: "#E48AA4",
    l: "#C9B4E8",
    d: "#8E74B8",
    b: "#8B5A3C",
    t: "#C4895A",
    m: "#FFF6EA",
    s: "#A86B42",
    h: "#E7D8F8",
    ".": "",
  };

  var rabbit = [
    "......oooo........",
    ".....oppppo.......",
    "....oppppppo......",
    "....oppppppo......",
    ".....oppppo.......",
    "......oooo........",
    "....ooccccoo......",
    "...occcccccco.....",
    "...ocwkkcwkkco....",
    "...ocwkkcwkkco....",
    "...occcccccco.....",
    "...occcnnccco.....",
    "...ocppccppco.....",
    "....occcccco......",
    ".....olddlo.......",
    "......oooo........",
    "....ooccccoo......",
    "...occcccccco.....",
    "...occcccccco.....",
    "....ocoooooco.....",
    "....oo....oo......",
  ];

  var beagle = [
    ".....ooooooo......",
    "....obbbbbbbo.....",
    "...obbbbbbbbbo....",
    "...obwwbbwwbbo....",
    "...obkkbbkkbbo....",
    "...obbbbbbbbbo....",
    "....obbnnbbbo.....",
    ".....obbbbo.......",
    "......ooooo.......",
    "...oottttttto.....",
    "..otmmmmmmmmto....",
    "..otmmmmmmmmto....",
    "..otsmmmmmmmto....",
    "...oottttttoo.....",
    "....oolllloo......",
    ".....otttto.......",
    ".....oo..oo.......",
    "....oo....oo......",
  ];

  var icons = {
    heart: [
      ".pp..pp.",
      "ppp..ppp",
      "pppppppp",
      ".pppppp.",
      "..pppp..",
      "...pp...",
    ],
    star: [
      "...t...",
      "..ttt..",
      "ttttttt",
      ".ttttt.",
      "..t.t..",
      ".t...t.",
    ],
    frame: [
      "oooooooo",
      "ohhhhhho",
      "ohhkkhho",
      "ohhhhhho",
      "ohhkkhho",
      "oooooooo",
    ],
  };

  function paint(canvas, rows, scale) {
    if (!canvas) return;
    var height = rows.length;
    var width = rows[0].length;
    canvas.width = width * scale;
    canvas.height = height * scale;
    var ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    rows.forEach(function (row, y) {
      for (var x = 0; x < row.length; x++) {
        var color = palette[row[x]];
        if (!color) continue;
        ctx.fillStyle = color;
        ctx.fillRect(x * scale, y * scale, scale, scale);
      }
    });
  }

  paint(document.getElementById("sprite-rabbit"), rabbit, 4);
  paint(document.getElementById("sprite-beagle"), beagle, 4);
  document.querySelectorAll("[data-icon]").forEach(function (canvas) {
    paint(canvas, icons[canvas.dataset.icon], 4);
  });

  window.paintMemory = function (canvas, scene) {
    var scale = 6;
    var width = 46;
    var height = 30;
    var n = Math.abs(scene | 0);
    canvas.width = width * scale;
    canvas.height = height * scale;
    var ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    var skies = ["#f4ecfc", "#efe4fb", "#f7f1fc", "#e9dcf8", "#f8eefc"];
    var grounds = ["#c9b4e8", "#b79ad6", "#d4c2f0", "#c3a6e4"];
    var sky = skies[n % skies.length];
    var ground = grounds[n % grounds.length];

    function px(x, y, color, w, h) {
      ctx.fillStyle = color;
      ctx.fillRect(x * scale, y * scale, (w || 1) * scale, (h || 1) * scale);
    }

    px(0, 0, sky, width, height);
    px(0, 21, ground, width, 9);
    px(4 + (n % 7), 4, n % 2 ? "#fff8ee" : "#f3b6c8", 4, 4);

    var motif = n % 8;
    var x = 16 + (n % 5);
    if (motif === 0) {
      px(x + 1, 14, "#7d9a62", 1, 7);
      px(x, 12, "#f3b6c8", 3, 3);
      px(x + 1, 13, "#fff8ee", 1, 1);
    } else if (motif === 1) {
      px(x, 12, "#fff8ee", 8, 7);
      px(x + 1, 8, "#8e74b8", 6, 4);
      px(x + 3, 15, "#5a4574", 2, 4);
    } else if (motif === 2) {
      px(x + 2, 10, "#6b8f71", 2, 11);
      px(x, 12, "#8fb58a", 6, 3);
      px(x + 1, 9, "#8fb58a", 4, 3);
    } else if (motif === 3) {
      px(x, 14, "#fff8ee", 9, 6);
      px(x, 14, "#c9b4e8", 9, 1);
      px(x + 3, 16, "#f3b6c8", 1, 1);
    } else if (motif === 4) {
      px(x, 16, "#d7c4a2", 12, 2);
      px(8, 18, "#d7c4a2", 8, 2);
      px(20, 19, "#d7c4a2", 10, 2);
    } else if (motif === 5) {
      px(x + 2, 11, "#e7d8f8", 5, 6);
      px(x + 1, 12, "#f7f1fc", 7, 4);
      px(x + 4, 17, "#b79ad6", 1, 3);
    } else if (motif === 6) {
      px(x, 13, "#f3b6c8", 2, 2);
      px(x + 3, 13, "#f3b6c8", 2, 2);
      px(x + 1, 15, "#f3b6c8", 3, 2);
      px(x + 2, 17, "#f3b6c8", 1, 2);
    } else {
      px(6, 8, "#fff8ee", 1, 1);
      px(14, 6, "#fff8ee", 1, 1);
      px(28, 9, "#fff8ee", 1, 1);
      px(36, 5, "#fff8ee", 1, 1);
      px(22, 11, "#fff8ee", 1, 1);
    }
  };
})();
