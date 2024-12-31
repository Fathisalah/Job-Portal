// Add any JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Example: Add confirmation for job applications
    const applyButtons = document.querySelectorAll('.apply-job-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to apply for this job?')) {
                e.preventDefault();
            }
        });
    });
}); 