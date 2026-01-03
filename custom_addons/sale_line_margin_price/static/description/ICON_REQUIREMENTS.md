# App Icon Requirements for Odoo Apps Marketplace

## Required Files

### 1. Module Icon (MANDATORY)
- **File name:** `icon.png`
- **Location:** `static/description/icon.png`
- **Dimensions:** 256×256 pixels (square)
- **Format:** PNG with transparency support
- **File size:** < 100 KB (recommended < 50 KB)
- **Background:** Preferably transparent or white

### 2. Banner Image (RECOMMENDED)
- **File name:** `banner.png`
- **Location:** `static/description/banner.png`
- **Dimensions:** 560×280 pixels (2:1 ratio)
- **Format:** PNG or JPG
- **File size:** < 200 KB
- **Content:** Feature highlight or product screenshot

### 3. Screenshots (RECOMMENDED)
- **File names:** `screenshot_1.png`, `screenshot_2.png`, etc.
- **Location:** `static/description/`
- **Dimensions:** 1920×1080 pixels recommended (16:9 ratio)
- **Format:** PNG or JPG
- **File size:** < 1 MB each
- **Quantity:** 2-5 screenshots showing key features

## Icon Design Guidelines

### DO:
✅ Use simple, recognizable symbols related to sales/pricing/margin
✅ Use high contrast colors that work on both light and dark backgrounds
✅ Center the main icon element with adequate padding (20-30px from edges)
✅ Use Odoo's color palette when possible (#875A7B purple is recommended)
✅ Make it distinctive and professional
✅ Test visibility at small sizes (64×64, 128×128)

### DON'T:
❌ Use text or small details (won't be readable at small sizes)
❌ Use gradients that don't scale well
❌ Use copyrighted or trademarked symbols
❌ Use low resolution or pixelated images
❌ Use very dark backgrounds (hard to see in dark mode)

## Design Concept Suggestions for "Sale Line Margin Pricing"

1. **Calculator + Percentage Symbol**
   - Simple calculator icon with % symbol overlay
   - Colors: Purple (#875A7B) and white/gray

2. **Price Tag with Margin**
   - Price tag shape with % symbol inside
   - Clean, minimalist design

3. **Graph/Chart with Upward Trend**
   - Bar chart or line graph showing profit margin
   - Suggests increasing profits

4. **Dollar Sign + Percentage**
   - Combined $ and % symbols
   - Represents cost-plus pricing

## Tools for Creating Icons

- **Online:** Canva, Figma, Adobe Express
- **Desktop:** GIMP (free), Adobe Photoshop, Illustrator
- **Icon Libraries:** Font Awesome, Material Icons (ensure license compliance)

## Quick Creation Steps

1. Create a 256×256px canvas with transparent background
2. Design your icon centered with 30px padding
3. Use vector graphics or high-res images
4. Export as PNG with transparency
5. Optimize file size using tools like TinyPNG or ImageOptim
6. Test at multiple sizes (256px, 128px, 64px)

## Verification Checklist

Before uploading:
- [ ] Icon is exactly 256×256 pixels
- [ ] File is named `icon.png`
- [ ] Background is transparent or white
- [ ] File size is under 100 KB
- [ ] Icon is readable at 64×64 pixels
- [ ] Colors have good contrast
- [ ] No copyright violations
- [ ] Professional appearance

## Example File Structure

```
sale_line_margin_price/
└── static/
    └── description/
        ├── icon.png              (256×256, <100KB)
        ├── banner.png            (560×280, optional)
        ├── screenshot_1.png      (feature demo)
        ├── screenshot_2.png      (configuration view)
        └── index.html            (app description)
```

## Marketplace Review Notes

- Odoo Apps reviewers will check icon quality
- Poor quality icons may result in rejection
- Icons should reflect the module's functionality
- Consistency with Odoo's design language is appreciated
- Professional appearance is critical for marketplace approval
