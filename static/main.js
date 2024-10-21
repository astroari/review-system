function validateOrderId() {
            const constraint = {
                pattern: /^\d{6}$/,
                message: "Order ID must have exactly 6 digits, e.g. 123456"
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

// get all the stars
const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');

const form = document.querySelector('.rate-form');
const confirmBox = document.getElementById('confirm-box');

const csrf = document.getElementsByName('csrfmiddlewaretoken');

const rateButtons = document.querySelector('.rate-buttons');

const handleStarSelect = (size) => {
    const children = rateButtons.children;
    for (let i = 0; i < children.length; i++) {
        if (i<size) {
            children[i].classList.add('checked');
        } else {
            children[i].classList.remove('checked');
        }
    }
}

const arr = [one, two, three, four, five];

const handleSelect = (selection) => {
    switch (selection) {
        case 'first': { 
            handleStarSelect(1);
            return;  
        }
        case 'second': {
            handleStarSelect(2);
            return;
        }
        case 'third': {
            handleStarSelect(3);
            return;
        }
        case 'fourth': {
            handleStarSelect(4);
            return;
        }
        case 'fifth': {
            handleStarSelect(5);
            return;
        }
    }
}

const getNumericValue = (stringValue) => {
    let numericValue;
    if (stringValue === 'first') {
        numericValue = 1;
    }
    else if (stringValue === 'second') {
        numericValue = 2;
    }
    else if (stringValue === 'third') {
        numericValue = 3;
    }
    else if (stringValue === 'fourth') {
        numericValue = 4;
    }
    else if (stringValue === 'fifth') {
        numericValue = 5;
    }
    else {
        numericValue = 0;
    }
    return numericValue;
}

if (one) {
    arr.forEach(star => {star.addEventListener('mouseover', (event) => {
        handleSelect(event.target.id);
    });
    });

    arr.forEach(star => {star.addEventListener('click', (event) => {
        const value = event.target.id;
        console.log(value);

        let isSubmit = false;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (isSubmit) {
                return;
            }
            
            // Validate the order ID before submission
            validateOrderId();
            const orderIdInput = document.getElementById('order-id');
            if (!orderIdInput.validity.valid) {
                return; // Stop form submission if order ID is invalid
            }
            
            isSubmit = true;
            const order_id = e.target.id;
            console.log(order_id);
            const val_num = getNumericValue(value);
            const review_text = document.getElementById('review-text').value;

            $.ajax({
                type: 'POST',
                url: '/rate/',
                data: {
                    'el_id': order_id,
                    'val': val_num,
                    'review': review_text,
                    'csrfmiddlewaretoken': csrf[0].value
                },
                success: function(response) {
                    console.log(response);
                    confirmBox.innerHTML = `<h1>Successfully rated with ${response.score}</h1>`;
                },
                error: function(error) {
                    console.log(error);
                    confirmBox.innerHTML = `<h1>Something went wrong</h1>`;
                }
            });
        });
    });
})};
