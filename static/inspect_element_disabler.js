$(document).bind("contextmenu",function(e) {
    e.preventDefault();
   });
   $(document).keydown(function(e){
       if(e.which === 123){
          return false;
       }
   });
document.onkeydown = function(e) {
    var x = 222;
    for (i=0;i<=x;i++){
        if(e.ctrlKey && e.keyCode == i){
            return false;
        }
        if(e.ctrlKey && e.shiftKey && e.keyCode == i){
            return false;
        }
        if(e.altKey && e.keyCode == i){
            return false;
        }
        if(e.altKey && e.shiftKey && e.keyCode == i){
            return false;
        }
    }
    var x= 123;
    for (i=112;i<=x;i++){
        if (e.keyCode == i){
            return false;
        }
    }
    if (e.keyCode == 27){
        return false;
    }
    }