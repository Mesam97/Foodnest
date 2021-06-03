// LIKE-funktionen
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
  console.log(liked)
    if (liked==1) $('.bi').removeClass('bi bi-suit-heart').addClass('bi bi-suit-heart-fill')

    else {
      $('.bi').removeClass('bi bi-suit-heart-fill').addClass('bi bi-suit-heart')  
    }


// Navbar-burger
const hamburger = document.getElementsByClassName('hamburger')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

  hamburger.addEventListener('click', () => {
      navbarLinks.classList.toggle('active')

  });
