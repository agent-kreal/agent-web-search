# scenario: docs-js

## U1: https://react.dev/learn
_(note: Next.js доки)_

**[local-auto]** (0.92s, 16542 chars, tier http; wr=1.0, wo=0.0; hdr 5, code 10, links 3, lists 6)
```
---
title: Quick Start – React
url: https://react.dev/learn
hostname: react.dev
description: The library for web and native user interfaces
sitename: Reactjs
---
Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

- How to create and nest components
- How to add markup and styles
- How to display data
- How to render conditions and lists
- How to respond to events and update the screen
- How to share data between components

## Creating and nesting components 

React apps are made out of *components*. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```
Now that you’ve declared `MyButton`, you can nest it into another component:

```
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```
Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) and

[…середина…]

istItems = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'darkgreen'
      }}
    >
      {product.title}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}

## Responding to events 

You can respond to events by declaring *event handler* functions inside your components:

```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }
  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```
Notice how `onClick={handleClick}` has no parentheses at the end! Do not *call* the event handler function: you only need to *pass it down*. React will call your event handler when the user clicks the button.

## Updating the screen 

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add *state* to your component.

First, import [`useState`](https://react.dev/reference/react/useState) from React:

`import { useState } from 'react';`
Now you can declare a *state variable* inside your component:

```
function MyButton() {
  const [count, setCount] = us
```

**[local-http]** (0.91s, 16542 chars, tier http; wr=1.0, wo=0.0; hdr 5, code 10, links 3, lists 6)
```
---
title: Quick Start – React
url: https://react.dev/learn
hostname: react.dev
description: The library for web and native user interfaces
sitename: Reactjs
---
Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

- How to create and nest components
- How to add markup and styles
- How to display data
- How to render conditions and lists
- How to respond to events and update the screen
- How to share data between components

## Creating and nesting components 

React apps are made out of *components*. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```
Now that you’ve declared `MyButton`, you can nest it into another component:

```
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```
Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) and

[…середина…]

istItems = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'darkgreen'
      }}
    >
      {product.title}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}

## Responding to events 

You can respond to events by declaring *event handler* functions inside your components:

```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }
  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```
Notice how `onClick={handleClick}` has no parentheses at the end! Do not *call* the event handler function: you only need to *pass it down*. React will call your event handler when the user clicks the button.

## Updating the screen 

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add *state* to your component.

First, import [`useState`](https://react.dev/reference/react/useState) from React:

`import { useState } from 'react';`
Now you can declare a *state variable* inside your component:

```
function MyButton() {
  const [count, setCount] = us
```

**[local-curl]** (3.37s, 16542 chars, tier curl; wr=1.0, wo=0.0; hdr 5, code 10, links 3, lists 6)
```
---
title: Quick Start – React
url: https://react.dev/learn
hostname: react.dev
description: The library for web and native user interfaces
sitename: Reactjs
---
Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

- How to create and nest components
- How to add markup and styles
- How to display data
- How to render conditions and lists
- How to respond to events and update the screen
- How to share data between components

## Creating and nesting components 

React apps are made out of *components*. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```
Now that you’ve declared `MyButton`, you can nest it into another component:

```
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```
Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) and

[…середина…]

istItems = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'darkgreen'
      }}
    >
      {product.title}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}

## Responding to events 

You can respond to events by declaring *event handler* functions inside your components:

```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }
  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```
Notice how `onClick={handleClick}` has no parentheses at the end! Do not *call* the event handler function: you only need to *pass it down*. React will call your event handler when the user clicks the button.

## Updating the screen 

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add *state* to your component.

First, import [`useState`](https://react.dev/reference/react/useState) from React:

`import { useState } from 'react';`
Now you can declare a *state variable* inside your component:

```
function MyButton() {
  const [count, setCount] = us
```

**[local-browser]** (4.94s, 16542 chars, tier browser; wr=1.0, wo=0.0; hdr 5, code 10, links 3, lists 6)
```
---
title: Quick Start – React
url: https://react.dev/learn
hostname: react.dev
description: The library for web and native user interfaces
sitename: Reactjs
---
Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

- How to create and nest components
- How to add markup and styles
- How to display data
- How to render conditions and lists
- How to respond to events and update the screen
- How to share data between components

## Creating and nesting components 

React apps are made out of *components*. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```
Now that you’ve declared `MyButton`, you can nest it into another component:

```
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```
Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}
export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) and

[…середина…]

istItems = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'darkgreen'
      }}
    >
      {product.title}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}

## Responding to events 

You can respond to events by declaring *event handler* functions inside your components:

```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }
  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```
Notice how `onClick={handleClick}` has no parentheses at the end! Do not *call* the event handler function: you only need to *pass it down*. React will call your event handler when the user clicks the button.

## Updating the screen 

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add *state* to your component.

First, import [`useState`](https://react.dev/reference/react/useState) from React:

`import { useState } from 'react';`
Now you can declare a *state variable* inside your component:

```
function MyButton() {
  const [count, setCount] = us
```

**[firecrawl]** (1.17s, 18718 chars; wr=1.0, wo=0.0; hdr 6, code 11, links 7, lists 9)
```
[Learn React](https://react.dev/learn)

Copy pageCopy

# Quick Start [Link for this heading](https://react.dev/learn\#undefined "Link for this heading")

Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

- How to create and nest components
- How to add markup and styles
- How to display data
- How to render conditions and lists
- How to respond to events and update the screen
- How to share data between components

## Creating and nesting components [Link for Creating and nesting components ](https://react.dev/learn\#components "Link for Creating and nesting components ")

React apps are made out of _components_. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```
function MyButton() {

  return (

    <button>I'm a button</button>

  );

}
```

Now that you’ve declared `MyButton`, you can nest it into another component:

```
export default function MyApp() {

  return (

    <div>

      <h1>Welcome to my app</h1>

      <MyButton />

    </div>

  );

}
```

Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

App.js

App.js

DownloadReloadClearFork

99

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

functionMyButton(){

return(

<button>

I'm a button

</button>

);

}

exportdefaultfunctionMyApp(){

return(

<div>

<h1>Welcome to my app</h1>

<MyButton/>

</div>

);

}

Sandpack Preview

# Welcome t

[…середина…]

rtdefaultfunctionShoppingList(){

constlistItems = products.map(product=>

<li

key={product.id}

style={{

color:product.isFruit ? 'magenta' : 'darkgreen'

}}

>

{product.title}

</li>

);

return(

<ul>{listItems}</ul>

);

}

Sandpack Preview

- Cabbage
- Garlic
- Apple

Show more

## Responding to events [Link for Responding to events ](https://react.dev/learn\#responding-to-events "Link for Responding to events ")

You can respond to events by declaring _event handler_ functions inside your components:

```
function MyButton() {

  function handleClick() {

    alert('You clicked me!');

  }

  return (

    <button onClick={handleClick}>

      Click me

    </button>

  );

}
```

Notice how `onClick={handleClick}` has no parentheses at the end! Do not _call_ the event handler function: you only need to _pass it down_. React will call your event handler when the user clicks the button.

## Updating the screen [Link for Updating the screen ](https://react.dev/learn\#updating-the-screen "Link for Updating the screen ")

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked.
```

**[tavily]** (0.83s, 17448 chars; wr=1.0, wo=0.0; hdr 6, code 15, links 6, lists 6)
```
[Learn React](/learn)

# Quick Start

Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

* How to create and nest components
* How to add markup and styles
* How to display data
* How to render conditions and lists
* How to respond to events and update the screen
* How to share data between components

## Creating and nesting components

React apps are made out of *components*. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

```


function MyButton() {



return (



<button>I'm a buttonbutton>



);



}


```

Now that you’ve declared `MyButton`, you can nest it into another component:

```


export default function MyApp() {



return (



<div>



<h1>Welcome to my apph1>



<MyButton />



div>



);



}


```

Notice that  starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app "Open in CodeSandbox")

```
function MyButton(){return(< button>button> ); } export default function MyApp() { return ( <div> <h1>Welcome to my apph1> <MyButton /> div> ); } button>);} export default function MyApp(){return(< div>< h1>h1> <MyButton /> div> ); } h1>< MyButton/>div> ); } div>);}
```

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/

[…середина…]

s}ul> ); } ul>);}
```

