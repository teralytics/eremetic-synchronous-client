# Pull Request Template

_This template is the actionable counterpart of the contribution guidelines._

_For trivial changes feel free to disregard it._

_Remove template material (in italic font, like this) before opening the pull request._

---

This pull request addresses _#???_ and includes:

- [ ] Production code
- [ ] Testing code
- [ ] Documentation

## Description

_Describe the added feature and the design decisions involved. If there is a relevant design document please provide a reference to it._

_Describe how and why this is different from the original design, if that's the case._

_If any item is missing from the checklist above, state why, for example:_

- _"This is a bug fix that does not need to update documentation."_
- _"This is a documentation improvement that includes no code."_

## Review hints

The reviewer is responsible with checking that the pull request:

- adheres to the contribution guidelines
- is small in size and simple to review
- fulfills the original requirements
- checks correctness with unit and integration tests
- checks edge cases throughout tests
- preserves original design choices (or documents variations)
- contains understandable code and tests
- does not introduce unreasonable systemic complexity
- does not introduce unreasonable algorithmic complexity
- does not introduce hard-coded constants or magic numbers
- includes documentation for developers
- includes documentation for users

_State doubts that you want reviewers to pay extra attention to, for example:_

- _"I'm using a deprecated API, is this acceptable?"_
- _"I've implemented this helper myself, do we already have something like this in our libraries?"_

_State what parts of the pull request do not need to a review (generated code, for example)._

---

## Extra sections

_Add extra sections as required (and make sure to remove this placeholder)._
