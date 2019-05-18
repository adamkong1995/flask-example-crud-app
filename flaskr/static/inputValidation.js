(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        select_validation_init();
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

const select_validation_init = () => {
  var selects = document.querySelectorAll('.selectpicker');

  selects.forEach(select => {
      // Check if selected is &nbsp;
      if (select.value == String.fromCharCode(160)) {
          select.setCustomValidity('Invalid field.');
      } else {
          select.setCustomValidity('');
      }
  })
}

document.addEventListener("DOMContentLoaded", () => select_validation_init());