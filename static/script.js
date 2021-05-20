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
const hamburger = document.getElementsByClassName('hamburger')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

hamburger.addEventListener('click', () => {
    navbarLinks.classList.toggle('active')
})

//KD3