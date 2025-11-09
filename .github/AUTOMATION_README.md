# GitHub Automation & CrewAI Integration

This repository includes comprehensive automation for issue management, PR triage, and AI-powered documentation review.

## Overview

### Automated Workflows

1. **Issue Triage** (`issue-triage.yml`)
   - Auto-labels issues based on content
   - Assigns priority levels
   - Links to relevant standards
   - Adds helpful comments

2. **Project Automation** (`project-automation.yml`)
   - Syncs issues to project boards
   - Updates PR status automatically
   - Links PRs to related issues
   - Manages stale issues

3. **PR Labeler** (`pr-labeler.yml`)
   - Labels PRs based on changed files
   - Categorizes by standards domain
   - Adds size labels
   - Provides review checklist

4. **CrewAI Review** (`crewai-review.yml`)
   - AI-powered documentation review
   - Specialized agents for different domains
   - Legal compliance checking
   - Security analysis
   - Technical accuracy validation

5. **Documentation Validation** (`documentation-validation.yml`)
   - Validates markdown syntax
   - Checks for broken links
   - Ensures _meta.md completeness
   - Generates documentation index

## CrewAI Agents

Our AI crew consists of specialized agents:

### 1. Legal Compliance Specialist
- Reviews for legal compliance
- Checks regulatory requirements
- Validates policy adherence
- Identifies licensing issues

### 2. Technical Documentation Expert
- Ensures clarity and completeness
- Checks consistency
- Validates technical accuracy
- Reviews structure and formatting

### 3. Software Architecture Reviewer
- Evaluates best practices
- Assesses scalability
- Reviews performance implications
- Checks maintainability

### 4. Security Standards Specialist
- Identifies security gaps
- Reviews security practices
- Checks compliance standards
- Suggests risk mitigation

### 5. AI Ethics and Safety Specialist
- Reviews ethical considerations
- Identifies potential bias
- Ensures safety measures
- Validates transparency

## Setup Instructions

### Prerequisites

1. **GitHub Secrets Required:**
   - `GITHUB_TOKEN` (automatically provided)
   - `OPENAI_API_KEY` (for CrewAI functionality)

2. **Repository Settings:**
   - Enable GitHub Actions
   - Enable Issues
   - Enable Projects (optional but recommended)

### Configuration

#### 1. Set up OpenAI API Key

For CrewAI to work, add your OpenAI API key:

```bash
# In your repository settings:
Settings → Secrets and variables → Actions → New repository secret
Name: OPENAI_API_KEY
Value: your-api-key-here
```

#### 2. Create Labels

Run this script to create all required labels:

```bash
# Create labels using GitHub CLI
gh label create "category:infrastructure" --color "0E8A16" --description "Infrastructure related"
gh label create "category:systems" --color "1D76DB" --description "Systems related"
gh label create "category:software" --color "5319E7" --description "Software related"
gh label create "category:ai-automation" --color "D93F0B" --description "AI and Automation"
gh label create "category:governance" --color "0052CC" --description "Governance and compliance"
gh label create "category:security" --color "B60205" --description "Security related"
gh label create "category:documentation" --color "0075CA" --description "Documentation"

gh label create "priority:high" --color "D93F0B" --description "High priority"
gh label create "priority:medium" --color "FBCA04" --description "Medium priority"
gh label create "priority:low" --color "0E8A16" --description "Low priority"

gh label create "type:bug" --color "D73A4A" --description "Bug report"
gh label create "type:enhancement" --color "A2EEEF" --description "Enhancement request"
gh label create "type:question" --color "D876E3" --description "Question"
gh label create "type:documentation" --color "0075CA" --description "Documentation"
gh label create "type:automation" --color "EDEDED" --description "Automation"
gh label create "type:metadata" --color "C5DEF5" --description "Metadata changes"

gh label create "size:small" --color "C2E0C6" --description "Small changes"
gh label create "size:medium" --color "FEF2C0" --description "Medium changes"
gh label create "size:large" --color "F9D0C4" --description "Large changes"

gh label create "status:stale" --color "EDEDED" --description "Stale issue or PR"
gh label create "status:blocked" --color "D93F0B" --description "Blocked"

gh label create "standards:global" --color "1D76DB" --description "Global standards"
gh label create "standards:infrastructure" --color "0E8A16" --description "Infrastructure standards"
gh label create "standards:systems" --color "5319E7" --description "Systems standards"
gh label create "standards:software" --color "FBCA04" --description "Software standards"
gh label create "standards:ai-automation" --color "D93F0B" --description "AI/Automation standards"
gh label create "standards:governance" --color "0052CC" --description "Governance standards"
```

#### 3. Enable Workflows

All workflows are enabled by default. To disable specific ones:
1. Go to Actions tab
2. Select the workflow
3. Click "Disable workflow"

## Usage

### For Issues

When you create an issue:
1. Title and description are automatically analyzed
2. Labels are applied based on content
3. Priority is assigned
4. Relevant standards are linked
5. Recommendations are provided

### For Pull Requests

When you create a PR:
1. Changed files are analyzed
2. Appropriate labels are added
3. Size is calculated
4. Review checklist is provided
5. Related standards are linked
6. CrewAI review is triggered (if markdown files changed)

### Manual Triggers

Some workflows can be triggered manually:

```bash
# Trigger CrewAI review
gh workflow run crewai-review.yml

# Trigger documentation validation
gh workflow run documentation-validation.yml
```

## Cost Considerations

### API Usage

CrewAI workflows use OpenAI API which incurs costs:
- Review triggered per PR with .md changes
- Reviews first 3 changed files
- Estimated cost: $0.01-0.10 per PR (depending on file size)

To reduce costs:
- Limit CrewAI to important PRs
- Adjust file content truncation (currently 2000 chars)
- Use workflow_dispatch for manual triggers only

### GitHub Actions Minutes

Free tier includes:
- 2,000 minutes/month (public repos get unlimited)
- Each workflow run consumes minutes

## Troubleshooting

### CrewAI Not Running

1. Check OpenAI API key is set correctly
2. Verify Python dependencies install successfully
3. Check workflow logs for errors
4. Ensure markdown files were changed

### Labels Not Applied

1. Verify label creation script was run
2. Check workflow permissions
3. Review issue/PR content for keywords

### Project Board Not Syncing

1. Configure PROJECT_ID in project-automation.yml
2. Check GitHub token permissions
3. Verify project exists and is accessible

## Customization

### Adding New Categories

Edit `issue-triage.yml` and `pr-labeler.yml`:

```yaml
categoryMap:
  'your-category': ['keyword1', 'keyword2']
```

### Modifying CrewAI Agents

Edit `crewai-review.yml` in the crew_config.py section:

```python
new_agent = Agent(
    role='Your Role',
    goal='Your Goal',
    backstory='Your Backstory',
    verbose=True
)
```

### Adjusting Stale Timeouts

Edit `project-automation.yml`:

```yaml
days-before-stale: 60  # Change this
days-before-close: 7   # Change this
```

## Best Practices

1. **Review Automation Output**: Always review auto-applied labels
2. **Adjust as Needed**: Customize workflows for your needs
3. **Monitor Costs**: Keep track of API usage
4. **Update Keywords**: Keep keyword lists current
5. **Provide Feedback**: Improve automation based on results

## Contributing

To improve automation:
1. Test changes in a fork first
2. Document new features
3. Update this README
4. Add examples where helpful

## Support

For issues with automation:
1. Check workflow logs in Actions tab
2. Review troubleshooting section
3. Open an issue with `type:automation` label
4. Include relevant logs and error messages
