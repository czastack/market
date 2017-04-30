(function (){
  var $repwd = $('#repassword');
  if ($repwd.length) 
    $($repwd[0].form).submit(function(){
      var ok = this.password.value == $repwd.val();
      $repwd.next('.help-block').toggleClass('hidden', ok);
      $('#repassword-parent').toggleClass('has-error', !ok);
      return ok;
    })
})();