$(document).ready(function(){
    $('#btn').click(function(){
      $('#post').hide('slow');
      $('#btn').html('NEXT     PAGE')
      $('#btn').animate({
        'marginRight':'-40%'
      },'slow')
    })
  });

var is_clicked = false;
var clicked_obj;

alert('hi');

function func2(the_obj){
  if (is_clicked == false){
      the_obj.style.backgroundColor = "#049dc8";
      is_clicked = true;
      clicked_obj = the_obj;
  } else {
    clicked_obj.style.backgroundColor = "#036f96";
    clicked_obj = the_obj;
    the_obj.style.backgroundColor = "#049dc8";
  }
}