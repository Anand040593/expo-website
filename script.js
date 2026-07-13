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
});

document.querySelectorAll('.fade-up').forEach(el => {
    observer.observe(el);
});

// Custom Mock Payment Modal Logic & Registration
const modalOverlay = document.getElementById('payment-modal');
const modalItemName = document.getElementById('modal-item-name');
const modalAmount = document.getElementById('modal-amount');
const paymentSuccess = document.getElementById('payment-success');

let currentItem = "";
let currentAmount = 0;
let isCurrentStall = false;

function initiatePayment(itemName, amount, isStall = false) {
    currentItem = itemName;
    currentAmount = amount;
    isCurrentStall = isStall;
    
    // Populate modal data
    modalItemName.textContent = "Payment for " + itemName;
    modalAmount.textContent = "₹" + amount.toLocaleString('en-IN');
    
    // Reset success state
    paymentSuccess.classList.add('hidden');
    
    // Clear standard inputs
    const inputs = ['reg-name', 'reg-email', 'reg-phone', 'reg-address', 'reg-company', 'reg-company-desc'];
    inputs.forEach(id => {
        const el = document.getElementById(id);
        if(el) {
            el.value = '';
            el.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        }
    });
    
    // Show/hide stall specific fields
    const stallFields = document.querySelectorAll('.stall-only');
    stallFields.forEach(el => {
        if(isStall) {
            el.style.display = 'block';
        } else {
            el.style.display = 'none';
        }
    });
    
    // Show modal
    modalOverlay.classList.add('active');
}

function closePaymentModal() {
    modalOverlay.classList.remove('active');
}

async function processMockPayment() {
    const name = document.getElementById('reg-name')?.value;
    const email = document.getElementById('reg-email')?.value;
    const phone = document.getElementById('reg-phone')?.value;
    const address = document.getElementById('reg-address')?.value;
    
    const companyName = document.getElementById('reg-company')?.value || "";
    const companyDesc = document.getElementById('reg-company-desc')?.value || "";
    
    if(!name || !email || !phone || !address) {
        alert("Please fill in all standard registration details!");
        return;
    }
    
    if(isCurrentStall && (!companyName || !companyDesc)) {
        alert("Please fill in the Company details required for stall booking!");
        return;
    }
    
    const payload = {
        name: name,
        email: email,
        phone: phone,
        address: address,
        item_name: currentItem,
        amount: currentAmount,
        is_stall: isCurrentStall,
        company_name: companyName,
        company_desc: companyDesc
    };
    
    try {
        const response = await fetch('api/register.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            paymentSuccess.classList.remove('hidden');
        } else {
            alert("Error saving registration details to database.");
        }
    } catch (err) {
        alert("Failed to connect to the backend server. Please make sure server.py is running!");
    }
}

// Close modal when clicking outside of it
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        closePaymentModal();
    }
});
