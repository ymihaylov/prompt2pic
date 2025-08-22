# AI Image Generator

A modern React application for generating AI images with an intuitive chat-based interface.

## Features

- **Chat-based Interface**: Conversational UI for describing your business and image requirements
- **Multiple AI Models**: Support for GPT-4, GPT-3.5-turbo, Claude-3 for text processing
- **Image Generation**: Integration with DALL-E 3, Stable Diffusion XL, and Midjourney
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Accessibility**: Full keyboard navigation and screen reader support
- **Real-time Updates**: Loading indicators and smooth animations

## Layout Structure

### Header
- Fixed header with dark theme (#363737)
- Logo display (40px height)
- Centered "AI Image Generator" title
- User menu placeholder

### Chat Container
- Scrollable message history
- User and assistant message cards
- Image thumbnail gallery
- Download functionality

### Input Controls
- Full-width business description textarea
- Model selection dropdowns (LLM and Image models)
- Gallery image count selector (1-15)
- Generate button with loading states

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Component Structure

```
src/
├── components/
│   ├── Header.js
│   ├── ChatContainer.js
│   ├── MessageList.js
│   ├── UserMessage.js
│   ├── AssistantMessage.js
│   ├── InputArea.js
│   ├── BusinessDescriptionInput.js
│   ├── ModelSelectors.js
│   └── GenerateButton.js
├── styles/
│   ├── Header.css
│   ├── Chat.css
│   └── InputArea.css
├── App.js
├── App.css
└── index.js
```

## Features in Detail

### Model Selection
- **LLM Models**: GPT-4, GPT-3.5-turbo, Claude-3
- **Image Models**: DALL-E 3, Stable Diffusion XL, Midjourney
- **Gallery Options**: 1-15 images per generation

### User Experience
- Auto-resizing textarea for business descriptions
- Keyboard shortcuts (Ctrl/Cmd + Enter to generate)
- Real-time form validation
- Loading states with spinners
- Smooth scrolling to new messages
- Image hover effects

### Responsive Design
- Mobile-first approach
- Touch-friendly button sizes
- Stacked layout on mobile devices
- Responsive image grids

### Accessibility
- ARIA labels for all interactive elements
- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Focus management

## Color Scheme

- **Background**: #212121 (Dark gray)
- **Cards/Header**: #363737 (Medium gray)
- **Accent**: #a6adff (Light purple)
- **Text**: White with various opacities
- **Borders**: #4a5568 (Blue-gray)

## Available Scripts

### `npm start`
Runs the app in development mode on [http://localhost:3000](http://localhost:3000)

### `npm test`
Launches the test runner in interactive watch mode

### `npm run build`
Builds the app for production to the `build` folder

### `npm run eject`
**Note: This is a one-way operation!** Ejects from Create React App configuration

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
