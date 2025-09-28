// Create background particles
function createParticles() {
  const particlesContainer = document.getElementById('particles');
  if (!particlesContainer) return;
  for (let i = 0; i < 20; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.width = Math.random() * 4 + 2 + 'px';
    particle.style.height = particle.style.width;
    particle.style.animationDuration = Math.random() * 3 + 3 + 's';
    particle.style.animationDelay = Math.random() * 2 + 's';
    particlesContainer.appendChild(particle);
  }
}

// Add ripple effect to buttons
function addRippleEffect() {
  document.querySelectorAll('.glass-button, .social-btn').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.className = 'ripple';
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });
}

// Language selector functionality
const translations = {
  en: {
    "main-title": `<span class="text-primary">HYDRO</span> HARVEST`,
    "subtitle": "Your Solution for Sustainable Water Management",
    "join-revolution": `Join the Water <span class="text-primary">Revolution</span>`,
    "discover-potential": "Discover the potential of rainwater harvesting at your location. Start your journey towards sustainable water management and contribute to groundwater conservation.",
    "liters-saved": "Liters Saved",
    "happy-users": "Happy Users",
    "get-started": "Get Started",
    "user-login": "User Login",
    "continue-google": "Continue with Google",
    "continue-mobile": "Continue with Mobile",
    "admin-login": "Admin Login",
    "admin-login-btn": "Admin Login",
    "enter-mobile": "Enter mobile number",
    "send-otp": "Send OTP",
    "otp-sent-to": "Enter the 6-digit code sent to ",
    "verify-continue": "Verify & Continue",
    "resend-otp": "Resend OTP",
    "terms-agree": `By continuing, you agree to our <a href="#" class="text-primary hover:underline">Terms of Service</a> and <a href="#" class="text-primary hover:underline">Privacy Policy</a>`,
    "conservation-starts": `Water Conservation Starts with <span class="text-primary">You</span>`,
    "every-drop-counts": "Every drop counts in our mission to preserve water for future generations. Learn how rainwater harvesting can transform your property into a water-positive asset.",
    "env-impact": "Environmental Impact",
    "env-impact-desc": "Reduce groundwater depletion and support ecosystem sustainability",
    "cost-savings": "Cost Savings",
    "cost-savings-desc": "Significant reduction in water bills and long-term financial benefits",
    "prop-value": "Property Value",
    "prop-value-desc": "Increase your property value with sustainable infrastructure",
    "did-you-know": "Did You Know?",
    "fact1": "A 1000 sq ft roof can collect ~600 liters per inch of rainfall",
    "fact2": "Rainwater harvesting can recharge groundwater by 40-60%",
    "fact3": "ROI typically achieved within 3-5 years of installation",
    "fact4": "Reduces flood risk and urban heat island effect",
    "your-consent": "Your Consent",
    "consent-data": "I consent to the collection and processing of my location data to provide personalized rainwater harvesting assessments",
    "consent-communication": "I agree to receive updates and recommendations about water conservation initiatives (optional)",
    "consent-terms": `I have read and agree to the <a href="#" class="text-primary hover:underline">Terms of Service</a> and <a href="#" class="text-primary hover:underline">Privacy Policy</a>`,
    "start-assessment": "Start My Assessment",
    "go-back": "Go Back",
    "footer-text": "Supporting sustainable water management across India"
  },
  hi: {
    "main-title": `<span class="text-primary">हाइड्रो</span> हार्वेस्ट`,
    "subtitle": "टिकाऊ जल प्रबंधन के लिए आपका समाधान",
    "join-revolution": `जल <span class="text-primary">क्रांति</span> में शामिल हों`,
    "discover-potential": "अपने स्थान पर वर्षा जल संचयन की क्षमता का पता लगाएं। टिकाऊ जल प्रबंधन की दिशा में अपनी यात्रा शुरू करें और भूजल संरक्षण में योगदान दें।",
    "liters-saved": "लीटर बचाया",
    "happy-users": "खुश उपयोगकर्ता",
    "get-started": "शुरू हो जाओ",
    "user-login": "उपयोगकर्ता लॉगिन",
    "continue-google": "Google के साथ जारी रखें",
    "continue-mobile": "मोबाइल के साथ जारी रखें",
    "admin-login": "एडमिन लॉगिन",
    "admin-login-btn": "एडमिन लॉगिन",
    "enter-mobile": "मोबाइल नंबर दर्ज करें",
    "send-otp": "ओटीपी भेजें",
    "otp-sent-to": "भेजे गए 6-अंकीय कोड दर्ज करें ",
    "verify-continue": "सत्यापित करें और जारी रखें",
    "resend-otp": "पुन: ओटीपी भेजें",
    "terms-agree": `जारी रखकर, आप हमारी <a href="#" class="text-primary hover:underline">सेवा की शर्तों</a> और <a href="#" class="text-primary hover:underline">गोपनीयता नीति</a> से सहमत हैं`,
    "conservation-starts": `जल संरक्षण <span class="text-primary">आपसे</span> शुरू होता है`,
    "every-drop-counts": "आने वाली पीढ़ियों के लिए पानी बचाने के हमारे मिशन में हर बूंद मायने रखती है। जानें कि कैसे वर्षा जल संचयन आपकी संपत्ति को जल-सकारात्मक संपत्ति में बदल सकता है।",
    "env-impact": "पर्यावरणीय प्रभाव",
    "env-impact-desc": "भूजल की कमी को कम करें और पारिस्थितिकी तंत्र की स्थिरता का समर्थन करें",
    "cost-savings": "लागत बचत",
    "cost-savings-desc": "पानी के बिलों में महत्वपूर्ण कमी और दीर्घकालिक वित्तीय लाभ",
    "prop-value": "संपत्ति का मूल्य",
    "prop-value-desc": "टिकाऊ बुनियादी ढांचे के साथ अपनी संपत्ति का मूल्य बढ़ाएं",
    "did-you-know": "क्या आपको पता था?",
    "fact1": "1000 वर्ग फुट की छत प्रति इंच वर्षा में ~600 लीटर पानी एकत्र कर सकती है",
    "fact2": "वर्षा जल संचयन भूजल को 40-60% तक रिचार्ज कर सकता है",
    "fact3": "ROI आमतौर पर स्थापना के 3-5 वर्षों के भीतर प्राप्त होता है",
    "fact4": "बाढ़ के खतरे और शहरी गर्मी द्वीप प्रभाव को कम करता है",
    "your-consent": "आपकी सहमति",
    "consent-data": "मैं व्यक्तिगत वर्षा जल संचयन आकलन प्रदान करने के लिए अपने स्थान डेटा के संग्रह और प्रसंस्करण के लिए सहमति देता हूं",
    "consent-communication": "मैं जल संरक्षण पहलों के बारे में अपडेट और सिफारिशें प्राप्त करने के लिए सहमत हूं (वैकल्पिक)",
    "consent-terms": `मैंने <a href="#" class="text-primary hover:underline">सेवा की शर्तों</a> और <a href="#" class="text-primary hover:underline">गोपनीयता नीति</a> को पढ़ और सहमत हूं`,
    "start-assessment": "मेरा मूल्यांकन शुरू करें",
    "go-back": "वापस जाओ",
    "footer-text": "पूरे भारत में टिकाऊ जल प्रबंधन का समर्थन"
  }
};

