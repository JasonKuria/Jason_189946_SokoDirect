// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  //hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none'
  )
}

// SokoDirect Front-End Interaction Controllers
document.addEventListener("DOMContentLoaded", function () {
    const alertCloseButtons = document.querySelectorAll(".alert__close");

    alertCloseButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            // Locates the parent container component and instantly removes it from view
            const parentAlertContainer = this.parentElement;
            if (parentAlertContainer) {
                parentAlertContainer.style.transition = "opacity 0.5s ease-out";
                parentAlertContainer.style.opacity = "0";
                setTimeout(() => {
                    parentAlertContainer.remove();
                }, 500);
            }
        });
    });
});