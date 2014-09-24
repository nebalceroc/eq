/** upload
  * This function make of upload of files
*/
$(document).ready(function(){
    $(".Real_State").attr('name','category');
    $(".Vehicles").attr('name','category');
    $(".Electronics").attr('name','category');
    $(".Others").attr('name','category');
    $(".upimg").hide();
    $("#upload_1").on('change',function(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend=function (event){
            var img = this.result;
            if($("load1")){
              $("#load1").remove();
            }
            $("#image1").append('<img id="load1" src="'+img+'" width="100px" height="100px"/>');
            $(this).hide();
            $('#image2').show()
        }
    });
    $("#upload_2").on('change',function(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend=function (event){
            var img = this.result;
            if($("load2")){
              $("#load2").remove();
            }
            $("#image2").append('<img id="load2" src="'+img+'" width="100px" height="100px"/>');
            $(this).hide();
            $('#image3').show()
        }
    });
    $("#upload_3").on('change',function(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend=function (event){
            var img = this.result;
            if($("load3")){
              $("#load3").remove();
            }
            $("#image3").append('<img id="load3" src="'+img+'" width="100px" height="100px"/>');
            $(this).hide();
            $('#image4').show()
        }
    });
    $("#upload_4").on('change',function(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend=function (event){
            var img = this.result;
            if($("load4")){
              $("#load4").remove();
            }
            $("#image4").append('<img id="load4" src="'+img+'" width="100px" height="100px"/>');
            $(this).hide();
            $('#image5').show()
        }
    });
    $("#upload_5").on('change',function(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend=function (event){
            var img = this.result;
            if($("load5")){
              $("#load5").remove();
            }
            $("#image5").append('<img id="load5" src="'+img+'" width="100px" height="100px"/>');
            $(this).hide();
        }
    });
});
