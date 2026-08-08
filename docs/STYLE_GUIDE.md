# Visual style guide

Reference images: `design/mockups/`.

## Palette
- Canvas: `#f5f6f7`
- Cards: `#ffffff`
- Text: `#202326`
- Muted text: `#687078`
- Border: `#d9dde2`
- Primary accent: `#e6533f`
- Accent dark: `#c94332`
- Success: `#2f8f68`
- Information: `#3576a8`

## Typography
Use system sans-serif only (`Inter`-like fallback without downloading fonts):
`-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`.

## Layout
- Dark header + light application body.
- Left control rail around 280–320 px on desktop.
- Main content uses cards with subtle 1 px borders and 8–12 px radius.
- Favor whitespace and large charts over dense tables.
- Presentation mode enlarges graph labels and collapses secondary controls.

## 3D terrain
- Terrain is the visual hero of Layer 2.
- Use Plotly `go.Surface` plus projected contours.
- Do not overdecorate; axes should teach weights and error.
- Always show the simplex-slice disclaimer.
