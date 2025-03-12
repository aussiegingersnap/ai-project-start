# Understanding Cursor Project Rules (The Simple Version)

> *"Think of these rules as your personal AI trainer - they help your AI assistant understand exactly what you want."*

## What Are Cursor Project Rules?

Cursor Project Rules are simple text files that tell the AI how to help you. They're like setting preferences for your AI assistant.

These rules files live in the `.cursor/rules/` folder and have the `.mdc` extension, which is just fancy talk for "special markdown files for Cursor."

## Why Use Rules?

Without rules, AI assistants might:
- Give you solutions that don't match your style
- Suggest overly complex approaches
- Miss important details about your project
- Be inconsistent in how they help you

With rules, your AI assistant becomes:
- More consistent
- Better at following your preferences
- More helpful with specific tasks
- Less likely to go off track

## The Rules Files (Explained Simply)

### 1. General Rules (general.mdc)

This file contains basic rules that apply to everything, like:
- How to format code
- When to add comments
- How to handle errors
- General style preferences

**Think of it as:** Your AI's general manners and behavior

### 2. Frontend Rules (frontend.mdc)

This file has rules about creating websites and user interfaces:
- How to structure web pages
- How to handle user interactions
- How to style elements
- How to make sites load faster

**Think of it as:** Your AI's guide to making pretty websites

### 3. Backend Rules (backend.mdc)

This file contains rules about behind-the-scenes code:
- How to store data
- How to keep information secure
- How to handle user requests
- How to deal with errors

**Think of it as:** Your AI's instructions for building the engine behind your app

### 4. Agent Instructions (agent_instructions.mdc)

This file directly speaks to the AI about how it should behave:
- How to explain things to you
- When to ask questions
- How to break down complex problems
- What to prioritize

**Think of it as:** Your personal communication style guide for the AI

## How to Customize Rules (Even for Beginners)

You don't need to be a developer to tweak these rules! Here's how:

1. **Start small:** Change one simple instruction at a time
2. **Use plain language:** Write instructions as if explaining to a person
3. **Be specific:** "Make buttons blue" is better than "Use good colors"
4. **Test changes:** After changing a rule, ask the AI to do something related

### Simple Example:

Original rule in frontend.mdc:
```
- Use a consistent color palette
```

Your customized rule:
```
- Use these colors for all designs: #3366FF for buttons, #FFFFFF for backgrounds, and #333333 for text
```

## When Rules Aren't Working

If the AI isn't following your rules:

1. **Be more direct:** Try phrasing your request differently
2. **Remind the AI:** Say "Please follow the project rules"
3. **Simplify:** Your rules might be too complex or contradictory
4. **Check location:** Make sure your rules files are in the right folder

---

*Remember: The AI is here to help YOU. These rules are just a way to help it understand what you want, not to make things complicated!* 