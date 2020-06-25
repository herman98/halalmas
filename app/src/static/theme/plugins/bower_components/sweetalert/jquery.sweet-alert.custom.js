var delay = ( function() {
    var timer = 0;
    return function(callback, ms) {
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // console.log(cookieValue);
    return cookieValue;
}

function call_ajax_activation(url_project_activation, token_in, status_to_set){
    // console.log("create post is working!") // sanity check
    var csrftoken = getCookie('csrftoken');
    var ret_func = NaN;

    ret_func = $.ajax({
        url :  url_project_activation, // the endpoint
        type : "POST", // http method
        data : { token_id     : token_in ,
                 user_status : status_to_set ,
                 csrfmiddlewaretoken: csrftoken,
            }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            // console.log(json); // log the returned json to the console
            // console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            err_msg = "Oops! We have encountered an error: "+errmsg; 
            console.log(err_msg);
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    
    return ret_func;
}

!function($) {
    "use strict";

    var SweetAlert = function() {};

    //examples 
    SweetAlert.prototype.init = function() {
        
    //Basic
    $('#sa-basic').click(function(){
        swal("Here's a message!");
    });

    //A title with a text under
    $('#sa-title').click(function(){
        swal("Here's a message!", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lorem erat eleifend ex semper, lobortis purus sed.")
    });

    //Success Message
    $('#sa-success').click(function(){
        swal("Good job!", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lorem erat eleifend ex semper, lobortis purus sed.", "success")
    });

    //Warning Message
    $('#sa-warning').click(function(){
        swal({   
            title: "Are you sure?",   
            text: "You will not be able to recover this imaginary file!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Yes, delete it!",   
            closeOnConfirm: false 
        }, function(){   
            swal("Deleted!", "Your imaginary file has been deleted.", "success"); 
        });
    });

    //Warning Message
    $('#signout-warning').click(function(){
        swal({   
            title: "Yakin untuk Logout?",   
            text: "Anda dapat melakukan login kembali setelah logout sukses!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Ya, Logout!",   
            closeOnConfirm: false,
            cancelButtonText: "Batal"
        }, function(){   
            swal("Sukses!", "Logout berhasil.", "success"); 
        	var url_project = document.getElementById("proj_url").innerHTML;
        	delay(function(){
			    window.location = url_project+"/accounts/logout";
			}, 1000 ); // end delay
        });
    });

    //Warning Message
    $('#signout-warning2').click(function(){
        swal({   
            title: "Yakin untuk Logout?",   
            text: "Anda dapat melakukan login kembali setelah logout sukses!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Ya, Logout!",   
            closeOnConfirm: false,
            cancelButtonText: "Batal"
        }, function(){   
            swal("Sukses!", "Logout berhasil.", "success"); 
            var url_project = document.getElementById("proj_url").innerHTML;
            delay(function(){
                window.location = url_project+"/accounts/logout";
            }, 1000 ); // end delay
        });
    });

    //Parameter
    $('#sa-params').click(function(){
        swal({   
            title: "Are you sure?",   
            text: "You will not be able to recover this imaginary file!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Yes, delete it!",   
            cancelButtonText: "No, cancel plx!",   
            closeOnConfirm: false,   
            closeOnCancel: false 
        }, function(isConfirm){   
            if (isConfirm) {     
                swal("Deleted!", "Your imaginary file has been deleted.", "success");   
            } else {     
                swal("Cancelled", "Your imaginary file is safe :)", "error");   
            } 
        });
    });

    //Custom Image
    $('#sa-image').click(function(){
        swal({   
            title: "Govinda!",   
            text: "Recently joined twitter",   
            imageUrl: "../plugins/images/users/govinda.jpg" 
        });
    });

    //Auto Close Timer
    $('#sa-close').click(function(){
         swal({   
            title: "Auto close alert!",   
            text: "I will close in 2 seconds.",   
            timer: 2000,   
            showConfirmButton: false 
        });
    });


    //Activation Message
    $('*[id^=id_kmart_data_activated_]').click(function(){
        var current_id = $(this).attr('id').replace("id_kmart_data_activated_","");

        var local_var_one = document.getElementById("local_var_one_"+current_id).innerHTML;
        var local_var_two = document.getElementById("id_btn_text_"+current_id).innerHTML;
        var local_var_three = document.getElementById("local_var_three").innerHTML;
        var url_project = document.getElementById("kurirmart_activate_url").innerHTML;
        // alert(local_var_one + ";" +local_var_two+ ";" +local_var_three);   

        //get token
        var token = document.getElementById("id_token_"+current_id).innerHTML;

        if(local_var_two=="Aktifkan"){
            swal({   
            title: "Aktivasi "+local_var_three+"?",   
            text: "Pengguna dengan nama "+ local_var_one +" akan diaktifkan!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Aktifkan!",   
            closeOnConfirm: false,
            cancelButtonText: "Batal"
        }, function(){   
            
            delay(function(){
                //window.location = url_project+"/logout";
                //ajax to update status
                var ret = call_ajax_activation(url_project, token, 1);
                // alert(ret);
                //if success
                if(ret != NaN){
                    swal("Sukses!", "Data berhasil di Aktifkan.", "success"); 
                    $('#id_btn_aktivasi_'+current_id).removeClass('btn-success').addClass('btn-danger');
                    $("#id_btn_text_"+current_id).html("Non-Aktifkan");
                    $('#id_btn_icon_'+current_id).removeClass('fa-check-circle').addClass('fa-times');
                    $("#id_status_active_"+current_id).html('<i class="fa fa-check"></i> Ya');
                    $('#id_status_active_'+current_id).removeClass('label-danger').addClass('label-info');
                    
                }else{
                    swal("Error!", "Aktivasi Gagal.", "error"); 
                }
            }, 1000 ); // end delay
        });
        }
        else { // status = active -> change to non-active with confirmation
            swal({   
            title: "Non-Aktivasi "+local_var_three+"?",   
            text: "Pengguna dengan nama "+ local_var_one +" akan di non-aktifkan!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Non-Aktifkan!",   
            closeOnConfirm: false,
            cancelButtonText: "Batal"
        }, function(){   
            
            delay(function(){
                //ajax to update status
                var ret = call_ajax_activation(url_project, token, 0);
                // alert(ret);
                if(ret != NaN){
                    swal("Sukses!", "Data berhasil di Non-Aktifkan.", "success"); 
                    //if success
                    $('#id_btn_aktivasi_'+current_id).removeClass('btn-danger').addClass('btn-success');
                    $("#id_btn_text_"+current_id).html("Aktifkan");
                    $('#id_btn_icon_'+current_id).removeClass('fa-times').addClass('fa-check-circle');
                    $("#id_status_active_"+current_id).html('<i class="fa fa-check"></i> Tidak');
                    $('#id_status_active_'+current_id).removeClass('label-info').addClass('label-danger');
                }
                else{
                    swal("Error!", "Aktivasi Gagal.", "error"); 
                }
            }, 1000 ); // end delay
        });
        }
        
    });


    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.SweetAlert.init()
}(window.jQuery);