# Placeholder Images

These are default placeholder images used when Unsplash API doesn't return results.

- placeholder-tech.jpg: Technology category
- placeholder-business.jpg: Business category
- placeholder-lifestyle.jpg: Lifestyle category

Replace these with actual images or create them using:
```bash
# Example: Create colored placeholder (requires ImageMagick)
convert -size 1200x630 -background "#4A5568" -fill white -pointsize 72 -gravity center label:"Tech" placeholder-tech.jpg
```
