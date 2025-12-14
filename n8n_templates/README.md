# LaTeX Resume Generator for n8n

This n8n workflow component generates a LaTeX resume from structured JSON data while properly handling escape characters to ensure valid LaTeX output.

## Overview

The solution includes:
- **Main n8n Code**: `latex_resume_generator.js` - The JavaScript code to use in an n8n Code node
- **Sample Input**: `sample_input.json` - Example JSON data matching your schema
- **Test Script**: `test_latex_generator.js` - Node.js script to test the functionality locally

## JSON Schema

The code expects input data matching this schema:

```json
{
  "key_skills": ["skill1", "skill2", ...],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name", 
      "duration": "Start -- End",
      "highlights": ["achievement1", "achievement2", ...]
    }
  ],
  "education": "Education description",
  "fit_score": 85
}
```

## n8n Workflow Setup

### 1. Create a Code Node

1. Add a **Code** node to your n8n workflow
2. Set the **Mode** to "Run Once for All Items"
3. Copy the entire content from `latex_resume_generator.js` into the code editor

### 2. Input Requirements

The code expects the input data to be available in `$input.all()[0].json`. Ensure your previous node outputs data in the correct format.

### 3. Output

The node returns:
```json
{
  "latex_content": "Complete LaTeX resume content",
  "timestamp": "2025-11-07T...",
  "fit_score": 92
}
```

## Key Features

### 🔒 LaTeX Escape Handling
The code properly escapes all LaTeX special characters:
- `&` → `\\&`
- `%` → `\\%`
- `$` → `\\$`
- `#` → `\\#`
- `^` → `\\textasciicircum{}`
- `_` → `\\_`
- `{` → `\\{`
- `}` → `\\}`
- `~` → `\\textasciitilde{}`
- `\\` → `\\textbackslash{}`

### 🏗️ Dynamic Content Generation
- **Experience Section**: Automatically formats all job experiences with highlights
- **Skills Section**: Intelligently categorizes skills into Languages, Tools, and Frameworks
- **Education**: Dynamically inserts education information
- **Fit Score**: Adds the fit score to achievements section

### 🎯 Template Preservation
- Maintains the exact LaTeX structure and formatting of your original resume
- Preserves all custom commands and styling
- Keeps the professional layout intact

## Testing Locally

To test the functionality before deploying to n8n:

```bash
cd n8n_templates
node test_latex_generator.js
```

This will:
1. Load the sample input data
2. Execute the LaTeX generation code
3. Save the output to `generated_resume.tex`
4. Display a preview and statistics

## Workflow Integration Examples

### Example 1: Simple Data Input
```
Manual Trigger → Set Node (with JSON data) → Code Node (LaTeX Generator) → File Write
```

### Example 2: API Integration
```
Webhook → Data Processing → Code Node (LaTeX Generator) → Email/File Storage
```

### Example 3: Database Integration
```
Schedule Trigger → Database Query → Data Transform → Code Node (LaTeX Generator) → Cloud Storage
```

## Customization Options

### Adding New Sections
To add new sections to the resume, modify the `generateLatexResume` function:

```javascript
// Add after the education section
const customSection = `
\\section{Custom Section}
  \\resumeItemListStart
    \\resumeSubItem{${escapeLatex(data.custom_field)}}
  \\resumeItemListEnd
`;
```

### Modifying Skills Categorization
Update the `generateTechnicalSkills` function to change how skills are categorized:

```javascript
// Modify the categorization logic
if (lowerSkill.includes('your_keyword')) {
  customCategory.push(escapeLatex(skill));
}
```

### Changing Personal Information
Update the header section in the template with dynamic data:

```javascript
// Replace static information with dynamic data
\\begin{center}
    {\\Huge \\scshape ${escapeLatex(data.name || 'Kaustav Chanda')}} \\\\ \\vspace{1pt}
    ${escapeLatex(data.title || 'Senior Software Engineer')} \\\\ \\vspace{1pt}
    ...
\\end{center}
```

## Error Handling

The code includes robust error handling:
- Null/undefined checks for all data fields
- Fallback values for missing information
- Graceful handling of empty arrays
- Default skills if none provided

## Compilation

To compile the generated LaTeX:

```bash
pdflatex generated_resume.tex
```

Make sure you have a LaTeX distribution installed (e.g., TeX Live, MiKTeX).

## Troubleshooting

### Common Issues

1. **Missing Data Fields**: The code provides fallback values for all required fields
2. **Special Characters**: All special characters are properly escaped
3. **Empty Arrays**: The code handles empty experience/skills arrays gracefully
4. **Encoding Issues**: Use UTF-8 encoding for all input data

### Debug Mode

Add debugging output to the code:

```javascript
console.log('Input data:', JSON.stringify(inputData, null, 2));
console.log('Generated experience section:', experienceSection);
```

## License

This code is based on the MIT-licensed LaTeX resume template by Jake Gutierrez.