function translatePage(language) {
  const langTranslations = translations[language];
  if (!langTranslations) return;

  document.querySelectorAll('[data-translate-key]').forEach(el => {
    const key = el.dataset.translateKey;
    if (langTranslations[key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = langTranslations[key];
      } else {
        el.innerHTML = langTranslations[key];
      }
    }
  });
}

function setLanguage(language) {
  const langSelect = document.getElementById('languageSelect');
  if (langSelect) {
    langSelect.value = language;
  }
  translatePage(language);
  localStorage.setItem('selectedLanguage', language);
}

// Authentication functions
function handleGoogleLogin() {
  console.log('Google login initiated');
  // Simulate login process
  setTimeout(() => {
    showAwarenessSection();
  }, 1000);
}

function showMobileLogin() {
  document.getElementById('mobileLoginForm')?.classList.remove('hidden');
}

function sendOTP() {
  const mobileNumberInput = document.getElementById('mobileNumber');
  if (!mobileNumberInput) return;
  const mobileNumber = mobileNumberInput.value;
  if (mobileNumber.length >= 10) {
    const sentNumberEl = document.getElementById('sentNumber');
    if (sentNumberEl) sentNumberEl.textContent = mobileNumber;
    document.getElementById('mobileLoginForm')?.classList.add('hidden');
    document.getElementById('otpVerification')?.classList.remove('hidden');
  } else {
    alert('Please enter a valid mobile number');
  }
}

function moveToNext(current, index) {
  if (current.value.length >= 1 && index < 5) {
    current.nextElementSibling?.focus();
  }
}

function verifyOTP() {
  const otpInputs = document.querySelectorAll('#otpVerification input[type="text"]');
  const otp = Array.from(otpInputs).map(input => input.value).join('');
  
  if (otp.length === 6) {
    console.log('OTP verified:', otp);
    showAwarenessSection();
  } else {
    alert('Please enter complete OTP');
  }
}

function proceedAsGuest() {
  console.log('Proceeding as guest');
  showAwarenessSection();
}

function showAwarenessSection() {
  document.getElementById('loginSection')?.classList.remove('active');
  document.getElementById('awarenessSection')?.classList.add('active');
  document.getElementById('step2')?.classList.add('active');
}

function goBack() {
  document.getElementById('awarenessSection')?.classList.remove('active');
  document.getElementById('loginSection')?.classList.add('active');
  document.getElementById('step2')?.classList.remove('active');
}

// Consent validation
function validateConsent() {
  const dataConsent = document.getElementById('dataConsent');
  const termsConsent = document.getElementById('termsConsent');
  const proceedBtn = document.getElementById('proceedBtn');
  if (!dataConsent || !termsConsent || !proceedBtn) return;
  
  if (dataConsent.checked && termsConsent.checked) {
    proceedBtn.classList.remove('opacity-50', 'pointer-events-none');
  } else {
    proceedBtn.classList.add('opacity-50', 'pointer-events-none');
  }
}

// Initialize page when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  createParticles();
  addRippleEffect();
  
  // Add consent validation listeners
  document.getElementById('dataConsent')?.addEventListener('change', validateConsent);
  document.getElementById('termsConsent')?.addEventListener('change', validateConsent);
  
  // Initialize proceed button state
  validateConsent();

  // Add language selector event listener
  document.getElementById('languageSelect')?.addEventListener('change', function() {
    setLanguage(this.value);
  });

  // Set language on initial load
  const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
  setLanguage(savedLanguage);
});
