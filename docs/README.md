# Trello CLI Documentation

Complete documentation for the Trello CLI project.

## 📚 Table of Contents

### For Users

- **[Main README](../README.md)** - Installation and quick start
- **[Claude Code Integration Guide](../CLAUDE.md)** - Essential guide for AI assistants

### For Developers

- **[Development Guides](./development/)**
  - [Project Summary](./development/PROJECT_SUMMARY.md) - Architecture and technical details
  - [Contributing Guide](./development/CONTRIBUTING.md) - How to contribute
  - [Migration Guide](./development/MIGRATION.md) - v1.0 → v2.0 migration
  - [Testing Guide](./TESTING_GUIDE.md) - Pytest setup and best practices
  - [Reporting Guide](./REPORTING_GUIDE.md) - Export reports to HTML/PDF

### Additional Resources

- **[Claude Code Guides](./guides/)**
  - [Claude Integration](./guides/CLAUDE_INTEGRATION.md) - Detailed integration guide

- **[Marketing Materials](./marketing/)**
  - [LinkedIn Post](./marketing/LINKEDIN_POST.md) - Announcement post
  - [Promotion](./marketing/PROMOTION.md) - Promotional content
  - [Claude MD Snippet](./marketing/CLAUDE_MD_SNIPPET.md) - Reusable snippets

## 🚀 Quick Links

### Essential Commands

```bash
# Get all commands
trello help-json

# Discovery
trello board-overview <board_id>
trello board-ids <board_id>
trello search-cards <board_id> "query"

# Quick workflows
trello quick-start <card_id>
trello quick-test <card_id>
trello quick-done <card_id>

# Sprint management
trello sprint-start <board_id>
trello sprint-status <board_id>
trello sprint-close <board_id>

# Board standardization
trello list-templates
trello standardize-lists <board_id> agile
trello scrum-check <board_id>
```

### Command Categories

1. **Discovery Commands** (5) - Explore boards and find information
2. **Quick Commands** (5) - Shortcuts for common workflows
3. **Sprint Planning** (4) - Full sprint lifecycle management
4. **Bulk Operations** (5) - Process multiple cards at once
5. **Advanced Queries** (5) - Filter and analyze cards
6. **Board Standardization** (4) - Ensure Agile/Scrum conformity
7. **Basic CRUD** (15+) - Create, read, update, delete operations

**Total**: 48 commands

## 📖 Documentation Structure

```
docs/
├── README.md                    # This file
├── TESTING_GUIDE.md             # Testing and pytest setup
├── REPORTING_GUIDE.md           # Export reports to various formats
│
├── development/                 # For contributors
│   ├── PROJECT_SUMMARY.md       # Technical architecture
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   └── MIGRATION.md             # Version migration guide
│
├── guides/                      # User guides
│   └── CLAUDE_INTEGRATION.md    # Detailed Claude Code integration
│
└── marketing/                   # Promotional content
    ├── LINKEDIN_POST.md
    ├── PROMOTION.md
    └── CLAUDE_MD_SNIPPET.md
```

## 🎯 By Use Case

### I want to...

#### ...start using Trello CLI
→ See [README.md](../README.md)

#### ...use with Claude Code
→ See [CLAUDE.md](../CLAUDE.md)

#### ...contribute to the project
→ See [CONTRIBUTING.md](./development/CONTRIBUTING.md)

#### ...write tests
→ See [TESTING_GUIDE.md](./TESTING_GUIDE.md)

#### ...export reports
→ See [REPORTING_GUIDE.md](./REPORTING_GUIDE.md)

#### ...standardize my boards
→ Run `trello list-templates` and `trello standardize-lists`

#### ...check Agile conformity
→ Run `trello scrum-check <board_id>`

## 🆕 What's New in v2.1

### 29 New Commands!

- ✅ Quick workflow shortcuts
- ✅ Complete sprint planning lifecycle
- ✅ Bulk operations for multiple cards
- ✅ Advanced filtering and queries
- ✅ Board standardization with templates
- ✅ Agile/Scrum conformity validation

See [CLAUDE.md](../CLAUDE.md) for complete changelog.

## 🤝 Community

- **GitHub**: [bernardurizaorozco/trello-cli-python](https://github.com/bernardurizaorozco/trello-cli-python)
- **Issues**: [Report bugs or request features](https://github.com/bernardurizaorozco/trello-cli-python/issues)
- **Discussions**: Share ideas and ask questions

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

---

**Version**: 2.1.0
**Last Updated**: 2025-10-27
**Maintainer**: Bernard Uriza Orozco
