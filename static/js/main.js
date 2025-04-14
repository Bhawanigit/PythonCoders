document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Handle the "Mark as completed" button
    const completeBtn = document.getElementById('mark-complete-btn');
    if (completeBtn) {
        completeBtn.addEventListener('click', function() {
            const form = document.getElementById('complete-form');
            if (form) {
                form.submit();
            }
        });
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Handle the navigation tabs in lessons
    const lessonTabs = document.querySelectorAll('.lesson-tab');
    if (lessonTabs.length > 0) {
        lessonTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                lessonTabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show the corresponding content
                const target = this.getAttribute('data-target');
                document.querySelectorAll('.lesson-content').forEach(content => {
                    content.style.display = 'none';
                });
                document.getElementById(target).style.display = 'block';
            });
        });
        
        // Activate the first tab by default
        lessonTabs[0].click();
    }
});

// Function to copy code examples to clipboard
function copyCode(button) {
    const codeBlock = button.parentElement.nextElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        // Change button text temporarily
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}
