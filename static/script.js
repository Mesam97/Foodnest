// Väntar på att sidan ska bli redo för att köra vårt JavaScript
$(document).ready(function() {
	$("#changePassword").on("click", function() {
        // Frågar användaren efter det gamla och det nya lösenordet
		var old_password = prompt("Ange ditt gamla lösenord");
        var new_password = prompt("Ange ditt nya lösenord");
        // Ändrar lösenordet
console.log("hej")
    $("#delete").on("click", function() {
        // Frågar användaren efter vilket inlägg som ska bort
        var remove = prompt("Ange titeln på det inlägg som du vill ta bort");
        // tar bort det valda inlägget
    })
})
});

// LIKE-function 
$('.bi').click(function(){
    if ($('.bi').hasClass('bi bi-suit-heart')){
      $('.bi').removeClass('bi bi-suit-heart').addClass('bi bi-suit-heart-fill')
    }                 

    else {
      $('.bi').removeClass('bi bi-suit-heart-fill').addClass('bi bi-suit-heart')
      }
  })

;

// Navbar
function navSlide() {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  const navLinks = document.querySelectorAll(".nav-links li");
  
  burger.addEventListener("click", () => {
      //Toggle Nav
      nav.classList.toggle("nav-active");
      
      //Animate Links
      navLinks.forEach((link, index) => {
          if (link.style.animation) {
              link.style.animation = ""
          } else {
              link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
          }
      });
      //Burger Animation
      burger.classList.toggle("toggle");
  });
  
}

navSlide();

//KD3