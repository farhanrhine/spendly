# JavaScript Basics

## What is JavaScript?
JavaScript makes your HTML page interactive.
HTML = structure. CSS = appearance. JS = behaviour.

---

## How to Link JS to HTML

```javascript
<script src="static/js/main.js"></script>   → put this at the bottom of <body>

→ always at the bottom. so HTML loads first before JS runs.
```

---

## Where to Write JS

```javascript
→ in a separate file: static/js/main.js
→ or inside <script> tags directly in HTML (for quick testing only)
```

---

## Variables

```javascript
let name = "Farhan";        → can be changed later
const age = 25;             → cannot be changed. use this by default.
var x = 10;                 → old way. avoid it.
```

---

## Data Types

```javascript
let name = "Farhan";        → string (text)
let age = 25;               → number
let isLoggedIn = true;      → boolean (true or false)
let nothing = null;         → empty on purpose
let notDefined;             → undefined. no value assigned yet.
let items = [1, 2, 3];      → array (list)
let user = {name: "Alex"};  → object (key-value pairs, like Python dict)
```

---

## console.log — your best friend

```javascript
console.log("hello");           → prints to browser console
console.log(name);              → prints the value of name
console.log("Name:", name);     → prints: Name: Farhan

→ open browser console: right click → inspect → Console tab
```

---

## Functions

```javascript
function greet() {              → define a function
    console.log("Hello");
}
greet();                        → call it

function add(a, b) {            → with parameters
    return a + b;               → returns a value
}
let result = add(2, 3);         → result = 5

→ arrow function (modern way, same thing):
const add = (a, b) => a + b;
```

---

## If / Else

```javascript
if (age > 18) {
    console.log("Adult");
} else if (age === 18) {
    console.log("Just 18");
} else {
    console.log("Minor");
}

=== → strict equal (checks value AND type). always use this, not ==
```

---

## Loops

```javascript
for (let i = 0; i < 5; i++) {     → runs 5 times
    console.log(i);               → prints 0 1 2 3 4
}

let items = ["a", "b", "c"];
for (let item of items) {         → loop over an array
    console.log(item);
}

items.forEach(item => {           → modern way to loop over array
    console.log(item);
});
```

---

## Arrays

```javascript
let items = ["apple", "banana", "mango"];

items[0]                 → "apple". index starts at 0
items.length             → 3
items.push("grape")      → adds to end
items.pop()              → removes from end
items.includes("apple")  → true or false
```

---

## Objects

```javascript
let user = {
    name: "Farhan",
    age: 25,
    isLoggedIn: true
};

user.name                → "Farhan"
user["name"]             → same thing
user.age = 26            → update a value
user.email = "f@f.com"   → add a new key
```

---

## DOM — selecting HTML elements

```javascript
DOM = Document Object Model. JS uses it to read and change HTML.

document.getElementById("navbar")         → select by id
document.querySelector(".card")           → select first element with class card
document.querySelectorAll(".card")         → select ALL elements with class card
```

---

## DOM — changing HTML

```javascript
let el = document.querySelector("h1");

el.textContent = "New Heading";       → changes the text
el.style.color = "red";              → changes CSS style
el.classList.add("active");          → adds a CSS class
el.classList.remove("active");       → removes a CSS class
el.classList.toggle("active");       → adds if not there, removes if there
```

---

## Events — reacting to user actions

```javascript
let btn = document.querySelector("button");

btn.addEventListener("click", function() {   → runs when button is clicked
    console.log("clicked");
});

→ common events:
"click"        → mouse click
"submit"       → form submitted
"input"        → user types in an input
"change"       → value changed
"mouseover"    → mouse hovers over element
```

---

## Reading Input Values

```javascript
let input = document.querySelector("input");
let value = input.value;             → gets what the user typed
```

---

## fetch — sending data to Flask without reloading page

```javascript
fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "f@f.com", password: "123" })
})
.then(response => response.json())   → parse response as JSON
.then(data => console.log(data))     → use the data
.catch(error => console.log(error)); → handle errors

→ you will use this later when you want to submit forms without page refresh
```

---

## JSON

```javascript
JSON.stringify({ name: "Farhan" })   → converts object to string → sends to server
JSON.parse('{"name":"Farhan"}')      → converts string back to object → use in JS
```

---

## Key Rules
- always use const by default. use let only if the value will change.
- always use === not ==
- JS is case sensitive. name and Name are different.
- always put <script> at the bottom of <body>
- console.log() is your debugging tool. use it constantly.
- one mistake (missing bracket, wrong spelling) breaks everything. check the console.