
 First, include the jQuery and masked input javascript files.

 <script src="jquery.js" type="text/javascript"></script>
 <script src="jquery.maskedinput.js" type="text/javascript"></script>

 Next, call the mask function for those items you wish to have masked.

 jQuery(function($){
        $("#date").mask("99/99/9999",{placeholder:"mm/dd/yyyy"});
        $("#phone").mask("(999) 999-9999");
        $("#tin").mask("99-9999999");
        $("#ssn").mask("999-99-9999");
 });

 Optionally, if you are not satisfied with the underscore ('_') character as a placeholder,
 you may pass an optional argument to the maskedinput method.

 jQuery(function($){
        $("#product").mask("99/99/9999",{placeholder:" "});
 });

 Optionally, if you would like to execute a function once the mask has been completed, 
 you can specify that function as an optional argument to the maskedinput method.

 jQuery(function($){
        $("#product").mask("99/99/9999",{completed:function(){alert("You typed the following: "+this.val());}});
 });

 You can now supply your own mask definitions.

 jQuery(function($){
        $.mask.definitions['~']='[+-]';
        $("#eyescript").mask("~9.99 ~9.99 999");
 });

 You can have part of your mask be optional. Anything listed after '?' within the mask
 is considered optional user input. The common example for this is phone number + optional extension.

 jQuery(function($){
        $("#phone").mask("(999) 999-9999? x99999");
 });

 If your requirements aren't met by the predefined placeholders, you can always add your own. 
 For example, maybe you need a mask to only allow hexadecimal characters. You can add your 
 own definition for a placeholder, say 'h', like so: $.mask.definitions['h'] = "[A-Fa-f0-9]"; 
 Then you can use that to mask for something like css colors.

 jQuery(function($){
        $("#phone").mask("#hhhhhh");
 });

 By design, this plugin will reject input which doesn't complete the mask. You can bypass 
 this by using a '?' character at the position where you would like to consider input optional. 
 For example, a mask of "(999) 999-9999? x99999" would require only the first 10 digits of a 
 phone number with extension being optional.

 
