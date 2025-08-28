# Contributing to EnnovateX AI Platform

Thank you for your interest in contributing to the EnnovateX AI Platform! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ennovatex-ai-platform-redesign.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `npm install`
5. Start the development server: `npm run dev`

## Development Guidelines

### Code Style
- Follow the existing code style and conventions
- Use TypeScript for all new code
- Run `npm run lint` before committing
- Ensure all TypeScript types are properly defined

### Commit Messages
- Use clear, descriptive commit messages
- Follow the format: `type(scope): description`
- Examples:
  - `feat(ui): add Samsung logo integration`
  - `fix(demo): resolve multimodal processing issue`
  - `docs(readme): update feature list`

### Testing
- Ensure your code builds successfully: `npm run build`
- Test your changes across different screen sizes
- Verify TypeScript compilation: `npx tsc --noEmit`

### Pull Request Process

1. Update the README.md if you've made significant changes
2. Ensure your code follows the project's coding standards
3. Make sure all tests pass and the build succeeds
4. Create a pull request with a clear title and description
5. Link any related issues in your PR description

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
├── components/          # Reusable React components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
└── visual-edits/       # Visual editing components
```

## Key Features to Maintain

- **Samsung Branding**: Preserve Samsung logo integration
- **Floating Navigation**: Maintain consistent navigation across pages
- **Performance**: Keep bundle sizes optimized
- **Accessibility**: Ensure WCAG compliance
- **Responsive Design**: Test on all device sizes

## Reporting Issues

- Use the provided issue templates
- Include steps to reproduce for bugs
- Provide context and use cases for feature requests

## Questions?

Feel free to open an issue for any questions about contributing!