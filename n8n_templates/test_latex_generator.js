// Test script to demonstrate the LaTeX resume generator
const fs = require('fs');
const path = require('path');

// Read the sample input
const sampleInput = JSON.parse(fs.readFileSync('sample_input.json', 'utf8'));

// Simulate n8n $input.all()[0].json
const $input = {
  all: () => [{ json: sampleInput }]
};

// Load and execute the n8n JavaScript code
const n8nCode = fs.readFileSync('latex_resume_generator.js', 'utf8');

// Extract just the function definitions and execution logic
// (In actual n8n, this would be handled by the platform)
const codeToExecute = n8nCode.replace(/\/\/ n8n execution context[\s\S]*$/, '');

// Execute the code
eval(codeToExecute);

// Simulate the n8n execution
const inputData = $input.all()[0].json;
const latexResume = generateLatexResume(inputData);

const result = {
  json: {
    latex_content: latexResume,
    timestamp: new Date().toISOString(),
    fit_score: inputData.fit_score || 0
  }
};

// Save the generated LaTeX to a file
fs.writeFileSync('generated_resume.tex', result.json.latex_content);

console.log('✅ LaTeX resume generated successfully!');
console.log('📄 Output saved to: generated_resume.tex');
console.log(`📊 Fit Score: ${result.json.fit_score}%`);
console.log(`🕒 Generated at: ${result.json.timestamp}`);

// Display a preview of the generated content
console.log('\n📋 Preview of generated LaTeX (first 500 characters):');
console.log('─'.repeat(50));
console.log(result.json.latex_content.substring(0, 500) + '...');
console.log('─'.repeat(50));