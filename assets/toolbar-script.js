(function() {
    'use strict';
    var header = document.querySelector('header');
    var navbar = document.querySelector('nav');
    var brandContainer = document.querySelector('.brand__container');
    var brandContainerMobile = document.querySelector('.brand__container--mobile');
    window.addEventListener('scroll', refreshToolbarVisibility);
    window.addEventListener('resize', refreshToolbarVisibility);
    var palmWidth = 800;
    refreshToolbarVisibility();
    function refreshToolbarVisibility(e) {
        if(window.innerWidth > palmWidth) {
            var boundingRect = brandContainer.getBoundingClientRect();
            var brandContainerHeight = boundingRect.height;
            var brandContainerY = boundingRect.y || boundingRect.top;
            if(brandContainerY + brandContainerHeight - 40 > 0) {
                navbar.style.display = "none";
            } else {
                navbar.style.display = "block";
            }
        } else {
            var boundingRect = brandContainerMobile.getBoundingClientRect();
            var brandContainerHeight = boundingRect.height;
            var brandContainerY = boundingRect.y || boundingRect.top;
            navbar.style.display = "block";
            navbar.style.opacity = 1;
        }
    }
})();