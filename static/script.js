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
      window.location.href=('?liked=True')
    }                 

    else {
      window.location.href=('?liked=False')
      }
  })

  let liked = $('.bi').attr('liked')
  
    if (liked==='True') $('.bi').removeClass('bi bi-suit-heart').addClass('bi bi-suit-heart-fill')

    else {
      $('.bi').removeClass('bi bi-suit-heart-fill').addClass('bi bi-suit-heart')  
    }
