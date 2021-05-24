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
  console.log($('.bi').hasClass('bi bi-suit-heart'))
    if ($('.bi').hasClass('bi-suit-heart')){
      window.location.href=('?liked=1')
    }                 

    else {
      window.location.href=('?liked=0')
      }
  })

let liked = $('.bi').attr('liked')
  
    if (liked==1) $('.bi').removeClass('bi bi-suit-heart').addClass('bi bi-suit-heart-fill')

    else {
      $('.bi').removeClass('bi bi-suit-heart-fill').addClass('bi bi-suit-heart')  
    }


// Navbar-burger
const hamburger = document.getElementsByClassName('hamburger')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

hamburger.addEventListener('click', () => {
    navbarLinks.classList.toggle('active')
})

window.onscroll = function() {myFunction()};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

//KD3