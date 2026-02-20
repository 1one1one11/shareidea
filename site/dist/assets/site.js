(function () {
  function slugify(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-");
  }

  function buildToc() {
    const content = document.getElementById("content");
    const toc = document.getElementById("toc");
    const toggle = document.getElementById("toc-toggle");
    if (!content || !toc) return;

    const headings = content.querySelectorAll("h2, h3");
    if (!headings.length) {
      toc.style.display = "none";
      if (toggle) toggle.style.display = "none";
      return;
    }

    const title = document.createElement("h2");
    title.textContent = "Contents";
    const list = document.createElement("ul");

    const used = new Set();
    headings.forEach((heading) => {
      const base = slugify(heading.textContent || "section") || "section";
      let id = base;
      let n = 1;
      while (used.has(id) || document.getElementById(id)) {
        id = `${base}-${n++}`;
      }
      used.add(id);
      heading.id = heading.id || id;

      const li = document.createElement("li");
      li.className = heading.tagName === "H3" ? "depth-3" : "depth-2";
      const a = document.createElement("a");
      a.href = `#${heading.id}`;
      a.textContent = heading.textContent || heading.id;
      li.appendChild(a);
      list.appendChild(li);
    });

    toc.innerHTML = "";
    toc.appendChild(title);
    toc.appendChild(list);

    const links = toc.querySelectorAll("a");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const target = toc.querySelector(`a[href=\"#${entry.target.id}\"]`);
          if (!target) return;
          if (entry.isIntersecting) {
            links.forEach((l) => l.classList.remove("active"));
            target.classList.add("active");
          }
        });
      },
      { rootMargin: "-35% 0px -55% 0px", threshold: [0, 1] }
    );

    headings.forEach((h) => observer.observe(h));

    if (toggle) {
      const collapseOnMobile = () => {
        if (window.matchMedia("(max-width: 960px)").matches) {
          toc.classList.add("is-collapsed");
          toggle.setAttribute("aria-expanded", "false");
        } else {
          toc.classList.remove("is-collapsed");
          toggle.setAttribute("aria-expanded", "true");
        }
      };

      collapseOnMobile();
      window.addEventListener("resize", collapseOnMobile);
      toggle.addEventListener("click", () => {
        const collapsed = toc.classList.toggle("is-collapsed");
        toggle.setAttribute("aria-expanded", String(!collapsed));
      });
    }
  }

  document.addEventListener("DOMContentLoaded", buildToc);
})();
