// Clear the flashed messages after a 2.5 second delay
$("document").ready(function(){
    setTimeout(function(){
        $("div.alert").remove();
    }, 2500 );
});


// Allow users to signup or login and go back in history on window close
if(window.location.href.includes('signup') || window.location.href.includes('login') ) {
    
    $('.close').click( () => {

        // If user navigates from signup to login window go back two pages in history on close
        if(document.referrer.indexOf('signup') !== -1 || document.referrer.indexOf('login') !== -1) {
            history.go(-2)
        }
        else {
        
        // Else go back one page
            history.back();
            return false;
        }
    })
}


$('#edit-commentModal').on('show.bs.modal', function (event) {
    console.log('this works');
    var button = $(event.relatedTarget);


    var title = button.data('title')
    var content = button.data('content')


    var modal = $(this)
    modal.find(".modal-content input").val(title);
    modal.find(".modal-body input").val(content);
})


$('#delete-commentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.data('title')
    var content = button.data('content')


    var modal = $(this)
    modal.find(".modal-body input").val(title);
    modal.find(".modal-footer input").val(content);
})