document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror editor if element exists
    const editorElement = document.getElementById('code-editor');
    if (editorElement) {
        const editor = CodeMirror.fromTextArea(editorElement, {
            lineNumbers: true,
            mode: 'python',
            theme: 'dracula',
            indentUnit: 4,
            lineWrapping: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            extraKeys: {
                "Tab": function(cm) {
                    cm.replaceSelection("    ", "end");
                }
            }
        });
        
        // Set editor height
        editor.setSize(null, 300);
        
        // Run code button
        const runButton = document.getElementById('run-code');
        if (runButton) {
            runButton.addEventListener('click', function() {
                executeCode(editor);
            });
        }
        
        // Verify exercise button
        const verifyButton = document.getElementById('verify-exercise');
        if (verifyButton) {
            verifyButton.addEventListener('click', function() {
                verifyExercise(editor);
            });
        }
        
        // Reset code button
        const resetButton = document.getElementById('reset-code');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                resetCode(editor);
            });
        }
    }
});

function executeCode(editor) {
    const code = editor.getValue();
    const outputElement = document.getElementById('code-output');
    
    if (outputElement) {
        // Show loading spinner
        outputElement.innerHTML = '<div class="text-center"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Send code to server for execution
        const form = new FormData();
        form.append('code', code);
        
        fetch('/execute_code', {
            method: 'POST',
            body: form
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                outputElement.innerHTML = `<pre class="text-success">${escapeHtml(data.output) || "Program executed successfully with no output."}</pre>`;
            } else {
                outputElement.innerHTML = `<pre class="text-danger">${escapeHtml(data.error)}</pre>`;
            }
        })
        .catch(error => {
            outputElement.innerHTML = `<pre class="text-danger">Error: ${escapeHtml(error.toString())}</pre>`;
        });
    }
}

function verifyExercise(editor) {
    const code = editor.getValue();
    const lessonId = document.getElementById('lesson-id').value;
    const exerciseId = document.getElementById('exercise-id').value;
    const outputElement = document.getElementById('code-output');
    
    if (outputElement) {
        // Show loading spinner
        outputElement.innerHTML = '<div class="text-center"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Send code to server for verification
        const form = new FormData();
        form.append('code', code);
        form.append('lesson_id', lessonId);
        form.append('exercise_id', exerciseId);
        
        fetch('/verify_exercise', {
            method: 'POST',
            body: form
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                outputElement.innerHTML = `
                    <div class="alert alert-success" role="alert">
                        <h4 class="alert-heading">Well done!</h4>
                        <p>${data.message}</p>
                        <hr>
                        <pre>${escapeHtml(data.output) || "Program executed successfully with no output."}</pre>
                    </div>`;
                
                // Show next button if available
                const nextBtn = document.getElementById('next-exercise-btn');
                if (nextBtn) {
                    nextBtn.classList.remove('d-none');
                }
            } else {
                outputElement.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <h4 class="alert-heading">Not quite right!</h4>
                        <p>Your code didn't pass the test. Try again!</p>
                        <hr>
                        <pre>${escapeHtml(data.error)}</pre>
                    </div>`;
            }
        })
        .catch(error => {
            outputElement.innerHTML = `<pre class="text-danger">Error: ${escapeHtml(error.toString())}</pre>`;
        });
    }
}

function resetCode(editor) {
    const startingCode = document.getElementById('starting-code').value;
    editor.setValue(startingCode);
}

// Helper function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
