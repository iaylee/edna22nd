(function () {
  var data = window.BIRTHDAY;
  var envelope = document.getElementById("envelope");
  var letter = document.getElementById("letter");
  var tab = document.getElementById("letter-tab");
  var hint = document.getElementById("hint");
  var panel = document.getElementById("panel");
  var panelTitle = document.getElementById("panel-title");
  var panelBody = document.getElementById("panel-body");
  var panelClose = document.getElementById("panel-close");

  var OPEN = 188;
  var THRESHOLD = 78;
  var titles = {
    encouragement: "Encouragement",
    jokes: "Dad jokes",
    memories: "Memory lane",
  };
  var lastIndex = { encouragement: -1, jokes: -1, memories: -1 };
  var drag = null;
  var justOpened = false;

  document.getElementById("letter-text").textContent = data.letter;

  function setHint(open) {
    hint.textContent = open ? "click the letter to put it back" : "drag the tab";
    tab.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function pullTo(px) {
    var flap = Math.max(0, Math.min(180, (px / OPEN) * 180));
    envelope.style.setProperty("--pull", px + "px");
    envelope.style.setProperty("--flap", flap + "deg");
  }

  function finishOpen() {
    envelope.classList.remove("dragging");
    envelope.classList.add("open");
    envelope.style.removeProperty("--pull");
    envelope.style.removeProperty("--flap");
    setHint(true);
    justOpened = true;
  }

  function finishClosed() {
    envelope.classList.remove("dragging", "open");
    envelope.style.removeProperty("--pull");
    envelope.style.removeProperty("--flap");
    setHint(false);
  }

  tab.addEventListener("pointerdown", function (event) {
    if (envelope.classList.contains("open")) return;
    drag = { id: event.pointerId, y: event.clientY, moved: false };
    envelope.classList.add("dragging");
    tab.setPointerCapture(event.pointerId);
  });

  tab.addEventListener("pointermove", function (event) {
    if (!drag || event.pointerId !== drag.id) return;
    var dy = Math.max(0, event.clientY - drag.y);
    if (dy > 4) drag.moved = true;
    pullTo(Math.min(OPEN, dy));
  });

  function endDrag(event) {
    if (!drag || event.pointerId !== drag.id) return;
    var dy = Math.max(0, event.clientY - drag.y);
    drag = null;
    if (dy >= THRESHOLD) finishOpen();
    else finishClosed();
  }

  tab.addEventListener("pointerup", endDrag);
  tab.addEventListener("pointercancel", endDrag);

  tab.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    if (envelope.classList.contains("open")) finishClosed();
    else finishOpen();
    justOpened = false;
  });

  tab.addEventListener("click", function (event) {
    event.preventDefault();
  });

  letter.addEventListener("click", function (event) {
    if (event.target.closest(".tab")) return;
    if (justOpened) {
      justOpened = false;
      return;
    }
    if (envelope.classList.contains("open")) finishClosed();
  });

  function button(label) {
    var el = document.createElement("button");
    el.type = "button";
    el.className = "pixel-btn";
    el.textContent = label;
    return el;
  }

  function listFor(kind) {
    if (kind === "encouragement") return data.verses;
    if (kind === "jokes") return data.jokes;
    return data.memories || [];
  }

  function pickIndex(kind) {
    var list = listFor(kind);
    var index = Math.floor(Math.random() * list.length);
    if (list.length > 1) {
      while (index === lastIndex[kind]) index = Math.floor(Math.random() * list.length);
    }
    lastIndex[kind] = index;
    return index;
  }

  function memoryCard(memory) {
    var figure = document.createElement("figure");
    figure.className = "viewer";
    if (memory.src && memory.type === "video") {
      var video = document.createElement("video");
      video.src = memory.src;
      video.controls = true;
      video.playsInline = true;
      figure.append(video);
    } else if (memory.src) {
      var img = document.createElement("img");
      img.src = memory.src;
      img.alt = memory.caption || "";
      figure.append(img);
    } else {
      var canvas = document.createElement("canvas");
      canvas.className = "memory-art";
      window.paintMemory(canvas, memory.scene || 0);
      figure.append(canvas);
    }
    if (memory.text) {
      var text = document.createElement("p");
      text.className = "quote";
      text.textContent = memory.text;
      figure.append(text);
    }
    if (memory.caption) {
      var caption = document.createElement("figcaption");
      caption.textContent = memory.caption;
      figure.append(caption);
    }
    return figure;
  }

  function renderPull(kind) {
    panelTitle.textContent = titles[kind];
    panelBody.replaceChildren();
    var list = listFor(kind);
    if (!list.length) {
      var empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = kind === "memories" ? "Add a memory" : "Nothing in this jar yet";
      panelBody.append(empty);
      return;
    }
    var item = list[pickIndex(kind)];
    if (kind === "memories") {
      panelBody.append(memoryCard(item));
    } else if (kind === "encouragement") {
      var quote = document.createElement("p");
      quote.className = "quote";
      quote.textContent = item.text;
      var cite = document.createElement("p");
      cite.className = "cite";
      cite.textContent = item.ref;
      panelBody.append(quote, cite);
    } else {
      var line = document.createElement("p");
      line.className = "quote";
      line.textContent = item;
      panelBody.append(line);
    }
    var next = button("pull another");
    next.addEventListener("click", function () {
      renderPull(kind);
    });
    panelBody.append(next);
  }

  document.querySelectorAll("[data-jar]").forEach(function (jar) {
    jar.addEventListener("click", function () {
      renderPull(jar.dataset.jar);
      if (!panel.open) panel.showModal();
    });
  });

  panelClose.addEventListener("click", function () {
    panel.close();
  });

  panel.addEventListener("click", function (event) {
    if (event.target === panel) panel.close();
  });
})();
