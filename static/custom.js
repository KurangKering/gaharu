 'use strict';

 function showSpinner() {
    // Initialize
    if ($('.kintone-spinner').length == 0) {
        // Create elements for the spinner and the background of the spinner
        var spin_div = $('<div id ="kintone-spin" class="kintone-spinner"></div>');
        var spin_bg_div = $('<div id ="kintone-spin-bg" class="kintone-spinner"></div>');

        // Append spinner to the body
        $(document.body).append(spin_div, spin_bg_div);

        // Set a style for the spinner
        $(spin_div).css({
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'z-index': '510',
            'padding': '26px',
            '-moz-border-radius': '4px',
            '-webkit-border-radius': '4px',
            'border-radius': '4px'
        });
        $(spin_bg_div).css({
            'position': 'fixed',
            'top': '0px',
            'left': '0px',
            'z-index': '500',
            'width': '100%',
            'height': '200%',
            'background-color': '#000',
            'opacity': '0.5',
            'filter': 'alpha(opacity=50)',
            '-ms-filter': "alpha(opacity=50)"
        });

        // Set options for the spinner
        var opts = {
            'color': '#fff'
        };

        // Create the spinner
        new Spin.Spinner(opts).spin(document.getElementById('kintone-spin'));
    }

    // Display the spinner
    $('.kintone-spinner').show();
}

// Function to hide the spinner
function hideSpinner() {
    // Hide the spinner
    $('.kintone-spinner').hide();
}
