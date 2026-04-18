// Table of Contents Generation
(function() {
  const contentBody = document.querySelector('.content-body');
  const tocList = document.getElementById('toc-list');
  
  if (!contentBody || !tocList) return;
  
  const headings = contentBody.querySelectorAll('h2, h3, h4');
  const toc = [];
  
  headings.forEach((heading, index) => {
    // Generate ID if not present
    if (!heading.id) {
      heading.id = `heading-${index}`;
    }
    
    const level = parseInt(heading.tagName[1]);
    const entry = {
      level: level,
      text: heading.textContent,
      id: heading.id
    };
    toc.push(entry);
  });
  
  // Build TOC list
  toc.forEach(entry => {
    const li = document.createElement('li');
    li.style.marginLeft = `${(entry.level - 2) * 1.5}rem`;
    
    const a = document.createElement('a');
    a.href = `#${entry.id}`;
    a.textContent = entry.text;
    
    li.appendChild(a);
    tocList.appendChild(li);
  });
  
  // Add smooth scroll behavior
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
})();
