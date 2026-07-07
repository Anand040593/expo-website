import os

css_append = """
/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}

.modal-content {
    background: linear-gradient(135deg, rgba(20, 25, 45, 0.9), rgba(10, 15, 30, 0.95));
    border: 1px solid var(--glass-highlight);
    padding: 40px;
    border-radius: 30px;
    width: 90%;
    max-width: 450px;
    position: relative;
    transform: translateY(40px) scale(0.95);
    transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    box-shadow: 0 30px 60px rgba(0,0,0,0.6), 0 0 30px rgba(255, 107, 0, 0.1);
}

.modal-overlay.active .modal-content {
    transform: translateY(0) scale(1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 20px;
    margin-bottom: 25px;
}

.modal-header h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
}

.close-modal {
    background: rgba(255,255,255,0.1);
    border: none;
    color: #fff;
    width: 36px; height: 36px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-modal:hover {
    background: rgba(255,255,255,0.2);
    transform: rotate(90deg);
}

.modal-price {
    font-size: 3rem;
    color: var(--primary);
    margin: 10px 0 30px;
    text-align: center;
    font-weight: 800;
    text-shadow: 0 0 20px var(--primary-glow);
}

.modal-item {
    text-align: center;
    color: var(--text-muted);
    font-size: 1.1rem;
}

.card-details {
    margin-bottom: 25px;
}

.mock-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 15px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    color: #fff;
    font-size: 1rem;
    font-family: 'Outfit', sans-serif;
    transition: border-color 0.3s;
}

.mock-input:focus {
    outline: none;
    border-color: var(--primary);
}

.card-extra {
    display: flex;
    gap: 15px;
}

.pay-confirm-btn {
    width: 100%;
    padding: 18px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border: none;
    border-radius: 15px;
    color: #fff;
    font-weight: 700;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.4s;
    box-shadow: 0 10px 25px var(--primary-glow);
}

.pay-confirm-btn:hover {
    box-shadow: 0 15px 35px var(--primary-glow);
    transform: translateY(-3px);
}

.payment-success-msg {
    text-align: center;
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(20, 25, 45, 0.95), rgba(10, 15, 30, 0.98));
    border-radius: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    z-index: 10;
    opacity: 1;
    transition: opacity 0.4s;
}

.payment-success-msg.hidden {
    opacity: 0;
    pointer-events: none;
}

.success-icon {
    font-size: 4rem;
    color: #34d399;
    margin-bottom: 20px;
    border: 4px solid #34d399;
    border-radius: 50%;
    width: 90px; height: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 30px rgba(52, 211, 153, 0.3);
    animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes scaleIn {
    0% { transform: scale(0); }
    100% { transform: scale(1); }
}
"""

with open(r"c:\Users\anand\Downloads\Expo_website\styles.css", "a", encoding="utf-8") as f:
    f.write("\n" + css_append)
print("CSS appended successfully.")
