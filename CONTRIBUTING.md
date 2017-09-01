# Contributing

## Introduction

This document describes what is a good contribution and why is that so.

Contributions with negligible impact can skip certain (or all) of these guidelines. Apply them with care.

A contribution is any amount of change provided to a project. It can come in many different shapes, including but not limited to:

- adding a feature,
- fixing an issue,
- removing a typo,
- improving the documentation,
- removing dead code or
- refactoring a module.

Sometimes removing, restructuring or improving is as important as adding new things. This applies to both code and documentation.

A good contribution is serviceable without the need of the original contributor.

## Who

Two actors come into play::

- the contributor
- one (or more) reviewers

**All** parties involved must ensure the quality of the contribution. The reviewers own the code as much as the contributor. They must work together to enforce these guidelines.

The contributor must enable an easy review. Following this guidelines is a first step. Keeping the contribution small helps. Try to keep it below 300 lines added and removed.

## What

Depending on the kind of contribution, it should include one or more of the following items:

- [Code](#code)
- [Tests](#tests)
- [Documentation](#documentation)

### Code

#### Why

Production code is what makes software produce value. It addresses business needs or serves as a basis for code that does.

#### How

The code **must** fulfill the original requirements.

Any team member should be able to understand it: it should be clear on _what_ it does and _how_. Use (a lot) of comments to explain _why_ a certain solution was (or was not) chosen.

The code must be well-structured. Well-structured code is easy to change, reuse and test.

Apply patterns from the discipline of practical programming. Reduce the scope to think about to make reasoning easy. Isolate and decouple. Use pure functions as much as you can. Push side effects to the boundaries of the system.

#### When

These are examples of contribution that should include production code:

- Adding a feature
- Fixing an issue
- Removing dead code
- Refactoring a module

[Back to top](#contributing)

### Tests

#### Why

Production code defines behavior. Static checking can prove this behavior to be sound, to a certain extent. Use tests to prove that your software behaves as expected at runtime, even for edge cases. Property-based testing can help.

Code that is simple to test is also well-structured. Use tests as a feedback tool for the quality of your code.

#### How

**All** requirements for production code hold for test as well. They **must** be understandable, well commented and clean.

Tests should cover as many relevant execution paths from production code as possible.

If a component is complex to test, it can be a sign that it's not well structured. Unit test isolated components and use integration tests to verify their interactions.

#### When

- Adding a feature
- Removing dead code
- Fixing an issue

[Back to top](#contributing)

### Documentation

Documentation is **as important as** production code and tests, if not more. It makes design, motivations and usage guidelines available for everybody at any time.

Document design and interfaces for developers.

Document usage for end users.

#### How

Documentation can be a contribution in itself. Code contributions that make the documentation obsolete must include the needed updates.

Documentation should come in plain text encoding. This enables documentation to come along with code contributions.

The format should enable automated rendering of the documentation as a rich document. Markdown and reStructuredText are examples.

Diagrams and plots can help understanding. The contributor should leverage the format to enrich the document with visual aids. Text-based image formats enable the review of visual aids. SVG is an example.

If someone asks about an undocumented behavior, it may be a hint on how to update the documentation.

#### When

- Adding or removing a feature
- Fixing an issue, if mentioned in the documentation
- Improving the documentation

[Back to top](#contributing)
