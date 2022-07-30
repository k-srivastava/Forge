# Forge (Pygame Wrapper)

# What is Forge?

`Forge` is a game development library that aims to help novice developers make the 2D games and experiences of their dreams using a simple and opinionated library that wraps around `Pygame`.

## Features

- The USP of `Forge` is its powerful CLI, `Kiln` that allows the creation of new objects quickly and easily. It takes inspiration from the `Rails` CLI.
- A complete UI library within `Forge` called `Hearth` which is used to create complex UI elements in code using a system of constraints that make it resizable and applicable to a large variety of screen sizes. It takes inspiration from `UIKit` Constraints and ThinMatrix’s GUI library.
- Written in `Python`, a language that most novice developers already know basic concepts of, and is easy to pick up and get started with.
- Type-hints throughout the code for a better development experience.
- Extensive documentation generated using the `Sphinx` library.

## Why a new Library?

`Pygame` is an excellent library to start off with but there are a few key problems with it:

- It doesn't have the best development experience due to a lack of type-hints, good documentation and its general design.
- A lot of globals used throughout the code leading to various wildcard imports.
- The structure of aliases within the library can often confuse many autocomplete engines’ type systems.
- The code is not very well modularised leading to a difficulty in separation uses of various components. Each file becomes very long and difficult to work with.

The crux of the argument is that to many any serious project with `Pygame` requires the creation of another small library on its own.

<aside>
💡 Using `Pygame` for large projects is like using vanilla `JavaScript` for a large application. You end up making a small and terrible framework of your own at the end, anyway.

</aside>

## Why a Wrapper?

For all its demerits, there is one big reason why I am using `Pygame` over making something from scratch: it is cross-platform.

Making a game engine using `OpenGL` would lead to a greater flexibility, but would drastically increase the scope of the project. That would mean adding important features like the `Kiln` CLI and `Hearth` UI system would take far more time than is required.

While the scope of the project even as a wrapper is quite large, it’s use-case (a tool for novice developers) doesn't justify the extra overhead that a graphics API like `OpenGL` adds.

## What are the Changes?

In short, everything except `pygame.display` and `Pygame`’s main-loop and internal systems (events, timers, etc.) will be completely re-written for `Forge`. I will have a custom implementation for those internal systems. While Pygame will be a dependency for me, the ideal scenario involves the end-developer not realising that `Forge` under the hood, actually runs `Pygame`.

## Target Audience

`Forge` is designed for amateur developers that want something simpler than Unity or Godot for making simple 2D experiences but something with more depth and nuance than `Pygame`. `Pyglet` exposes more `OpenGL` than what I would be comfortable with.

`Forge` should not only create good games but also create a welcoming, fun and light development environment but still have enough depth to create more involved and complex experiences.

# Development Process

## Versioning

### `X.0.0`

A major version involves a completely new feature that requires a drastic change in current architecture. All the current features are planned with the current architecture in mind. At its current state, the project will stay on version `1.X.X`.

### `0.X.0`

A minor version involves a new feature that can be implemented using the current architecture. Each minor version creates a new GitHub branch.

### `0.0.X`

A tiny version involves new implementation of an existing feature or, bug fixes using existing architecture.

## Planning New Features

Spend two days on planning new features to be added to `Forge`. Think of all implementations, use-cases and future updates to it. Think of applications within current example projects and see whether they are actually useful or, reduce code complexity at all.

## Working on Architecture

Plan the architecture of the feature; the design patterns used, the way it interacts with current systems and how it will be exposed to the end-developer.

## Writing Tests

All new features will be implemented using a test-driven-development process for `Forge`. The basic empty implementation and abstraction methods will be implemented. Then, detailed tests for the feature will be written using the `unittest` module. The aim is for 100% coverage and then some.

The `ReStructuredText` documentation should also be added, even for tests, at this point.

## Implementation and Debugging

Finally, write the code to implement the feature. The aim is to keep the code easy to read and maintain. The files should be short and have a singular purpose. Modularise the code and efficiently pack it. No fancy techniques should be used unless absolutely required to achieve the desired output within certain constraints.

The `ReStructuredText` documentation should also be added at this point along with any single-line explanation comments, if required.

## CLI Integration

Integrate the feature, if applicable, with the `Kiln` CLI. The aim is for `Kiln` to be developed alongside `Forge Core` and not as a separate entity to avoid the package-within-a-package feel when using it. Kiln should feel like a natural extension of `Forge` and not like an additional, optional feature. CLI should be given first-class support.

## Final Debugging and Documentation

Undergo the final debugging process. No bugs should be shipped if I am aware of their existence. The release cycle may be pushed back but, the uploaded code should be in a completely usable state.

The `Sphinx` documentation should also be updated at this point.

## Commit and Push to Git Repository

Once the code has passed all unit tests and works as expected in the example project tests, it should be committed and pushed to a public Git repository. If a new feature is being introduced at this point, the correct branch should be created and checked out. Each branch on the repository should contain an internally complete project (however impractical it may be to use).

# Feature Details

## `Kiln` CLI

`Kiln` is the CLI for `Forge`. The trouble with simple game making tools is that often, developers are forced to re-write the same boilerplate classes with inheritance, and the same default methods as always.

`Kiln` massively simplifies this process by using simple command line arguments to create the Python files with custom boilerplate so that the developer can focus on the actual development and implementation details rather that being bogged down with the actual code. `Kiln` takes inspiration from the `Rails` CLI.

### Implementation Details

## `Hearth` UI

`Hearth` is the UI manager for `Forge`. UI is often an overlooked component of game making tools. Especially, in a 2D medium, the UI needs to scale, move with a display of custom dimensions and aspect ratios and look good while doing it.

Hearth uses basic shapes and custom versions of common UI components. The components that `Hearth` supports are:

- Container
- Panel
- Button
- Checkbox
- Slider
- List Items

The scaling is made possible by an advanced system of constraints that allow for the changing of component dimensions by changing the display or parent container sizes. It allows for the creation of complex and scalable UIs at multiple display sizes and aspect ratios. The constraints that `Hearth` supports are:

- 

Heart takes inspiration form Apple’s `UIKit` constraint system for its own implementation of constraints.

### Implementation Details

## Event System

### Implementation Details

## Physics System

`Forge` uses a basic Physics component library to simulate simple Physics-based experiences in 2D. `Pygame` already has a few Physics and Maths classes and implementations however, `Forge` shall not use either for its internal representation of Physics objects.

### Implementation Details
