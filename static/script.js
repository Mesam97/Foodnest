// Väntar på att sidan ska bli redo för att köra vårt JavaScript
$(document).ready(function() {
	$("#changePassword").on("click", function() {
        // Frågar användaren efter det gamla och det nya lösenordet
		var old_password = prompt("Ange ditt gamla lösenord");
        var new_password = prompt("Ange ditt nya lösenord");
        // Ändrar lösenordet

    $("#delete").on("click", function() {
        // Frågar användaren efter vilket inlägg som ska bort
        var remove = prompt("Ange titeln på det inlägg som du vill ta bort");
        // tar bort det valda inlägget
    })
})
});