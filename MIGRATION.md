# Migration Guide: v1.0 → v2.0

## Overview

Trello CLI has been migrated from a single monolithic file to a modular, production-ready Python package.

## What Changed

### File Structure

**Before (v1.0):**
```
~/trello-cli.py          # Single 265-line file
~/.trello_config.json    # Config file
```

**After (v2.0):**
```
~/Documents/trello-cli-python/    # Project directory
├── trello_cli/                   # Python package
│   ├── commands/                 # Command modules
│   ├── utils/                    # Utilities
│   ├── cli.py                    # Main CLI
│   ├── client.py                 # API client
│   └── config.py                 # Config management
├── tests/                        # Test suite
├── examples/                     # Usage examples
├── trello                        # Main executable
└── README.md                     # Documentation

~/.trello_config.json            # Config (same location)
```

### Access Methods

**v1.0:**
```bash
# Direct script execution
~/trello-cli.py boards
python3 ~/trello-cli.py boards

# Via alias (if configured)
trello boards
```

**v2.0:**
```bash
# Via PATH (recommended)
trello boards

# Direct execution
~/Documents/trello-cli-python/trello boards

# Backward compatibility alias
trello-cli.py boards  # → redirects to 'trello'
```

## Migration Steps

### 1. Cleanup (Already Done)

```bash
# Old files removed:
rm ~/trello-cli.py
rm ~/trello-cli.py.backup
```

### 2. Updated PATH Configuration

**.zshrc changes:**
```bash
# OLD:
export PATH="$HOME:$HOME/.local/bin:$PATH"
alias trello="trello-cli.py"

# NEW:
export PATH="$HOME/Documents/trello-cli-python:$PATH"
alias trello="trello"
alias trello-cli.py="trello"  # Backward compatibility
```

### 3. Reload Shell Configuration

```bash
source ~/.zshrc
```

### 4. Verify Installation

```bash
# Check version
trello --version
# Output: Trello CLI v2.0.0

# Check path
which trello
# Output: /Users/bernardurizaorozco/Documents/trello-cli-python/trello

# Test command
trello boards
```

## Backward Compatibility

### All Existing Commands Work Identically

```bash
# These commands have NOT changed:
trello boards
trello lists <board_id>
trello cards <list_id>
trello add-card <list_id> "Title" "Description"
trello add-label <card_id> "color" "name"
trello set-due <card_id> "2025-11-01"
trello add-comment <card_id> "Comment"
trello move-card <card_id> <list_id>
```

### Scripts Using `trello-cli.py` Continue to Work

Thanks to the alias:
```bash
# OLD scripts using this:
python3 ~/trello-cli.py boards

# Now work via alias:
trello-cli.py boards
```

### Programmatic Usage (New Feature)

**v2.0 adds Python module import:**
```python
from trello_cli.client import get_client

client = get_client()
boards = client.list_boards()
```

## Configuration

### No Changes Required

`.trello_config.json` remains in the same location:
```
~/.trello_config.json
```

Format unchanged:
```json
{
  "api_key": "your_key",
  "token": "your_token"
}
```

## Updated Scripts

### Scripts That Reference Trello CLI

If you have scripts that use the full path, update them:

**Before:**
```bash
#!/bin/bash
TRELLO_CLI="/Users/bernardurizaorozco/trello-cli.py"
python3 $TRELLO_CLI boards
```

**After:**
```bash
#!/bin/bash
# Option 1: Use command directly (recommended)
trello boards

# Option 2: Use full path
TRELLO_CLI="/Users/bernardurizaorozco/Documents/trello-cli-python/trello"
$TRELLO_CLI boards
```

### Example: Aurity Import Script

If you have scripts like `import_aurity_csv.py`:

**Update path reference:**
```python
# OLD:
TRELLO_CLI = "/Users/bernardurizaorozco/trello-cli.py"

# NEW (recommended):
TRELLO_CLI = "trello"  # Use from PATH

# NEW (explicit):
TRELLO_CLI = "/Users/bernardurizaorozco/Documents/trello-cli-python/trello"
```

## New Features in v2.0

### Better Error Messages

```bash
# v1.0
Configuration file not found. Run 'trello config' first.

# v2.0
❌ Configuration file not found.
   Run 'trello config' to set up API credentials.
```

### Enhanced Output

```bash
# Card creation
✅ Card created: PF-FEAT-001: New Feature
   ID: 68fd24640bf4
   List: To Do (Sprint)

# Label addition
✅ Label 'P0' (red) added to card PF-FEAT-001
```

### Validation

```bash
# Invalid color
❌ Invalid color: pink
   Valid colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime

# Invalid date
❌ Invalid date format: 2025-13-01
   Expected: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
```

## Testing

### Verify Migration Success

Run these commands to confirm everything works:

```bash
# 1. Check version
trello --version
# Expected: Trello CLI v2.0.0

# 2. Check help
trello --help
# Expected: Full help text with all commands

# 3. List boards
trello boards
# Expected: Table of your Trello boards

# 4. Check backward compatibility
trello-cli.py --version
# Expected: Trello CLI v2.0.0

# 5. Test a real command
trello lists <your_board_id>
# Expected: Table of lists in that board
```

## Rollback (If Needed)

If you need to rollback to v1.0:

```bash
# 1. Restore backup
cp ~/trello-cli.py.backup ~/trello-cli.py
chmod +x ~/trello-cli.py

# 2. Update .zshrc
# Change:
#   export PATH="$HOME/Documents/trello-cli-python:$PATH"
# Back to:
#   export PATH="$HOME:$HOME/.local/bin:$PATH"

# 3. Reload
source ~/.zshrc
```

**Note:** Backup was already removed. If needed, restore from git:
```bash
cd ~/Documents/trello-cli-python
git show 739ad49:trello-cli.py > ~/trello-cli.py.backup
```

## Benefits of v2.0

### For Users

- ✅ Better error messages with emoji indicators
- ✅ Input validation prevents mistakes
- ✅ Cleaner output formatting
- ✅ Backward compatible (no breaking changes)
- ✅ Better documentation

### For Developers

- ✅ Modular code (easier to maintain)
- ✅ Test suite included
- ✅ Example scripts provided
- ✅ Programmatic API available
- ✅ Git repository with history

### For DevOps

- ✅ Scriptable with proper exit codes
- ✅ CI/CD friendly
- ✅ PATH-based installation
- ✅ No hardcoded paths

## Support

### Issues After Migration

1. **Command not found:**
   ```bash
   source ~/.zshrc
   which trello
   ```

2. **Old path references:**
   - Update scripts to use `trello` directly
   - Or update path to new location

3. **Configuration lost:**
   - Config is preserved at `~/.trello_config.json`
   - If missing, run `trello config`

### Getting Help

- **README:** `~/Documents/trello-cli-python/README.md`
- **Project Summary:** `~/Documents/trello-cli-python/PROJECT_SUMMARY.md`
- **Contributing:** `~/Documents/trello-cli-python/CONTRIBUTING.md`
- **GitHub Issues:** https://github.com/bernardurizaorozco/trello-cli-python/issues

---

**Migration Date:** 2025-10-25
**Version:** v1.0 → v2.0
**Status:** ✅ Complete
