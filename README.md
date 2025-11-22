# Daniel Feller - Portfolio Site

Personal portfolio site built with Jekyll, based on the Gradfolio theme with a dark color scheme.

## Sections

- **About** - Overview of expertise and background
- **Projects** - Code projects and technical work
- **Research** - Published papers with PDF links
- **Book** - Information about healthcare data standards book
- **Contact** - Ways to get in touch

## Quick Start

### Deploy to GitHub Pages

1. **Create a new repository:**
   - Go to GitHub and create a new repo named `yourusername.github.io`
   - Make it public

2. **Push these files:**
   ```bash
   cd gradfolio-site
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: Deploy from branch
   - Branch: main, folder: / (root)
   - Save

4. **Your site will be live at:**
   - `https://yourusername.github.io`

## Local Development

### Prerequisites
- Ruby (2.7+)
- Bundler

### Setup
```bash
cd gradfolio-site
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000`

## Customization

### Essential Updates

1. **_config.yml:**
   - Update `title`, `description`, `url`
   - Add your email, GitHub username, LinkedIn username

2. **All pages:**
   - Replace `your.email@example.com` with your email
   - Replace `yourusername` with your GitHub username
   - Replace `yourprofile` with your LinkedIn username
   - Update project GitHub links

3. **Content:**
   - Customize the About section in `index.md`
   - Update project descriptions in `projects.md`
   - Verify publication list in `research.md`
   - Edit book details in `book.md`

### Adding PDFs

Create a `pdfs` folder and add your publication PDFs with these names:
- `feller_amia_2018_sdoh.pdf`
- `feller_jamia_visual_analytics.pdf`
- `feller_jaids_2018_nlp_risk.pdf`
- (etc.)

### Color Customization

Edit `assets/css/main.css` and modify the `:root` variables:

```css
:root {
  --bg-color: #0d1117;          /* Main background */
  --bg-secondary: #161b22;      /* Card backgrounds */
  --text-color: #c9d1d9;        /* Main text */
  --text-secondary: #8b949e;    /* Secondary text */
  --accent-color: #58a6ff;      /* Links, highlights */
  --accent-hover: #79c0ff;      /* Link hover */
  --border-color: #30363d;      /* Borders */
}
```

## Structure

```
.
├── _config.yml           # Site configuration
├── _layouts/
│   └── default.html      # Main layout template
├── assets/
│   └── css/
│       └── main.css      # Dark theme styles
├── pdfs/                 # Publication PDFs (create this)
├── index.md              # About page
├── projects.md           # Projects page
├── research.md           # Research publications
├── book.md               # Book information
├── contact.md            # Contact page
├── Gemfile               # Ruby dependencies
└── README.md             # This file
```

## Features

- Dark theme optimized for developers
- Fully responsive design
- Clean, minimal aesthetic
- Fast loading
- GitHub Pages compatible
- No JavaScript required
- SEO optimized

## Tips

- Keep the dark theme - it signals technical competence
- Update projects as you complete them
- Keep contact info current
- Link from LinkedIn to drive traffic

## Support

For Jekyll questions: https://jekyllrb.com/docs/
For GitHub Pages: https://docs.github.com/en/pages

## License

Based on Gradfolio theme (MIT License)
