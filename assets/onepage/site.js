// One-page homepage behaviour. Plain ES5 so the build's minifier accepts it.
(function () {
  "use strict";

  function each(list, fn) {
    Array.prototype.forEach.call(list, fn);
  }

  // Publication filter. Without JavaScript the full list stays visible.
  var bar = document.querySelector("[data-pub-filter]");
  var pubs = document.querySelectorAll("[data-pub]");
  var chips = bar ? bar.querySelectorAll("[data-filter]") : [];

  function applyFilter(tag) {
    each(pubs, function (el) {
      var tags = (el.getAttribute("data-tags") || "").split(" ");
      el.hidden = !(tag === "all" || tags.indexOf(tag) !== -1);
    });
    each(chips, function (chip) {
      chip.setAttribute("aria-pressed", chip.getAttribute("data-filter") === tag ? "true" : "false");
    });
  }

  if (bar && pubs.length) {
    bar.hidden = false;
    each(chips, function (chip) {
      chip.addEventListener("click", function () {
        applyFilter(chip.getAttribute("data-filter"));
      });
    });
    var target = location.hash && document.getElementById(location.hash.slice(1));
    applyFilter(target && target.hasAttribute("data-pub") && !/\bselected\b/.test(target.getAttribute("data-tags")) ? "all" : "selected");
  }

  // Links from the research cards: show every paper if the target is filtered out.
  each(document.querySelectorAll("[data-pub-link]"), function (link) {
    link.addEventListener("click", function () {
      var el = document.getElementById(link.getAttribute("href").slice(1));
      if (el && el.hidden) applyFilter("all");
    });
  });

  // BibTeX copy buttons.
  each(document.querySelectorAll("[data-copy]"), function (button) {
    button.addEventListener("click", function () {
      var code = button.parentNode.querySelector("code");
      if (!code) return;
      var done = function () {
        button.textContent = "Copied";
        setTimeout(function () { button.textContent = "Copy"; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code.textContent).then(done, function () {
          selectText(code);
        });
      } else {
        selectText(code);
      }
    });
  });

  function selectText(node) {
    var range = document.createRange();
    range.selectNodeContents(node);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  // Highlight the menu entry for the section in view.
  var navLinks = document.querySelectorAll('.nav a[href^="#"]');
  if ("IntersectionObserver" in window && navLinks.length) {
    var byId = {};
    each(navLinks, function (a) {
      byId[a.getAttribute("href").slice(1)] = a;
    });
    var observer = new IntersectionObserver(
      function (entries) {
        each(entries, function (entry) {
          if (!entry.isIntersecting) return;
          each(navLinks, function (a) { a.removeAttribute("aria-current"); });
          var link = byId[entry.target.id];
          if (link) link.setAttribute("aria-current", "true");
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    Object.keys(byId).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }
})();
