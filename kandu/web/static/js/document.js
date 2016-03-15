
$(document).ready(function(){

   function assign_rule(evt){
      console.log($("#identify div.btn-group").index($(this).closest("div.btn-group")));
      var i = $("#identify div.btn-group").index($(this).closest("div.btn-group"));
      var v = $("#ie1").val();
      if (v != ''){
         // Rule has a name: we can assign the rule to the item
         $.ajax({'url': 'setrule',
            'type': 'POST',
            'data': 'i='+i+"&v="+v,
            'success': function(data){
               $("div#identify").html(data);
               connectBitsBtn();
               $("#ie1").val('');
            }
         });
      }
      else{
         // Rule has no name: we shift to the inputbox to ask for a name
         // and pop the popover
         console.log("no rule name");
         scrollTo('#varinputdiv');
         $("#varinputdiv").addClass("has-feedback");
         $("#varinputdiv").addClass("has-error");

      }
   };

   function assign_joker(evt){
      console.log($("#identify div.btn-group").index($(this).closest("div.btn-group")));
      var i = $("#identify div.btn-group").index($(this).closest("div.btn-group"));
      var v = '*';
         // Rule has a name: we can assign the rule to the item
         $.ajax({'url': 'setrule',
            'type': 'POST',
            'data': 'i='+i+"&v="+v,
            'success': function(data){
               $("div#identify").html(data);
               connectBitsBtn();
            }
         });
   };

   function ignore_folder(evt){
      var i = $("#identify div.btn-group").index($(this).closest("div.btn-group"));
      var v = '**';
         // Rule has a name: we can assign the rule to the item
         $.ajax({'url': 'setrule',
            'type': 'POST',
            'data': 'i='+i+"&v="+v,
            'success': function(data){
               $("div#identify").html(data);
               connectBitsBtn();
            }
         });
   };

   function split(evt){
      console.log($("div.bit").index($(this).closest("div.bit")));
      var i = $("div.bit").index($(this).closest("div.bit"));

      $.ajax({'url': 'split',
         'type': 'POST',
         'data': 'i='+i,
         'success': function(data){
            $("div#identify").html(data);
            connectBitsBtn();
         }
      });
   };

   function connectBitsBtn(){
            $("ul.dropdown-menu").dropdown();
            $("li.assign").click(assign_rule);
            $("li.split").click(split);
            $("li.addrule").click(addrule);
            $("li.joker").click(assign_joker);
            $("li.ignorefolder").click(ignore_folder);
            $("#filterextension").click(filterextension);
   };

   function addrule(evt){
      var i = $("#ie2").val();
      $.ajax({'url': 'addrule',
         'type': 'POST',
         'data': 'text='+i,
         'success': reloadRules
      });
   };

   function filterextension(evt){
      ext = $(this).data('ext');
      console.log(ext);
      $.ajax({'url': 'filterext',
         'type': 'POST',
         'data': 'ext='+ext,
         'success': reloadRules
      });
   };

   function validate(evt){
      var params = {validate:"validate"};
      $("#loading-image").show();
      $.ajax({
         type: "POST",
         url: 'validate',
         data: params,
         success: function(data){
            $("#statsOne div.panel-body").html(data);
         },
         complete: function(){
            $("#loading-image").hide();
         },
      });
   };

   function save(evt){
      var params = {validate:"save"};
      $.ajax({
         type: "POST",
         url: 'validate',
         data: params,
         success: function(data){
            alert("saved.");
         }
      });
   };

   // On first inputbox keypress event
   $('#ie1').keyup(function(e){
      if ($(this).val() != ""){
         $("li.assign").html('<a href="#">Set rule '+ $("#ie1").val() + "</a>");
      }
      else {
         $("li.assign").html('<a href="#">Set rule</a>');
      }
      if(e.keyCode == 13) {
         $(this).trigger("enterKey");
      }
      if ($("#varinputdiv").hasClass('has-error')){
         $("#varinputdiv").removeClass('has-feedback');
         $("#varinputdiv").removeClass('has-error');
      }
   });

   // On second inputbox keypress event
   $('#ie2').keyup(function(e){
      if ($("#ruleinputdiv").hasClass('has-error')){
         $("#ruleinputdiv").removeClass('has-feedback');
         $("#ruleinputdiv").removeClass('has-error');
      }
      if(e.keyCode == 13) {
         $('#addrule').click();
      }
   });

   // Click on addrule button
   $("#addrule").click(function(e){
      var length = $("div#identify").children('div.btn-group').length;
      if (length == 0){

         scrollTo('#repository');
         $("#ie2").val("");
      }
      else if ($("#ie2").val() == ''){

         // if no rule name provided
         scrollTo("#ruleinputdiv");
         $("#ruleinputdiv").addClass("has-feedback");
         $("#ruleinputdiv").addClass("has-error");
      }
      else {
         // if a rule name is provided, then add it
         addrule(e);
         $("#ie2").val("");
      }

   });

   function scrollTo(id){
            $('html, body').animate({
               scrollTop: $(id).offset().top
            }, 500);
   }

   function reloadRules(data){
            $("#rulesOne div.panel-body").html(data);
            connectRulesBtn();
            scrollTo('#rulesOne');
   };

   function connectLoadPresetsBtn(){
            $(".loadjson").click(loadPreset);
            $(".loadopenfmri").click(loadPreset);
            $(".loadfreesurfer").click(loadPreset);
            $(".loadmorpho").click(loadPreset);
            $(".reset").click(loadPreset);
   };

   function connectRulesBtn(){
            $("#checkrules").click(checkRules);
            $("#validate").click(validate);
            $("#save").click(save);
            connectLoadPresetsBtn();
   }
   function connectPreviewBtn(){
      $("#togglepreview").click(togglepreview);
      $("div#repository a.btn").click(clickFile);
   }

   function loadPreset(e){
      cls = $(this).attr('class');
      $.ajax({'url': 'preset',
         'type': 'POST',
         'data': 'p=' + cls,
         'success': reloadRules
      });
   };

   function checkRules(e){
      var files = Array();
      var selected = Array();
      $("div#repository a.btn").each(function(){
         files.push($(this).data('path'))
      });
      $("#hierarchy label").each(function(){
         if ($(this).hasClass('active')){
            selected.push($(this).data('rule'));
         }
      });
      var params = { files:files,
                     selected:selected };
      console.log(params);
      $.ajax({'url': 'validate',
         'type': 'POST',
         'data': params,
         'success': function(data){
            var res = JSON.parse(data);
            var valid = res['valid'];
            var labels = res['labels'];
            var repo = res['repo'];
            $("#repository").html(repo);
            $("#repository a.btn").each( function(){
               var path = $(this).data('path');
               var index = $.inArray(path, valid);
               console.log(index);
               if (index != -1) {
                  $(this).css('background-color', '#aaaaaa');
                  $(this).after("<span> -- " + labels[index] + "</span>");
               }
            });
            connectPreviewBtn();
            scrollTo("#repository");
         }
      });
   };

   function clickFile(e){
      var path = $(this).data('path');
      var ext = path.split('.').pop();
      $.ajax({'url': 'identify',
         'type': 'POST',
         'data': 'path='+ path,
         'success': function(data){
            $("div#identify").html(data);
            $("#filterextension").text('Add rule for .'+ext);
            $("#filterextension").data("ext", ext);
            $("#filterextension").show();
            connectBitsBtn();
            scrollTo("#identify");
         }
      });
   };
   function togglepreview(e){
      isActive = $(this).hasClass('active');
      if (isActive){
         isActive = '0';
      }
      else {
         isActive = '1';
         $("#loading-image").show();
      }
      $.ajax({'url': 'togglepreview',
         'type': 'get',
         'data': 'unknown_only='+isActive,
         'success': function(data){
            $("div#repository").html(data);
            $("#loading-image").hide();
            connectPreviewBtn();
            connectLoadPresetsBtn();
         }
      });

   };

   connectRulesBtn();
   connectPreviewBtn();
});
