$(function(){
  $("nav li").on("click",function(){
    $(this).addClass("active").siblings().removeClass("active");

    if($(this).index() == 0){
      $("section").addClass("first-selected");
    }else{
      $(".main-container > section").removeClass("first-selected");
    }
  });
});