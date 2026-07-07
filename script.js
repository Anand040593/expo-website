// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Scroll Reveal Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .pricing-card, .event-item, .section-title, .hero-text, .hero-image-wrapper').forEach(el => {
    el.classList.add('fade-up');
    observer.observe(el);
});

// Custom Mock Payment Modal Logic
const modalOverlay = document.getElementById('payment-modal');
const modalItemName = document.getElementById('modal-item-name');
const modalAmount = document.getElementById('modal-amount');
const paymentSuccess = document.getElementById('payment-success');

function initiatePayment(itemName, amount) {
    // Populate modal data
    modalItemName.textContent = "Payment for " + itemName;
    modalAmount.textContent = "₹" + amount.toLocaleString('en-IN');
    
    // Reset success state if it was shown before
    paymentSuccess.classList.add('hidden');
    
    // Show modal
    modalOverlay.classList.add('active');
}

function closePaymentModal() {
    modalOverlay.classList.remove('active');
}

function processMockPayment() {
    // Show success message within modal
    paymentSuccess.classList.remove('hidden');
}

// Close modal when clicking outside of it
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        closePaymentModal();
    }
});