## Responding to events

You can respond to events by declaring *event handler* functions inside your components:

```


function MyButton() {



function handleClick() {



alert('You clicked me!');



}



return (



<button onClick={handleClick}>



Click me



button>



);



}


```

Notice how `onClick={handleClick}` has no parentheses at the end! Do not *call* the event handler function: you only need to *pass it down*. React will call your event handler when the user clicks the button.

## Updating the screen

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add *state* to your component.

First, import [`useState`](/reference/react/useState) from React:

```


import { useState } from 'react';


```

Now you can declare a *state variable* inside your component:

```


function MyButton() {



const [count, setCount] = useState(0);



// ...


```

You’ll get two things from `useState`: the current state (`count`), and the function that lets you update it (`setCount`). You can give them any names, but the convention is to write `
```

**[jina]** (5.19s, 16737 chars; wr=1.0, wo=0.0; hdr 5, code 0, links 8, lists 6)
```
Title: Quick Start – React

URL Source: https://react.dev/learn

Markdown Content:
Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

### You will learn

*   How to create and nest components
*   How to add markup and styles
*   How to display data
*   How to render conditions and lists
*   How to respond to events and update the screen
*   How to share data between components

## Creating and nesting components [](https://react.dev/learn#components "Link for Creating and nesting components ")

React apps are made out of _components_. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

`function MyButton() {return (<button>I'm a button</button>);}`

Now that you’ve declared `MyButton`, you can nest it into another component:

`export default function MyApp() {return (<div><h1>Welcome to my app</h1><MyButton /></div>);}`

Notice that `<MyButton />` starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

The `export default` keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, [MDN](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) and [javascript.info](https://javascript.info/import-export) have great references.

## Writing markup with JSX [](https://react.dev/learn#writing-markup-with-jsx "Link for Writing markup with JSX ")

The markup syntax you’ve seen above is called _JSX_.

[…середина…]

   >
      {product.title}
    </li>
  );

  return (
    <ul>{listItems}</ul>
  );
}

## Responding to events [](https://react.dev/learn#responding-to-events "Link for Responding to events ")

You can respond to events by declaring _event handler_ functions inside your components:

`function MyButton() {function handleClick() {alert('You clicked me!');}return (<button onClick={handleClick}>      Click me</button>);}`

Notice how `onClick={handleClick}` has no parentheses at the end! Do not _call_ the event handler function: you only need to _pass it down_. React will call your event handler when the user clicks the button.

## Updating the screen [](https://react.dev/learn#updating-the-screen "Link for Updating the screen ")

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add _state_ to your component.

First, import [`useState`](https://react.dev/reference/react/useState) from React:

`import { useState } from 'react';`

Now you can declare a _state variable_ inside your component:

`function MyButton() {const [count, setCount] = useState(0);// ...`

You’ll 
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U2: https://tailwindcss.com/docs/installation
_(note: доки tailwind)_

**[local-auto]** (1.04s, 1896 chars, tier http; wr=1.0, wo=0.0; hdr 0, code 0, links 1, lists 0)
```
---
title: Installing with Vite - Installation
url: https://tailwindcss.com/docs/installation/using-vite
hostname: tailwindcss.com
description: Integrate Tailwind CSS with frameworks like Laravel, SvelteKit, React Router, and SolidJS.
sitename: Tailwind CSS
date: "2026-01-01"
---
Installation

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

`npm create vite@latest my-projectcd my-project`
Install `tailwindcss` and `@tailwindcss/vite` via npm.

`npm install tailwindcss @tailwindcss/vite`
Add the `@tailwindcss/vite` plugin to your Vite configuration.

`import { defineConfig } from 'vite'import tailwindcss from '@tailwindcss/vite'export default defineConfig({  plugins: [    tailwindcss(),  ],})`
Add an `@import` to your CSS file that imports Tailwind CSS.

`@import "tailwindcss";`
Run your build process with `npm run dev` or whatever command is configured in your `package.json` file.

`npm run dev`
Make sure your compiled CSS is included in the `<head>` *(your framework might handle this for you)*, then start using Tailwind’s utility classes to style your content.

`<!doctype html><html><head>  <meta charset="UTF-8">  <meta name="viewport" content="width=device-width, initial-scale=1.0">  <link href="/src/style.css" rel="stylesheet
```

**[local-http]** (0.99s, 1896 chars, tier http; wr=1.0, wo=0.0; hdr 0, code 0, links 1, lists 0)
```
---
title: Installing with Vite - Installation
url: https://tailwindcss.com/docs/installation/using-vite
hostname: tailwindcss.com
description: Integrate Tailwind CSS with frameworks like Laravel, SvelteKit, React Router, and SolidJS.
sitename: Tailwind CSS
date: "2026-01-01"
---
Installation

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

`npm create vite@latest my-projectcd my-project`
Install `tailwindcss` and `@tailwindcss/vite` via npm.

`npm install tailwindcss @tailwindcss/vite`
Add the `@tailwindcss/vite` plugin to your Vite configuration.

`import { defineConfig } from 'vite'import tailwindcss from '@tailwindcss/vite'export default defineConfig({  plugins: [    tailwindcss(),  ],})`
Add an `@import` to your CSS file that imports Tailwind CSS.

`@import "tailwindcss";`
Run your build process with `npm run dev` or whatever command is configured in your `package.json` file.

`npm run dev`
Make sure your compiled CSS is included in the `<head>` *(your framework might handle this for you)*, then start using Tailwind’s utility classes to style your content.

`<!doctype html><html><head>  <meta charset="UTF-8">  <meta name="viewport" content="width=device-width, initial-scale=1.0">  <link href="/src/style.css" rel="stylesheet
```

**[local-curl]** (0.99s, 1896 chars, tier curl; wr=1.0, wo=0.0; hdr 0, code 0, links 1, lists 0)
```
---
title: Installing with Vite - Installation
url: https://tailwindcss.com/docs/installation/using-vite
hostname: tailwindcss.com
description: Integrate Tailwind CSS with frameworks like Laravel, SvelteKit, React Router, and SolidJS.
sitename: Tailwind CSS
date: "2026-01-01"
---
Installation

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

`npm create vite@latest my-projectcd my-project`
Install `tailwindcss` and `@tailwindcss/vite` via npm.

`npm install tailwindcss @tailwindcss/vite`
Add the `@tailwindcss/vite` plugin to your Vite configuration.

`import { defineConfig } from 'vite'import tailwindcss from '@tailwindcss/vite'export default defineConfig({  plugins: [    tailwindcss(),  ],})`
Add an `@import` to your CSS file that imports Tailwind CSS.

`@import "tailwindcss";`
Run your build process with `npm run dev` or whatever command is configured in your `package.json` file.

`npm run dev`
Make sure your compiled CSS is included in the `<head>` *(your framework might handle this for you)*, then start using Tailwind’s utility classes to style your content.

`<!doctype html><html><head>  <meta charset="UTF-8">  <meta name="viewport" content="width=device-width, initial-scale=1.0">  <link href="/src/style.css" rel="stylesheet
```

**[local-browser]** (4.9s, 1896 chars, tier browser; wr=1.0, wo=0.0; hdr 0, code 0, links 1, lists 0)
```
---
title: Installing with Vite - Installation
url: https://tailwindcss.com/docs/installation/using-vite
hostname: tailwindcss.com
description: Integrate Tailwind CSS with frameworks like Laravel, SvelteKit, React Router, and SolidJS.
sitename: Tailwind CSS
date: "2026-01-01"
---
Installation

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

`npm create vite@latest my-projectcd my-project`
Install `tailwindcss` and `@tailwindcss/vite` via npm.

`npm install tailwindcss @tailwindcss/vite`
Add the `@tailwindcss/vite` plugin to your Vite configuration.

`import { defineConfig } from 'vite'import tailwindcss from '@tailwindcss/vite'export default defineConfig({  plugins: [    tailwindcss(),  ],})`
Add an `@import` to your CSS file that imports Tailwind CSS.

`@import "tailwindcss";`
Run your build process with `npm run dev` or whatever command is configured in your `package.json` file.

`npm run dev`
Make sure your compiled CSS is included in the `<head>` *(your framework might handle this for you)*, then start using Tailwind’s utility classes to style your content.

`<!doctype html><html><head>  <meta charset="UTF-8">  <meta name="viewport" content="width=device-width, initial-scale=1.0">  <link href="/src/style.css" rel="stylesheet
```

**[firecrawl]** (1.39s, 3143 chars; wr=1.0, wo=1.0; hdr 9, code 12, links 15, lists 5)
```
[Home](https://tailwindcss.com/) v4.3

`⌘K`  `Ctrl K` [Docs](https://tailwindcss.com/docs) [Blog](https://tailwindcss.com/blog) [Showcase](https://tailwindcss.com/showcase) [Partners](https://tailwindcss.com/partners) [Plus](https://tailwindcss.com/plus?ref=top) [GitHub repository](https://github.com/tailwindlabs/tailwindcss)

1. Getting Started
2. Using Vite

Installation

# Get started with Tailwind CSS

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

## Installation

- ## [Using Vite](https://tailwindcss.com/docs/installation/using-vite)

- ## [Using PostCSS](https://tailwindcss.com/docs/installation/using-postcss)

- ## [Tailwind CLI](https://tailwindcss.com/docs/installation/tailwind-cli)

- ## [Framework Guides](https://tailwindcss.com/docs/installation/framework-guides)

- ## [Play CDN](https://tailwindcss.com/docs/installation/play-cdn)


### Installing Tailwind CSS as a Vite plugin

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

01

#### Create your project

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

Terminal

```
npm create vite@latest my-projectcd my-project
```

02

#### Install Tailwind CSS

Install `tailwindcss` and `@tailwindcss/vite` via npm.

Terminal

```
npm install tailwindcss @tailwindcss/vite
```

03

#### Configure the Vite plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration.

```

**[tavily]** (0.77s, 3612 chars; wr=1.0, wo=1.0; hdr 9, code 12, links 13, lists 5)
```
[Docs](/docs)[Blog](/blog)[Showcase](/showcase)[Partners](/partners)[Plus](/plus?ref=top)

1. Getting Started
2. Using Vite

Installation

# Get started with Tailwind CSS

Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

## Installation

* ## [Using Vite](/docs/installation/using-vite)
* ## [Using PostCSS](/docs/installation/using-postcss)
* ## [Tailwind CLI](/docs/installation/tailwind-cli)
* ## [Framework Guides](/docs/installation/framework-guides)
* ## [Play CDN](/docs/installation/play-cdn)

### Installing Tailwind CSS as a Vite plugin

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

01

#### Create your project

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use[Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

Terminal

```
npm create vite@latest my-project npm  create  vite@latest my-projectcd my-project cd my-project
```

02

#### Install Tailwind CSS

Install `tailwindcss` and `@tailwindcss/vite` via npm.

Terminal

```
npm install tailwindcss @tailwindcss/vite npm  install  tailwindcss @tailwindcss/vite
```

03

#### Configure the Vite plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration.

vite.config.ts

```
import { defineConfig } from 'vite' import { defineConfig }  from  'vite'import tailwindcss from '@tailwindcss/vite' import  tailwindcss  from '@tailwindcss/vite' export default defineConfig({export  default  defineConfig({ plugins: [ plugins: 
```

**[jina]** (0.85s, 2625 chars; wr=1.0, wo=0.0; hdr 7, code 0, links 6, lists 5)
```
Title: Installing with Vite - Installation

URL Source: https://tailwindcss.com/docs/installation

Markdown Content:
Tailwind CSS works by scanning all of your HTML files, JavaScript components, and any other templates for class names, generating the corresponding styles and then writing them to a static CSS file.

It's fast, flexible, and reliable — with zero-runtime.

*   ## [Using Vite](https://tailwindcss.com/docs/installation/using-vite)

*   ## [Using PostCSS](https://tailwindcss.com/docs/installation/using-postcss)

*   ## [Tailwind CLI](https://tailwindcss.com/docs/installation/tailwind-cli)

*   ## [Framework Guides](https://tailwindcss.com/docs/installation/framework-guides)

*   ## [Play CDN](https://tailwindcss.com/docs/installation/play-cdn)

### Installing Tailwind CSS as a Vite plugin

Installing Tailwind CSS as a Vite plugin is the most seamless way to integrate it with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

01

#### Create your project

Start by creating a new Vite project if you don’t have one set up already. The most common approach is to use[Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

Terminal

`npm create vite@latest my-projectcd my-project`

02

#### Install Tailwind CSS

Install `tailwindcss` and `@tailwindcss/vite` via npm.

Terminal

`npm install tailwindcss @tailwindcss/vite`

03

#### Configure the Vite plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration.

vite.config.ts

`import { defineConfig } from 'vite'import tailwindcss from '@tailwindcss/vite'export default defineConfig({  plugins: [    tailwindcss(),  ],})`

04

#### Import Tailwind CSS

Add an `@import` to your CSS file that imports Tailwind CSS.

CSS

`@import "tailwindcss";`

05

#### Start your build p
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U3: https://docs.docker.com/engine/containers/run/
_(note: доки docker)_

**[local-auto]** (0.9s, 32000 chars, tier http; wr=1.0, wo=0.0; hdr 6, code 10, links 5, lists 2)
```
---
title: Running containers
url: https://docs.docker.com/engine/containers/run/
hostname: docker.com
description: Running and configuring containers with the Docker CLI
sitename: Docker Documentation
date: "2026-05-13"
tags: ['docker,run,cli']
---
# Running containers

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When you
execute `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](https://docs.docker.com#general-form)

A `docker run` command takes the following form:

```
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```
The `docker run` command must specify an [image reference](https://docs.docker.com#image-references)
to create the container from.

### [Image references](https://docs.docker.com#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

- `docker run IMAGE[:TAG][@DIGEST]`
- `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use
the tag to run a container from specific version of an image. For example, to
run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](https://docs.docker.com#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image wi

[…середина…]

ness behavior. Accepts an integer between 0 and 100. | 
| `--shm-size=""` | Size of `/dev/shm` . The format is`<number><unit>` .`number` must be greater than`0` . Unit is optional and can be`b` (bytes),`k` (kilobytes),`m` (megabytes), or`g` (gigabytes). If you omit the unit, the system uses bytes. If you omit the size entirely, the system uses`64m` . | 

### [User memory constraints](https://docs.docker.com#user-memory-constraints)

We have four ways to set user memory usage:

| Option | Result | 
|---|---|
| **memory=inf, memory-swap=inf** (default) | There is no memory limit for the container. The container can use as much memory as needed. | 
| **memory=L<inf, memory-swap=inf** | (specify memory and set memory-swap as `-1` ) The container is not allowed to use more than L bytes of memory, but can use as much swap as is needed (if the host supports swap memory). | 
| **memory=L<inf, memory-swap=2*L** | (specify memory without memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is double of that. | 
| **memory=L<inf, memory-swap=S<inf, L<=S** | (specify both memory and memory-swap) The container is not allowed to use more than L b
```

**[local-http]** (0.91s, 32000 chars, tier http; wr=1.0, wo=0.0; hdr 6, code 10, links 5, lists 2)
```
---
title: Running containers
url: https://docs.docker.com/engine/containers/run/
hostname: docker.com
description: Running and configuring containers with the Docker CLI
sitename: Docker Documentation
date: "2026-05-13"
tags: ['docker,run,cli']
---
# Running containers

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When you
execute `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](https://docs.docker.com#general-form)

A `docker run` command takes the following form:

```
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```
The `docker run` command must specify an [image reference](https://docs.docker.com#image-references)
to create the container from.

### [Image references](https://docs.docker.com#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

- `docker run IMAGE[:TAG][@DIGEST]`
- `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use
the tag to run a container from specific version of an image. For example, to
run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](https://docs.docker.com#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image wi

[…середина…]

ness behavior. Accepts an integer between 0 and 100. | 
| `--shm-size=""` | Size of `/dev/shm` . The format is`<number><unit>` .`number` must be greater than`0` . Unit is optional and can be`b` (bytes),`k` (kilobytes),`m` (megabytes), or`g` (gigabytes). If you omit the unit, the system uses bytes. If you omit the size entirely, the system uses`64m` . | 

### [User memory constraints](https://docs.docker.com#user-memory-constraints)

We have four ways to set user memory usage:

| Option | Result | 
|---|---|
| **memory=inf, memory-swap=inf** (default) | There is no memory limit for the container. The container can use as much memory as needed. | 
| **memory=L<inf, memory-swap=inf** | (specify memory and set memory-swap as `-1` ) The container is not allowed to use more than L bytes of memory, but can use as much swap as is needed (if the host supports swap memory). | 
| **memory=L<inf, memory-swap=2*L** | (specify memory without memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is double of that. | 
| **memory=L<inf, memory-swap=S<inf, L<=S** | (specify both memory and memory-swap) The container is not allowed to use more than L b
```

**[local-curl]** (0.92s, 32000 chars, tier curl; wr=1.0, wo=0.0; hdr 6, code 10, links 5, lists 2)
```
---
title: Running containers
url: https://docs.docker.com/engine/containers/run/
hostname: docker.com
description: Running and configuring containers with the Docker CLI
sitename: Docker Documentation
date: "2026-05-13"
tags: ['docker,run,cli']
---
# Running containers

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When you
execute `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](https://docs.docker.com#general-form)

A `docker run` command takes the following form:

```
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```
The `docker run` command must specify an [image reference](https://docs.docker.com#image-references)
to create the container from.

### [Image references](https://docs.docker.com#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

- `docker run IMAGE[:TAG][@DIGEST]`
- `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use
the tag to run a container from specific version of an image. For example, to
run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](https://docs.docker.com#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image wi

[…середина…]

ness behavior. Accepts an integer between 0 and 100. | 
| `--shm-size=""` | Size of `/dev/shm` . The format is`<number><unit>` .`number` must be greater than`0` . Unit is optional and can be`b` (bytes),`k` (kilobytes),`m` (megabytes), or`g` (gigabytes). If you omit the unit, the system uses bytes. If you omit the size entirely, the system uses`64m` . | 

### [User memory constraints](https://docs.docker.com#user-memory-constraints)

We have four ways to set user memory usage:

| Option | Result | 
|---|---|
| **memory=inf, memory-swap=inf** (default) | There is no memory limit for the container. The container can use as much memory as needed. | 
| **memory=L<inf, memory-swap=inf** | (specify memory and set memory-swap as `-1` ) The container is not allowed to use more than L bytes of memory, but can use as much swap as is needed (if the host supports swap memory). | 
| **memory=L<inf, memory-swap=2*L** | (specify memory without memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is double of that. | 
| **memory=L<inf, memory-swap=S<inf, L<=S** | (specify both memory and memory-swap) The container is not allowed to use more than L b
```

**[local-browser]** (6.94s, 32000 chars, tier browser; wr=1.0, wo=0.0; hdr 6, code 10, links 5, lists 2)
```
---
title: Running containers
url: https://docs.docker.com/engine/containers/run/
hostname: docker.com
description: Running and configuring containers with the Docker CLI
sitename: Docker Documentation
date: "2026-05-13"
tags: ['docker,run,cli']
---
# Running containers

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When you
execute `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](https://docs.docker.com#general-form)

A `docker run` command takes the following form:

```
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```
The `docker run` command must specify an [image reference](https://docs.docker.com#image-references)
to create the container from.

### [Image references](https://docs.docker.com#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

- `docker run IMAGE[:TAG][@DIGEST]`
- `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use
the tag to run a container from specific version of an image. For example, to
run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](https://docs.docker.com#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image wi

[…середина…]

r. Accepts an integer between 0 and 100. | 
| `--shm-size=""` | Size of `/dev/shm` . The format is`<number><unit>` .`number` must be greater than`0` . Unit is optional and can be`b` (bytes),`k` (kilobytes),`m` (megabytes), or`g` (gigabytes). If you omit the unit, the system uses bytes. If you omit the size entirely, the system uses`64m` . | 

### [User memory constraints](https://docs.docker.com#user-memory-constraints)

We have four ways to set user memory usage:

| Option | Result | 
|---|---|
| **memory=inf, memory-swap=inf** (default) | There is no memory limit for the container. The container can use as much memory as needed. | 
| **memory=L<inf, memory-swap=inf** | (specify memory and set memory-swap as `-1` ) The container is not allowed to use more than L bytes of memory, but can use as much swap as is needed (if the host supports swap memory). | 
| **memory=L<inf, memory-swap=2*L** | (specify memory without memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is double of that. | 
| **memory=L<inf, memory-swap=S<inf, L<=S** | (specify both memory and memory-swap) The container is not allowed to use more than L bytes of memo
```

**[firecrawl]** (10.86s, 32000 chars; wr=0.333, wo=0.25; hdr 6, code 2, links 9, lists 5)
```
Start a new chat

### What can I help you with?

I'm Gordon, your AI assistant for Docker and documentation
questions.

Try asking

Get started with Docker

Docker Hardened Images

MCP Toolkit

Create an org

### What can I help you with?

I'm Gordon, your AI assistant for Docker and documentation
questions.

Try asking

Get started with Docker

Docker Hardened Images

MCP Toolkit

Create an org

Was this helpful?

HelpfulNot quite

Copy

remaining in this thread.

You've reached the maximum of
questions per thread. For
better answer quality, start a new thread.

Start a new thread

When enabled, Gordon considers the current page you're viewing
to provide more relevant answers.

[Share feedback](https://github.com/docker/docs/issues/23966)

Answers are generated based on the documentation.

Back

[Manuals](https://docs.docker.com/manuals/)

- [Get started](https://docs.docker.com/get-started/)
- [Guides](https://docs.docker.com/guides/)
- [Reference](https://docs.docker.com/reference/)

# Running containers

Ask GordonCopy MarkdownView Markdown

* * *

Table of contents

* * *

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When you
execute `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](https://docs.docker.com/engine/containers/run/\#general-form)

A `docker run` command takes the following form:

```console
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

The `docker run` command must specify an [image reference](https://docs.docker.com/engine/containers/run/#

[…середина…]

mit the CPU real-time period. In microseconds. Requires parent cgroups be set and cannot be higher than parent. Also check rtprio ulimits. |
| `--cpu-rt-runtime=0` | Limit the CPU real-time runtime. In microseconds. Requires parent cgroups be set and cannot be higher than parent. Also check rtprio ulimits. |
| `--blkio-weight=0` | Block IO weight (relative weight) accepts a weight value between 10 and 1000. |
| `--blkio-weight-device=""` | Block IO weight (relative device weight, format: `DEVICE_NAME:WEIGHT`) |
| `--device-read-bps=""` | Limit read rate from a device (format: `<device-path>:<number>[<unit>]`). Number is a positive integer. Unit can be one of `kb`, `mb`, or `gb`. |
| `--device-write-bps=""` | Limit write rate to a device (format: `<device-path>:<number>[<unit>]`). Number is a positive integer. Unit can be one of `kb`, `mb`, or `gb`. |
| `--device-read-iops=""` | Limit read rate (IO per second) from a device (format: `<device-path>:<number>`). Number is a positive integer. |
| `--device-write-iops=""` | Limit write rate (IO per second) to a device (format: `<device-path>:<number>`). Number is a positive integer. |
| `--oom-kill-disable=false` | Whether to disable OOM
```

**[tavily]** (1.09s, 32000 chars; wr=0.333, wo=0.25; hdr 8, code 8, links 10, lists 5)
```
Gordon, your AI assistant for Docker docs

Start a new chat

### What can I help you with?

I'm Gordon, your AI assistant for Docker and documentation questions.

Try asking

Was this helpful?

remaining in this thread.

You've reached the maximum of questions per thread. For better answer quality, start a new thread.

Answers are generated based on the documentation.

* [Get started](/get-started/)
* [Guides](/guides/)
* [Reference](/reference/)

# Running containers

---

Table of contents

---

Docker runs processes in isolated containers. A container is a process which runs on a host. The host may be local or remote. When you execute `docker run`, the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](#general-form)

A `docker run` command takes the following form:

```
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...] $ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...] $[][|][][]
```

The `docker run` command must specify an [image reference](#image-references) to create the container from.

### [Image references](#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

* `docker run IMAGE[:TAG][@DIGEST]`
* `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use the tag to run a container from specific version of an image. For example, to run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](#image-digests)

Images using the v2 or later image format hav

[…середина…]



```
$ docker run busybox /etc; echo $? $ docker run busybox /etc; echo $? $; echo $?    docker: Error response from daemon: Container command '/etc' could not be invoked. docker: Error response from daemon: Container command '/etc' could not be invoked. docker: Error response from daemon: Container command '/etc' could not be invoked. 126 126 126 
```

### [127](#127)

Exit code `127` indicates that the contained command can't be found.

```
$ docker run busybox foo; echo $? $ docker run busybox foo; echo $? $; echo $?    docker: Error response from daemon: Container command 'foo' not found or does not exist. docker: Error response from daemon: Container command 'foo' not found or does not exist. docker: Error response from daemon: Container command 'foo' not found or does not exist. 127 127 127 
```

### [Other exit codes](#other-exit-codes)

Any exit code other than `125`, `126`, and `127` represent the exit code of the provided container command.

```
$ docker run busybox /bin/sh -c 'exit 3' $ docker run busybox /bin/sh -c 'exit 3' $ 'exit 3' $ echo $? $ echo $? $ echo $? 3 3 3 
```

## [Runtime constraints on resources](#runtime-constraints-on-resources)

The operator can als
```

**[jina]** (5.95s, 32000 chars; wr=0.333, wo=0.0; hdr 4, code 0, links 5, lists 2)
```
Title: Running containers

URL Source: https://docs.docker.com/engine/containers/run/

Published Time: 2026-05-13 14:54:03 +0000 UTC

Markdown Content:
Docker runs processes in isolated containers. A container is a process which runs on a host. The host may be local or remote. When you execute `docker run`, the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

A `docker run` command takes the following form:

The `docker run` command must specify an [image reference](https://docs.docker.com/engine/containers/run/#image-references) to create the container from.

### [Image references](https://docs.docker.com/engine/containers/run/#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

*   `docker run IMAGE[:TAG][@DIGEST]`
*   `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use the tag to run a container from specific version of an image. For example, to run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](https://docs.docker.com/engine/containers/run/#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image with the `sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0` digest:

### [Options](https://docs.docker.com/engine/containers/run/#options)

`[OPTIONS]` l

[…середина…]

sets the memory reservation to 200M.

Under this configuration, when the container consumes memory more than 200M and less than 500M, the next system memory reclaim attempts to shrink container memory below 200M.

The following example set memory reservation to 1G without a hard memory limit.

The container can use as much memory as it needs. The memory reservation setting ensures the container doesn't consume too much memory for long time, because every memory reclaim shrinks the container's consumption to the reservation.

By default, kernel kills processes in a container if an out-of-memory (OOM) error occurs. To change this behaviour, use the `--oom-kill-disable` option. Only disable the OOM killer on containers where you have also set the `-m/--memory` option. If the `-m` flag is not set, this can result in the host running out of memory and require killing the host's system processes to free memory.

The following example limits the memory to 100M and disables the OOM killer for this container:

The following example, illustrates a dangerous way to use the flag:

The container has unlimited memory which can cause the host to run out memory and require killing system processes
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U4: https://nextjs.org/docs/app/getting-started/installation
_(note: доки nextjs)_

**[local-auto]** (0.86s, 12508 chars, tier http; wr=1.0, wo=0.25; hdr 9, code 5, links 7, lists 7)
```
---
title: "Getting Started: Installation | Next.js"
url: https://nextjs.org/docs/app/getting-started/installation
hostname: nextjs.org
description: Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.
sitename: Next.js
date: "2026-07-21"
---
`Accept: text/markdown` header. For an index of Next.js documentation, see [/docs/llms.txt](https://nextjs.org/docs/llms.txt).

# Installation

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000` .

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```
- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias`@/*` , and includes`AGENTS.md` (with a`CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

`pnpm create ne

[…середина…]

 to create the root layout, Next.js will automatically create this file when running the development server with
`next dev`.- You can optionally use a
[`src` folder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create the `public` folder (optional)

Create a [`public` folder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

```
import Image from 'next/image'
 
export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```
## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

Minimum TypeSc
```

**[local-http]** (0.85s, 12508 chars, tier http; wr=1.0, wo=0.25; hdr 9, code 5, links 7, lists 7)
```
---
title: "Getting Started: Installation | Next.js"
url: https://nextjs.org/docs/app/getting-started/installation
hostname: nextjs.org
description: Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.
sitename: Next.js
date: "2026-07-21"
---
`Accept: text/markdown` header. For an index of Next.js documentation, see [/docs/llms.txt](https://nextjs.org/docs/llms.txt).

# Installation

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000` .

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```
- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias`@/*` , and includes`AGENTS.md` (with a`CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

`pnpm create ne

[…середина…]

 to create the root layout, Next.js will automatically create this file when running the development server with
`next dev`.- You can optionally use a
[`src` folder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create the `public` folder (optional)

Create a [`public` folder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

```
import Image from 'next/image'
 
export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```
## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

Minimum TypeSc
```

**[local-curl]** (0.95s, 12508 chars, tier curl; wr=1.0, wo=0.25; hdr 9, code 5, links 7, lists 7)
```
---
title: "Getting Started: Installation | Next.js"
url: https://nextjs.org/docs/app/getting-started/installation
hostname: nextjs.org
description: Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.
sitename: Next.js
date: "2026-07-21"
---
`Accept: text/markdown` header. For an index of Next.js documentation, see [/docs/llms.txt](https://nextjs.org/docs/llms.txt).

# Installation

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000` .

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```
- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias`@/*` , and includes`AGENTS.md` (with a`CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

`pnpm create ne

[…середина…]

 to create the root layout, Next.js will automatically create this file when running the development server with
`next dev`.- You can optionally use a
[`src` folder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create the `public` folder (optional)

Create a [`public` folder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

```
import Image from 'next/image'
 
export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```
## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

Minimum TypeSc
```

**[local-browser]** (6.63s, 12508 chars, tier browser; wr=1.0, wo=0.25; hdr 9, code 5, links 7, lists 7)
```
---
title: "Getting Started: Installation | Next.js"
url: https://nextjs.org/docs/app/getting-started/installation
hostname: nextjs.org
description: Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.
sitename: Next.js
date: "2026-07-21"
---
`Accept: text/markdown` header. For an index of Next.js documentation, see [/docs/llms.txt](https://nextjs.org/docs/llms.txt).

# Installation

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000` .

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```
- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias`@/*` , and includes`AGENTS.md` (with a`CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

`pnpm create ne

[…середина…]

 to create the root layout, Next.js will automatically create this file when running the development server with
`next dev`.- You can optionally use a
[`src` folder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create the `public` folder (optional)

Create a [`public` folder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

```
import Image from 'next/image'
 
export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```
## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

Minimum TypeSc
```

**[firecrawl]** (5.15s, 14965 chars; wr=1.0, wo=0.25; hdr 9, code 4, links 12, lists 7)
```
Menu

Using App Router

Features available in /app

Latest Version

16.3.3

Using App Router

Features available in /app

Latest Version

16.3.3

This page is also available as Markdown: request this page's URL with an `Accept: text/markdown` header.For an index of Next.js documentation, see [/docs/llms.txt](https://nextjs.org/docs/llms.txt).

Copy page

On this page

# Installation

Last updated July 21, 2026

Create a new Next.js app and run it locally.

## Quick start [Link to this section](https://nextjs.org/docs/app/getting-started/installation\#quick-start)

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000`.

pnpmnpmyarnbun

Terminal

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```

- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias `@/*`, and includes `AGENTS.md` (with a `CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements [Link to this section](https://nextjs.org/docs/app/getting-started/installation\#system-requirements)

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers [Link to this section](https://nextjs.org/docs/app/getting-started/installation\#supported-browsers)

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target 

[…середина…]

oject to separate your application's code from configuration files.

### Create the `public` folder (optional) [Link to this section](https://nextjs.org/docs/app/getting-started/installation\#create-the-public-folder-optional)

Create a [`public` folder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

app/page.tsx

TypeScript

JavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```

## Run the development server [Link to this section](https://nextjs.org/docs/app/getting-started/installation\#run-the-development-server)

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript [
```

**[tavily]** (0.83s, 14464 chars; wr=1.0, wo=0.5; hdr 10, code 7, links 7, lists 7)
```
[Skip to content](#geist-skip-nav)


This page is also available as Markdown: request this page's URL with an `Accept: text/markdown` header. For an index of Next.js documentation, see </docs/llms.txt>.

# Installation

Last updated July 21, 2026

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000`.

Terminal

```
pnpm create next-app@latest my-app --yes pnpm  create next-app@latest my-app --yescd my-app cd my-app pnpm dev pnpm  dev
```

* `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias `@/*`, and includes `AGENTS.md` (with a `CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

* Minimum Node.js version: [20.9](https://nodejs.org/)
* Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

* Chrome 111+
* Edge 111+
* Firefox 111+
* Safari 16.4+

Learn more about [browser support](/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [`create-next-app`](/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

Terminal

```
pnpm create next-app pnpm  create next-app
```

On installation, you'll see the following prompts:

Terminal

```
What is your project named? my-appWhat is your project named? my-appWo

[…середина…]

optionally use a [`src` folder](/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create the `public` folder (optional)

Create a [`public` folder](/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

app/page.tsx

TypeScript

```
import Image from 'next/image' import  Image from 'next/image'  export default function Page() {export  default  function  Page() { return <Image src="/profile.png" alt="Profile" width={100} height={100} />  return < Image  src ="/profile.png"  alt = "Profile"  width ={100} height ={100} />}}
```

## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

> Minimu
```

**[jina]** (4.88s, 32000 chars; wr=0.0, wo=0.25; hdr 0, code 0, links 41, lists 22)
```
Title: Getting Started: Installation

URL Source: https://nextjs.org/docs/app/getting-started/installation

Markdown Content:
[Skip to content](https://nextjs.org/docs/app/getting-started/installation#geist-skip-nav)

[![Image 5: Vercel](https://nextjs.org/_next/static/immutable/media/vercel-light.3_gxxexgi1nmy.svg)![Image 6: Vercel](https://nextjs.org/_next/static/immutable/media/vercel-dark.1f3cgy23m5_jy.svg)](https://vercel.com/home?utm_source=next-site&utm_medium=banner&utm_campaign=docs_app_getting-started_installation "Go to Vercel homepage")[![Image 7: NextjsLogotype](https://nextjs.org/_next/static/immutable/media/nextjs-logotype-light.00-_80jv8_dct.svg)![Image 8: NextjsLogotype](https://nextjs.org/_next/static/immutable/media/nextjs-logotype-dark.3h4a2z2v_dkod.svg)](https://nextjs.org/ "Go to the homepage")

Search documentation...CtrlK Search...CtrlK

[![Image 9: Vercel](https://nextjs.org/_next/static/immutable/media/vercel-light.3_gxxexgi1nmy.svg)![Image 10: Vercel](https://nextjs.org/_next/static/immutable/media/vercel-dark.1f3cgy23m5_jy.svg)](https://vercel.com/home?utm_source=next-site&utm_medium=banner&utm_campaign=docs_app_getting-started_installation "Go to Vercel homepage")[![Image 11: NextjsLogotype](https://nextjs.org/_next/static/immutable/media/nextjs-logotype-light.00-_80jv8_dct.svg)![Image 12: NextjsLogotype](https://nextjs.org/_next/static/immutable/media/nextjs-logotype-dark.3h4a2z2v_dkod.svg)](https://nextjs.org/ "Go to the homepage")

[Showcase](https://nextjs.org/showcase)[Docs](https://nextjs.org/docs "Documentation")[Blog](https://nextjs.org/blog)[Templates](https://vercel.com/templates/next.js?utm_source=next-site&utm_medium=navbar&utm_campaign=next_site_nav_templates)[Enterprise](https://vercel.com/contact/sales?utm_source=next-site&utm

[…середина…]

unctions/connection)
        *   [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
        *   [draftMode](https://nextjs.org/docs/app/api-reference/functions/draft-mode)
        *   [fetch](https://nextjs.org/docs/app/api-reference/functions/fetch)
        *   [forbidden](https://nextjs.org/docs/app/api-reference/functions/forbidden)
        *   [generateImageMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata)
        *   [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)
        *   [generateSitemaps](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps)
        *   [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)
        *   [generateViewport](https://nextjs.org/docs/app/api-reference/functions/generate-viewport)
        *   [headers](https://nextjs.org/docs/app/api-reference/functions/headers)
        *   [ImageResponse](https://nextjs.org/docs/app/api-reference/functions/image-response)
        *   [io](https://nextjs.org/docs/app/api-reference/functions/io)
        *   [NextRequest](https://nextjs.org/docs/app/api-re
```

**[parallel]** (2.04s, 10522 chars; wr=0.333, wo=0.25; hdr 6, code 16, links 9, lists 12)
```
title: Installation
description: "Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases."
url: "https://nextjs.org/docs/app/getting-started/installation"
docs_index: /docs/llms.txt
version: 16.3.3
lastUpdated: 2026-07-21
prerequisites:
- "Getting Started: /docs/app/getting-started"
> For an index of all Next.js documentation, see [/docs/llms.txt](/docs/llms.txt).
> Create a new Next.js app and run it locally.

# Quick start
1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000`.
```bash package="pnpm"
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```
```bash package="npm"
npx create-next-app@latest my-app --yes
cd my-app
npm run dev
```
```bash package="yarn"
yarn create next-app@latest my-app --yes
cd my-app
yarn dev
```
```bash package="bun"
bun create next-app@latest my-app --yes
cd my-app
bun dev
```
* `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias `@/*`, and includes `AGENTS.md` (with a `CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.

## System requirements
Before you begin, make sure your development environment meets the following requirements:
* Minimum Node.js version: [20.9](https://nodejs.org/)
* Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers
Next.js supports modern browsers with zero configuration.
* Chrome 111+
* Edge 111+
* Firefox 111+
* Safari 16.4+
Learn more about [browser support](/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the C

[…середина…]

,
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```
These scripts refer to the different stages of developing an application:
* `next dev`: Starts the development server using Turbopack (default bundler).
* `next build`: Builds the application for production.
* `next start`: Starts the production server.
* `eslint`: Runs ESLint.
Turbopack is now the default bundler. To use Webpack run `next dev --webpack` or `next build --webpack`. See the [Turbopack docs](/docs/app/api-reference/turbopack) for configuration details.

### Create the `app` directory
Next.js uses file-system routing, which means the routes in your application are determined by how you structure your files.
Create an `app` folder. Then, inside `app`, create a `layout.tsx` file. This file is the [root layout](/docs/app/api-reference/file-conventions/layout#root-layout). It's required and must contain the `<html>` and `<body>` tags.

...

```jsx filename="app/layout.js" switcher
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```
Create a home page `app/page.tsx` with some initial content:
```tsx filename="app/page.tsx" switc
```

## U5: https://vuejs.org/guide/introduction.html
_(note: доки vue)_

**[local-auto]** (1.26s, 9811 chars, tier http; wr=1.0, wo=0.333; hdr 5, code 7, links 10, lists 4)
```
---
title: Vue.js
url: https://vuejs.org/
hostname: vuejs.org
description: Vue.js - The Progressive JavaScript Framework
sitename: Vuejs
date: "2026-01-01"
---
# Introduction [](https://vuejs.org#introduction)

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023** . Learn more about[Vue 2 EOL](https://v2.vuejs.org/eol/) .
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/) .


Learn Vue with video tutorials on VueMastery.com

![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)

![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)

## What is Vue? [](https://vuejs.org#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp, ref } from 'vue'
createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```
template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```
**Result**

The above example demonstrates the two core features of Vue:

- **Declarative Rendering** : Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.
- **Reactivity** : Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest o

[…середина…]

l stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a framework that can grow with you and adapt to your needs.

## Single-File Components [](https://vuejs.org#single-file-components)

In most build-tool-enabled Vue projects, we author Vue components using an HTML-like file format called **Single-File Component** (also known as `*.vue` files, abbreviated as **SFC**). A Vue SFC, as the name suggests, encapsulates the component's logic (JavaScript), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>
<style scoped>
button {
  font-weight: bold;
}
</style>
```
SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vu
```

**[local-http]** (1.14s, 9811 chars, tier http; wr=1.0, wo=0.333; hdr 5, code 7, links 10, lists 4)
```
---
title: Vue.js
url: https://vuejs.org/
hostname: vuejs.org
description: Vue.js - The Progressive JavaScript Framework
sitename: Vuejs
date: "2026-01-01"
---
# Introduction [](https://vuejs.org#introduction)

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023** . Learn more about[Vue 2 EOL](https://v2.vuejs.org/eol/) .
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/) .


Learn Vue with video tutorials on VueMastery.com

![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)

![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)

## What is Vue? [](https://vuejs.org#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp, ref } from 'vue'
createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```
template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```
**Result**

The above example demonstrates the two core features of Vue:

- **Declarative Rendering** : Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.
- **Reactivity** : Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest o

[…середина…]

l stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a framework that can grow with you and adapt to your needs.

## Single-File Components [](https://vuejs.org#single-file-components)

In most build-tool-enabled Vue projects, we author Vue components using an HTML-like file format called **Single-File Component** (also known as `*.vue` files, abbreviated as **SFC**). A Vue SFC, as the name suggests, encapsulates the component's logic (JavaScript), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>
<style scoped>
button {
  font-weight: bold;
}
</style>
```
SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vu
```

**[local-curl]** (0.78s, 9811 chars, tier curl; wr=1.0, wo=0.333; hdr 5, code 7, links 10, lists 4)
```
---
title: Vue.js
url: https://vuejs.org/
hostname: vuejs.org
description: Vue.js - The Progressive JavaScript Framework
sitename: Vuejs
date: "2026-01-01"
---
# Introduction [](https://vuejs.org#introduction)

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023** . Learn more about[Vue 2 EOL](https://v2.vuejs.org/eol/) .
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/) .


Learn Vue with video tutorials on VueMastery.com

![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)

![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)

## What is Vue? [](https://vuejs.org#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp, ref } from 'vue'
createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```
template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```
**Result**

The above example demonstrates the two core features of Vue:

- **Declarative Rendering** : Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.
- **Reactivity** : Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest o

[…середина…]

l stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a framework that can grow with you and adapt to your needs.

## Single-File Components [](https://vuejs.org#single-file-components)

In most build-tool-enabled Vue projects, we author Vue components using an HTML-like file format called **Single-File Component** (also known as `*.vue` files, abbreviated as **SFC**). A Vue SFC, as the name suggests, encapsulates the component's logic (JavaScript), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>
<style scoped>
button {
  font-weight: bold;
}
</style>
```
SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vu
```

**[local-browser]** (15.01s, 9811 chars, tier browser; wr=1.0, wo=0.333; hdr 5, code 7, links 10, lists 4)
```
---
title: Vue.js
url: https://vuejs.org/
hostname: vuejs.org
description: Vue.js - The Progressive JavaScript Framework
sitename: Vuejs
date: "2026-01-01"
---
# Introduction [](https://vuejs.org#introduction)

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023** . Learn more about[Vue 2 EOL](https://v2.vuejs.org/eol/) .
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/) .


Learn Vue with video tutorials on VueMastery.com

![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)

![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)

## What is Vue? [](https://vuejs.org#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp, ref } from 'vue'
createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```
template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```
**Result**

The above example demonstrates the two core features of Vue:

- **Declarative Rendering** : Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.
- **Reactivity** : Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest o

[…середина…]

l stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a framework that can grow with you and adapt to your needs.

## Single-File Components [](https://vuejs.org#single-file-components)

In most build-tool-enabled Vue projects, we author Vue components using an HTML-like file format called **Single-File Component** (also known as `*.vue` files, abbreviated as **SFC**). A Vue SFC, as the name suggests, encapsulates the component's logic (JavaScript), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>
<style scoped>
button {
  font-weight: bold;
}
</style>
```
SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vu
```

**[firecrawl]** (3.9s, 11711 chars; wr=0.667, wo=0.667; hdr 4, code 11, links 11, lists 4)
```
[Skip to content](https://vuejs.org/guide/introduction.html#VPContent)

On this page

# Introduction [​](https://vuejs.org/guide/introduction.html\#introduction)

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023**. Learn more about [Vue 2 EOL](https://v2.vuejs.org/eol/).
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/).

[![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)\\
\\
Learn Vue with video tutorials on VueMastery.com\\
\\
![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)](https://www.vuemastery.com/courses/)

## What is Vue? [​](https://vuejs.org/guide/introduction.html\#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp } from 'vue'

createApp({
  data() {
    return {
      count: 0
    }
  }
}).mount('#app')
```

js

```
import { createApp, ref } from 'vue'

createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```

template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```

**Result**

Count is: 0

The above example demonstrates the two core features of Vue:

- **Declarative Rendering**: Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.

- **Reactivity**: Vue automatically tracks JavaScript 

[…середина…]

ere's the previous example, written in SFC format:

vue

```
<script>
export default {
  data() {
    return {
      count: 0
    }
  }
}
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vuejs.org/guide/scaling-up/sfc) in its dedicated section - but for now, just know that Vue will handle all the build tools setup for you.

## API Styles [​](https://vuejs.org/guide/introduction.html\#api-styles)

Vue components can be authored in two different API styles: **Options API** and **Composition API**.

### Options API [​](https://vuejs.org/guide/introduction.html\#options-api)

With Options API, we define a component's logic using an object of options such as `data`, `methods`, a
```

**[tavily]** (0.73s, 9335 chars; wr=0.667, wo=0.667; hdr 3, code 6, links 19, lists 8)
```
[Skip to content](#VPContent)


[Vue.js](/)

[github](https://github.com/vuejs/ "github")[twitter](https://x.com/vuejs "twitter")[discord](https://discord.com/invite/vue "discord")

Appearance

[github](https://github.com/vuejs/ "github")[twitter](https://x.com/vuejs "twitter")[discord](https://discord.com/invite/vue "discord")

On this page

[Sponsors](/sponsor/)

[Become a Sponsor](/sponsor/)

Are you an LLM? You can read better optimized documentation at /guide/introduction.md for this page in Markdown format

# Introduction [​](#introduction)

You are reading the documentation for Vue 3!

* Vue 2 support has ended on **Dec 31, 2023**. Learn more about [Vue 2 EOL](https://v2.vuejs.org/eol/).
* Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/).

[![Vue Mastery banner](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vuemastery-graphical-link-96x56.png)

Learn Vue with video tutorials on VueMastery.com

![Vue Mastery Logo](https://storage.googleapis.com/vue-mastery.appspot.com/flamelink/media/vue-mastery-logo.png)](https://www.vuemastery.com/courses/)

## What is Vue? [​](#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp } from 'vue' import { createApp } from  'vue' createApp({createApp({ data() { data() { return { return { count: 0 count: 0 } } } }}).mount('#app')}). mount('#app')
```

js

```
import { createApp, ref } from 'vue' import { createApp, ref } from  'vue' createApp({createApp({ setup() { setup() { ret

[…середина…]

ue can be used in different ways:

* Enhancing static HTML without a build step
* Embedding as Web Components on any page
* Single-Page Application (SPA)
* Fullstack / Server-Side Rendering (SSR)
* Jamstack / Static Site Generation (SSG)
* Targeting desktop, mobile, WebGL, and even the terminal

If you find these concepts intimidating, don't worry! The tutorial and guide only require basic HTML and JavaScript knowledge, and you should be able to follow along without being an expert in any of these.

If you are an experienced developer interested in how to best integrate Vue into your stack, or you are curious about what these terms mean, we discuss them in more detail in [Ways of Using Vue](/guide/extras/ways-of-using-vue).

Despite the flexibility, the core knowledge about how Vue works is shared across all these use cases. Even if you are just a beginner now, the knowledge gained along the way will stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a fra
```

**[jina]** (3.84s, 10913 chars; wr=0.667, wo=0.333; hdr 4, code 11, links 7, lists 4)
```
Title: Vue.js

URL Source: https://vuejs.org/guide/introduction.html

Markdown Content:
## Introduction [​](https://vuejs.org/guide/introduction.html#introduction)

You are reading the documentation for Vue 3!

*   Vue 2 support has ended on **Dec 31, 2023**. Learn more about [Vue 2 EOL](https://v2.vuejs.org/eol/).
*   Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/).

## What is Vue? [​](https://vuejs.org/guide/introduction.html#what-is-vue)

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp } from 'vue'

createApp({
  data() {
    return {
      count: 0
    }
  }
}).mount('#app')
```

js

```
import { createApp, ref } from 'vue'

createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```

template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```

**Result**

The above example demonstrates the two core features of Vue:

*   **Declarative Rendering**: Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.

*   **Reactivity**: Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest of the documentation. For now, please read along so you can have a high-level understanding of what Vue offers.

Prerequisites

The rest of the documentation assumes basic familiarity wi

[…середина…]

Script), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script>
export default {
  data() {
    return {
      count: 0
    }
  }
}
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vuejs.org/guide/scaling-up/sfc) in its dedicated section - but for now, just know that Vue will handle all the build tools setup for you.

## API Styles [​](https://vuejs.org/guide/introduction.html#api-styles)

Vue components can be authored in two different API styles: **Options API** and **Composition API**.

### Options API [​](https://vuejs.org/guide/introduction.html#options-api)

With Options API, we define a component's l
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)
