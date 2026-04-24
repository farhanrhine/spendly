// main.js — students will add JavaScript here as features are built

// Settings Menu Functionality
document.addEventListener('DOMContentLoaded', function() {
    const settingsBtn = document.getElementById('settings-btn');
    const settingsDropdown = document.getElementById('settings-dropdown');
    
    // Toggle settings dropdown
    if (settingsBtn) {
        settingsBtn.addEventListener('click', function() {
            settingsDropdown.classList.toggle('active');
        });
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.settings-menu')) {
            settingsDropdown.classList.remove('active');
        }
    });
});

// Theme Management (for initial page load)
document.addEventListener('DOMContentLoaded', function() {
    const htmlElement = document.documentElement;
    
    // Get saved theme preference or detect system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = savedTheme ? savedTheme === 'dark' : systemPrefersDark;
    
    // Set initial theme
    htmlElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
});

// Video Modal Functionality
document.addEventListener('DOMContentLoaded', function() {
    const videoTrigger = document.getElementById('video-trigger');
    const videoModal = document.getElementById('video-modal');
    const modalClose = document.getElementById('modal-close');
    const modalOverlay = document.querySelector('.video-modal-overlay');
    const videoFrame = document.getElementById('video-frame');

    // Open modal when clicking "See how it works"
    if (videoTrigger) {
        videoTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            videoModal.classList.add('active');
        });
    }

    // Close modal when clicking close button
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            closeVideoModal();
        });
    }

    // Close modal when clicking outside (on overlay)
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function() {
            closeVideoModal();
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && videoModal.classList.contains('active')) {
            closeVideoModal();
        }
    });

    // Function to close modal and stop video
    function closeVideoModal() {
        videoModal.classList.remove('active');
        
        // Stop video by resetting src temporarily
        const currentSrc = videoFrame.src;
        videoFrame.src = '';
        videoFrame.src = currentSrc;
    }
});

// Initialize Lucide Icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
