# AgentXen - Comprehensive Project Plan

## 🎯 Project Vision
An AI-powered browser agent built on Zen Browser that allows users to give natural language commands to perform web tasks autonomously.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           AgentXen UI (Zen Browser)             │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ Chat Window  │  │  Browser Tabs             │ │
│  │ (Task Input) │  │  - Agent Mode             │ │
│  │              │  │  - Manual Mode            │ │
│  └──────┬───────┘  └──────────────────────────┘ │
└─────────┼──────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│         AI Agent Controller Layer               │
│  - Natural Language Understanding               │
│  - Task Planning & Execution                    │
│  - Browser Action Translation                   │
└─────────┬───────────────────────────────────────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌─────────┐  ┌──────────────┐
│ Ollama  │  │  Playwright  │
│ (Small  │  │  (Browser    │
│  Model) │  │  Automation) │
└─────────┘  └──────────────┘
```

## 📦 Phase 1: Foundation & Research (Week 1)

### 1.1 Environment Setup
- [ ] Set up development environment
- [ ] Install dependencies (Node.js, Python, etc.)
- [ ] Configure Git workflow

### 1.2 Repository Analysis
- [ ] Clone Zen Browser repository
- [ ] Study Zen Browser build system
- [ ] Understand Firefox extension architecture
- [ ] Document customization points

### 1.3 Technology Integration Research
- [ ] Review Ollama API and local model options
- [ ] Study Playwright browser automation capabilities
- [ ] Research Firefox/Zen Browser WebExtension APIs
- [ ] Identify integration approach

## 📦 Phase 2: Core Infrastructure (Week 2-3)

### 2.1 Project Structure
```
agentxen/
├── src/
│   ├── agent/           # AI agent core logic
│   ├── browser/         # Browser integration
│   ├── ui/              # Chat interface
│   ├── automation/      # Playwright wrapper
│   └── models/          # Data models
├── extension/           # Browser extension files
├── ollama/              # Ollama integration
├── tests/
├── docs/
└── scripts/             # Build & deployment scripts
```

### 2.2 Ollama Integration
- [ ] Install and configure Ollama locally
- [ ] Select appropriate small model (e.g., Qwen3:4b, Llama3.2:3b)
- [ ] Create Ollama API wrapper
- [ ] Implement prompt templates for browser actions
- [ ] Test model response parsing

### 2.3 Playwright Integration
- [ ] Set up Playwright for Firefox
- [ ] Create browser action abstraction layer
- [ ] Implement core actions:
  - Navigate to URL
  - Click elements
  - Fill forms
  - Extract data
  - Take screenshots
  - Scroll page
- [ ] Build action queue system

## 📦 Phase 3: Agent Intelligence (Week 4-5)

### 3.1 Natural Language to Action Translation
- [ ] Design prompt engineering system
- [ ] Create action vocabulary/schema
- [ ] Implement task decomposition
- [ ] Build action validation system
- [ ] Add error handling & recovery

### 3.2 Agent Controller
- [ ] Task queue management
- [ ] State management
- [ ] Memory system (conversation context)
- [ ] Tool calling interface
- [ ] Action execution engine

### 3.3 Safety & Constraints
- [ ] Implement action allowlist
- [ ] Add user confirmation for sensitive actions
- [ ] Rate limiting
- [ ] Sandbox environment support

## 📦 Phase 4: Browser UI Integration (Week 6-7)

### 4.1 Zen Browser Modification
- [ ] Fork/customize Zen Browser
- [ ] Add WebExtension support for AgentXen
- [ ] Create custom build pipeline

### 4.2 Chat Interface
- [ ] Design chat UI mockups
- [ ] Implement chat window component
- [ ] Add message history
- [ ] Display agent actions/feedback
- [ ] Add input controls & suggestions

### 4.3 Tab Management
- [ ] Implement "Agent Mode" vs "Manual Mode" tabs
- [ ] Add tab state indicators
- [ ] Create tab creation/switching logic
- [ ] Build permission system

## 📦 Phase 5: MVP Features (Week 8-9)

### 5.1 Core Capabilities
- [ ] Web search
- [ ] Form filling
- [ ] Data extraction
- [ ] Multi-step workflows
- [ ] Screenshot & analysis

### 5.2 User Experience
- [ ] Onboarding flow
- [ ] Example tasks/templates
- [ ] Settings panel
- [ ] Keyboard shortcuts
- [ ] Visual feedback system

### 5.3 Testing & Quality
- [ ] Unit tests for core components
- [ ] Integration tests
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Bug fixing

## 📦 Phase 6: Polish & Release (Week 10)

### 6.1 Documentation
- [ ] User guide
- [ ] API documentation
- [ ] Developer setup guide
- [ ] Architecture documentation

### 6.2 Deployment
- [ ] Build release packages
- [ ] Create installation instructions
- [ ] Set up auto-update mechanism
- [ ] Prepare demo videos

## 🔧 Technology Stack

### Core Technologies
- **Browser**: Zen Browser (Firefox fork)
- **AI**: Ollama with Gemma 1B (ultra-lightweight, fast inference)
- **Automation**: Playwright for Firefox
- **Extension**: Firefox WebExtensions API

### Development Stack
- **Languages**: JavaScript/TypeScript, Python
- **Build**: Webpack/Vite, npm/yarn
- **Testing**: Jest, Playwright Test
- **UI Framework**: React/Vue (for chat interface)

### APIs & Libraries
- Ollama API (local)
- Playwright API
- Firefox WebExtension APIs
- Native Messaging API (for extension-to-agent communication)

## 🎯 MVP Success Criteria

1. ✅ User can open AgentXen and see chat interface
2. ✅ User can type natural language commands
3. ✅ Agent can perform basic actions:
   - Navigate to websites
   - Click buttons/links
   - Fill forms
   - Extract information
4. ✅ Agent provides feedback on actions taken
5. ✅ User can switch between agent-controlled and manual tabs
6. ✅ System runs on local machine without cloud dependencies

## 🚀 Future Enhancements (Post-MVP)

- Multi-tab coordination
- Session persistence
- Voice input
- Visual element selection
- Browser history integration
- Bookmark management
- Advanced web scraping
- API integration capabilities
- Custom action plugins

## ⚙️ Technical Considerations

### Model Selection Criteria
- **Size**: < 2GB (for fast inference)
- **Capabilities**: Instruction following, tool calling
- **Speed**: < 1s response time on average hardware
- **Selected Model**: **Gemma 1B** (optimized for speed and efficiency)
- **Alternative Candidates**: 
  - Qwen3:4b
  - Llama3.2:3b
  - Phi-4:3b

### Browser Communication Architecture
- Extension uses Native Messaging to communicate with local agent service
- Agent service runs Ollama and Playwright
- WebSocket for real-time updates to chat UI

### Security Model
- All computation local (no data sent to cloud)
- Action approval system for sensitive operations
- Sandboxed execution environment
- Clear permissions model

## 📊 Timeline Summary
- **Phase 1**: 1 week (Research & Setup)
- **Phase 2**: 2 weeks (Infrastructure)
- **Phase 3**: 2 weeks (Agent Intelligence)
- **Phase 4**: 2 weeks (UI Integration)
- **Phase 5**: 2 weeks (MVP Features)
- **Phase 6**: 1 week (Polish & Release)
- **Total**: ~10 weeks to MVP

## 📝 Notes
- Focus on MVP first, avoid feature creep
- Prioritize reliability over features
- Regular testing with real user scenarios
- Keep architecture modular for future extensions
