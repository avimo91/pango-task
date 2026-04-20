# AI Reflection

## Overall Approach and Key Decisions

I began with manual exploration of the Parkly application, mapping the core user flows and identifying risk areas. I structured my test plan around three priorities: business logic correctness, data isolation between users, and input validation. Visual and UX issues were noted during exploration but were treated as lower priority compared to functional and security-related risks.

For automation, I invested in a layered POM architecture: Extensions for Selenium wrappers, Page Objects for locators and UI actions, Workflows for business logic, and Tests for assertions only. This ensures the suite is maintainable and scalable even at small size.

## Trade-offs

I invested significant time in the test plan - mapping risks, documenting bugs with clear reproduction steps, and thinking through edge cases. In hindsight, I could have managed my time differently: allocating less time to the test plan and more to the automation phase.

Rather than rushing to add more test scenarios at the cost of quality, I chose to deliver two stable, well-structured tests that run reliably. I believe a focused suite that runs cleanly reflects better judgment than a broader suite with fragile results.

Given better time management, I would have delivered a more complete automation suite - covering the full E2E parking lifecycle (start, end, verify in history), adding a regression test for the duplicate slot bug (BUG-01), and applying an even cleaner separation between UI actions, business workflows, and test assertions.

## AI Tools Used

- **Claude** - primary tool throughout: exploration, test plan, code generation, architecture, debugging
- **ChatGPT and Gemini** - used in parallel for second opinions and phrasing

## Reasoning Behind Tool Choices

Claude maintained full context across the entire working session, which made it effective for generating accurate, project-specific code. Using multiple AI tools in parallel helped cross-check decisions and avoid over-relying on a single model's perspective.

For deterministic regression automation, Selenium remains the more reliable choice over AI-based browser agents, which introduce variability that conflicts with the stability requirements of a test suite.
