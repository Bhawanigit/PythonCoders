# Converting to a Static Site for GitHub Pages

Since GitHub Pages only supports static websites, you would need to convert your dynamic Flask application into a static site to host it there. Here's how you can approach this:

## Option 1: Create a Project Landing Page

1. Create a `docs` folder in your repository
2. Create a static HTML version of your landing page inside this folder
3. Include screenshots, feature lists, and documentation
4. Enable GitHub Pages in your repository settings to serve from the `docs` folder

## Option 2: Use a Static Site Generator

You can use a tool like [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/) to convert your Flask application into a static site:

1. Install Frozen-Flask:
   ```
   pip install Frozen-Flask
   ```

2. Create a script to generate static files (e.g., `freeze.py`):
   ```python
   from flask_frozen import Freezer
   from app import app
   
   freezer = Freezer(app)
   
   if __name__ == '__main__':
       freezer.freeze()
   ```

3. Run the script to generate static files:
   ```
   python freeze.py
   ```

4. This will create a `build` directory with static HTML files
5. Copy these files to your `docs` folder
6. Enable GitHub Pages in your repository settings

## Limitations of a Static Site

Converting your Flask application to a static site will have these limitations:

1. **No User Authentication**: The login/register functionality won't work
2. **No Database**: User progress tracking won't work
3. **No Code Execution**: The interactive code editor won't work
4. **No Dynamic Content**: All pages must be pre-generated

## Alternative: Create a Project Website + Deploy the Full App Elsewhere

The best approach might be to:

1. Use GitHub Pages to host a project website that showcases your application
2. Deploy the actual Flask application on a platform that supports Python web apps
3. Link from your GitHub Pages site to your deployed application

## Creating a Simple Landing Page

Here's a simple HTML template you could use for a GitHub Pages landing page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Learning Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        .hero {
            background-color: #343a40;
            color: white;
            padding: 100px 0;
            margin-bottom: 40px;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #0d6efd;
        }
        .feature-card {
            border: none;
            transition: transform 0.3s;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-10px);
        }
        .cta-section {
            background-color: #e9ecef;
            padding: 80px 0;
            margin: 60px 0;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">Python Learning Platform</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#features">Features</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#screenshots">Screenshots</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#get-started">Get Started</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/yourusername/PythonLearningPlatform">GitHub</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <section class="hero text-center">
        <div class="container">
            <h1 class="display-4 fw-bold mb-4">Learn Python Programming</h1>
            <p class="lead mb-5">An interactive web application for learning Python programming, built with Flask and PostgreSQL.</p>
            <a href="https://your-deployed-app-url.com" class="btn btn-primary btn-lg">Try The App</a>
            <a href="https://github.com/yourusername/PythonLearningPlatform" class="btn btn-outline-light btn-lg ms-3">View on GitHub</a>
        </div>
    </section>

    <section class="container mb-5" id="features">
        <h2 class="text-center mb-5">Features</h2>
        <div class="row g-4">
            <div class="col-md-3">
                <div class="card feature-card shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">📚</div>
                        <h5 class="card-title">Interactive Lessons</h5>
                        <p class="card-text">Structured content on Python fundamentals with examples and explanations.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card feature-card shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">💻</div>
                        <h5 class="card-title">Live Code Editor</h5>
                        <p class="card-text">Practice Python code directly in your browser with instant feedback.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card feature-card shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">🔍</div>
                        <h5 class="card-title">Progress Tracking</h5>
                        <p class="card-text">Monitor your learning journey with completed lesson tracking.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card feature-card shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">🧪</div>
                        <h5 class="card-title">Practice Exercises</h5>
                        <p class="card-text">Reinforce learning with hands-on coding exercises and challenges.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="container mb-5" id="screenshots">
        <h2 class="text-center mb-5">Screenshots</h2>
        <div class="row">
            <div class="col-md-6 mb-4">
                <img src="screenshot1.png" alt="Homepage" class="img-fluid rounded shadow">
            </div>
            <div class="col-md-6 mb-4">
                <img src="screenshot2.png" alt="Lesson Page" class="img-fluid rounded shadow">
            </div>
            <div class="col-md-6 mb-4">
                <img src="screenshot3.png" alt="Code Editor" class="img-fluid rounded shadow">
            </div>
            <div class="col-md-6 mb-4">
                <img src="screenshot4.png" alt="Profile Page" class="img-fluid rounded shadow">
            </div>
        </div>
    </section>

    <section class="cta-section" id="get-started">
        <div class="container text-center">
            <h2 class="mb-4">Ready to start learning Python?</h2>
            <p class="lead mb-4">Check out the full application or explore the code on GitHub.</p>
            <a href="https://your-deployed-app-url.com" class="btn btn-primary btn-lg me-3">Try The App</a>
            <a href="https://github.com/yourusername/PythonLearningPlatform" class="btn btn-dark btn-lg">View Code</a>
        </div>
    </section>

    <footer class="bg-dark text-white py-4">
        <div class="container text-center">
            <p>Python Learning Platform - Created by Your Name</p>
            <p>
                <a href="https://github.com/yourusername" class="text-white me-3">GitHub</a>
                <a href="https://your-portfolio.com" class="text-white me-3">Portfolio</a>
                <a href="mailto:your-email@example.com" class="text-white">Contact</a>
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

Replace placeholder URLs, usernames, and add screenshots to make this page yours.