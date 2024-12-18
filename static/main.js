function validateOrderId() {
            const constraint = {
                pattern: /^\d{6}$/,
                message: django.gettext("Order ID must have exactly 6 digits, e.g. 123456")
            };
            const orderIdInput = document.getElementById('order-id');

            if (constraint.pattern.test(orderIdInput.value)) {
                orderIdInput.setCustomValidity("");
            } else {
                orderIdInput.setCustomValidity(constraint.message);
            }
            
            // Trigger the browser's built-in validation UI
            orderIdInput.reportValidity();
        }

        document.addEventListener('DOMContentLoaded', function() {
            const orderIdInput = document.getElementById('order-id');
            const ratingForm = document.getElementById('rating-form');
            
            if (orderIdInput && ratingForm) {
                // Validate on input
                orderIdInput.addEventListener('input', validateOrderId);
                
                // Validate on form submission
                ratingForm.addEventListener('submit', function(event) {
                    validateOrderId();
                    if (!orderIdInput.validity.valid) {
                        event.preventDefault();
                    }
                });

                // Update form ID when order ID changes
                orderIdInput.addEventListener('input', function() {
                    ratingForm.id = this.value || 'rating-form';
                });
            }
        });

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            // Get the CSRF token from the rating form specifically
            xhr.setRequestHeader("X-CSRFToken", $('.rate-form [name=csrfmiddlewaretoken]').val());
        }
    }
});

// get all the stars
const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');

const form = document.querySelector('.rate-form');
const confirmBox = document.getElementById('confirm-box');
const csrf = document.getElementsByName('csrfmiddlewaretoken');

// Select all star buttons
const starButtons = document.querySelectorAll('.rate-buttons button');

let selectedRating = 0;
const selectedRatingInput = document.getElementById('selected-rating');

// Function to handle star selection
const handleStarSelect = (rating) => {
    starButtons.forEach((button, index) => {
        if (index < rating) {
            button.classList.add('checked');
        } else {
            button.classList.remove('checked');
        }
    });
}

// Add click event listeners to star buttons
starButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        handleStarSelect(index + 1);
        selectedRating = index + 1;
        selectedRatingInput.value = selectedRating;
    });

    // Add mouseover event
    button.addEventListener('mouseover', () => {
        handleStarSelect(index + 1);
    });

    // Add mouseout event
    button.addEventListener('mouseout', () => {
        handleStarSelect(selectedRating);
    });
});

// Add mouseout event to the container
document.querySelector('.rate-buttons').addEventListener('mouseout', () => {
    handleStarSelect(selectedRating);
});

// Form submission handler
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Validate the order ID before submission
    validateOrderId();
    const orderIdInput = document.getElementById('order-id');
    if (!orderIdInput.validity.valid) {
        return; // Stop form submission if order ID is invalid
    }
    
    // Check if a rating has been selected
    if (selectedRating === 0) {
        alert(django.gettext('Please select a rating before submitting.'));
        console.log(gettext('Please select a rating before submitting.'));
        return; // Stop form submission if no rating is selected
    }
    
    const order_id = orderIdInput.value;
    const review_text = document.getElementById('review-text').value;

    $.ajax({
        type: 'POST',
        url: rateUrl,
        data: {
            'el_id': order_id,
            'val': selectedRating,
            'review': review_text,
        },
        success: function(response) {
            if (response.success === 'false') {
                orderIdInput.setCustomValidity(response.error);
                orderIdInput.reportValidity();
            } else {
                // Redirect to the success page
                window.location.href = response.redirect_url;
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});
