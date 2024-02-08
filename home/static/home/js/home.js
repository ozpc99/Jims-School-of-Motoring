/*
Scroller:
- Each line is animated (see home.css) which takes 5 seconds.
- Each line will pause for 4 out of those 5 seconds.
- Each line will scroll in and out for 1 of those 5 seconds. (0.5s for in and 0.5s for out).
*/
document.addEventListener("DOMContentLoaded", function() {
    const lines = document.querySelectorAll(".line");
    let index = 0;
  
    function displayLine() {
      lines.forEach(line => {
        line.classList.remove("scroll-in", "scroll-out");
      });
  
      lines[index].classList.add("scroll-in");
      setTimeout(() => {
        lines[index].classList.add("scroll-out");
        index = (index + 1) % lines.length;
      }, 4000); // 4 Second Pause before next line is displayed
  
      setTimeout(displayLine, 5000); // 5 Second Duration for each animation
    }
  
    displayLine();
  });
  