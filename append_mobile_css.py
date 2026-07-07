import os

mobile_css = """
/* Extended Mobile Optimizations */
@media (max-width: 480px) {
    .section-padding { padding: 60px 0; }
    
    .section-title { font-size: 1.8rem; margin: 0 auto 40px; }
    
    .hero { padding: 40px 10px; min-height: auto; }
    .hero-text h2 { font-size: 2rem; margin-bottom: 15px; letter-spacing: -1px; }
    .hero-text p { font-size: 1rem; margin-bottom: 25px; }
    
    .primary-btn { padding: 15px 30px; font-size: 1rem; width: 100%; text-align: center; }
    
    .features-grid { grid-template-columns: 1fr; gap: 20px; }
    .feature-card { padding: 30px 20px; }
    .feature-icon { width: 50px; height: 50px; font-size: 1.8rem; }
    
    .pricing-grid { grid-template-columns: 1fr; gap: 30px; }
    .pricing-card { padding: 30px 20px; }
    .pricing-header h3 { font-size: 1.8rem; }
    .popular-badge { padding: 6px 15px 5px; font-size: 0.75rem; letter-spacing: 1px; }
    
    .events-list { gap: 15px; }
    .event-item { padding: 15px; }
    .event-info h3 { font-size: 1.1rem; }
    .payment-btn.small { padding: 10px 15px; font-size: 0.85rem; width: 100%; margin-top: 10px; }
    
    .footer { padding: 50px 0 20px; margin-top: 50px; }
    .footer-content { gap: 30px; flex-direction: column; text-align: center; }
    .footer h3::after { left: 50%; transform: translateX(-50%); }
    
    .header-text h1 { font-size: 1.2rem; }
    .subtitle { font-size: 0.7rem; }
    .logo { height: 45px; }
    .event-date { font-size: 0.8rem; padding: 6px 12px; }
    
    .modal-content { padding: 25px 20px; }
    .modal-price { font-size: 2rem; margin-bottom: 20px; }
    .modal-header h3 { font-size: 1.2rem; }
    
    body::before, body::after { filter: blur(70px); width: 300px; height: 300px; }
}
"""

with open(r"c:\Users\anand\Downloads\Expo_website\styles.css", "a", encoding="utf-8") as f:
    f.write("\n" + mobile_css)

print("Mobile CSS optimizations appended successfully.")
