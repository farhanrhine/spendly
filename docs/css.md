# CSS Basics

## What is CSS?
CSS tells the browser how HTML elements should look.
It has 3 parts: selector + property + value.

```css
selector {
  property: value;
}
```

Example:

```css
h1 {
  color: blue;
  font-size: 32px;
}
```

→ every h1 on the page becomes blue and 32px.

---

## How to Link CSS to HTML

```css
<link rel="stylesheet" href="style.css">   → put this inside <head>
```

---

## Selectors — how to target elements

```css
h1 { }            → targets every <h1> tag
p { }             → targets every <p> tag
.card { }         → targets every element with class="card"
#navbar { }       → targets the one element with id="navbar"
* { }             → targets every single element on the page
```

---

## The Box Model
Every element is a box. From inside to outside:

```css
content           → the actual text or image
padding           → space between content and border (inside the box)
border            → the line around the box
margin            → space outside the box (pushes other elements away)

div {
  padding: 20px;               → space inside
  margin: 20px;                → space outside
  border: 1px solid black;     → line around it
}
```

---

## Common Properties

### Text
```css
color: red;                  → text color
font-size: 16px;             → text size
font-weight: bold;           → makes text bold
font-family: Arial;          → font style
text-align: center;          → align text left, center, right
line-height: 1.5;            → space between lines
```

### Background
```css
background-color: #f5f5f5;   → background color
background: white;           → same thing, shorthand
```

### Sizing
```css
width: 400px;                → fixed width
height: 200px;               → fixed height
max-width: 100%;             → never wider than the screen
min-height: 100vh;           → at least full screen height
```

### Spacing
```css
padding: 20px;               → all 4 sides
padding: 10px 20px;          → top/bottom 10px, left/right 20px
margin: 20px;                → all 4 sides
margin: 0 auto;              → center a block element horizontally
```

### Border
```css
border: 1px solid #ddd;      → width, style, color
border-radius: 8px;          → rounds the corners
border-radius: 50%;          → makes it a circle
```

### Box Sizing
```css
box-sizing: border-box;      → prevents padding and border from increasing the element's width and height
```

### Display
```css
display: block;              → takes full width, starts on new line
display: inline;             → sits in line with text, no width/height
display: flex;               → enables flexbox layout
display: none;               → hides the element completely
```

### Cursor
```css
cursor: pointer;             → hand icon on hover. always add to buttons.
```

---

## Flexbox — for layout

```css
.container {
  display: flex;             → turns on flexbox
  justify-content: center;   → horizontal alignment
  align-items: center;       → vertical alignment
  gap: 16px;                 → space between children
  flex-direction: row;       → children side by side (default)
  flex-direction: column;    → children stacked top to bottom
}
```

### justify-content values
```css
flex-start     → push everything to the left
flex-end       → push everything to the right
center         → center everything
space-between  → first item left, last item right, rest spread evenly
space-around   → equal space around each item
```

### align-items values
```css
flex-start     → push everything to the top
flex-end       → push everything to the bottom
center         → center everything vertically
```

---

## Pseudo-classes — style on interaction

```css
button:hover {
  background: darkblue;      → changes style when mouse hovers
}

input:focus {
  border: 2px solid blue;    → changes style when user clicks into input
}
```

---

## Units

```css
px     → fixed pixels. e.g. 16px
%      → relative to parent. e.g. width: 50% = half of parent
vh     → viewport height. 100vh = full screen height
vw     → viewport width. 100vw = full screen width
rem    → relative to root font size. 1rem = 16px by default
```

---

## Colors

```css
color: red;                  → color name
color: #ff0000;              → hex code
color: rgb(255, 0, 0);       → rgb value
color: rgba(255, 0, 0, 0.5); → rgb + opacity. 0 = invisible, 1 = solid
```

---

## Key Rules
- CSS reads top to bottom. lower rules override upper ones.
- More specific selector wins. #id beats .class beats tag.
- Always use class for styling. avoid id for CSS.
- `box-sizing: border-box` makes padding not add to width. Always set this.