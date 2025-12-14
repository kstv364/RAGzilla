// n8n JavaScript Code Node for LaTeX Resume Generation
// This code takes JSON data matching your schema and generates a LaTeX resume

// Function to escape LaTeX special characters
function escapeLatex(text) {
  if (!text) return '';
  
  return text
    .replace(/\\/g, '\\textbackslash{}')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/\$/g, '\\$')
    .replace(/&/g, '\\&')
    .replace(/%/g, '\\%')
    .replace(/#/g, '\\#')
    .replace(/\^/g, '\\textasciicircum{}')
    .replace(/_/g, '\\_')
    .replace(/~/g, '\\textasciitilde{}')
    .replace(/>/g, '\\textgreater{}')
    .replace(/</g, '\\textless{}');
}

// Function to format duration with proper escaping
function formatDuration(duration) {
  if (!duration) return '';
  return escapeLatex(duration.replace(/--/g, ' -- '));
}

// Function to generate experience section
function generateExperience(experiences) {
  if (!experiences || experiences.length === 0) return '';
  
  let experienceSection = '';
  
  experiences.forEach(exp => {
    const title = escapeLatex(exp.title || '');
    const company = escapeLatex(exp.company || '');
    const duration = formatDuration(exp.duration || '');
    
    experienceSection += `
    \\resumeSubheading
      {${company}}{${duration}}
      {${title}}{Kolkata, West Bengal}
      \\resumeItemListStart`;
    
    if (exp.highlights && exp.highlights.length > 0) {
      exp.highlights.forEach(highlight => {
        const escapedHighlight = escapeLatex(highlight);
        experienceSection += `
        \\resumeItem{${escapedHighlight}}`;
      });
    }
    
    experienceSection += `
      \\resumeItemListEnd
`;
  });
  
  return experienceSection;
}

// Function to generate technical skills section
function generateTechnicalSkills(keySkills) {
  if (!keySkills || keySkills.length === 0) {
    return `     \\textbf{Languages}{: C\\#, HTML/CSS, Typescript, JavaScript, SQL} \\\\
     \\textbf{Developer Tools}{: VS Code, Visual Studio, IntelliJ, Git, TFS} \\\\
     \\textbf{Technologies/Frameworks}{: .NET, Linux, Jenkins, Docker, Webpack, Github Actions} \\\\`;
  }
  
  // Group skills by categories (this is a simplified approach)
  const languages = [];
  const tools = [];
  const frameworks = [];
  
  keySkills.forEach(skill => {
    const lowerSkill = skill.toLowerCase();
    
    // Categorize skills based on common patterns
    if (lowerSkill.includes('c#') || lowerSkill.includes('javascript') || 
        lowerSkill.includes('typescript') || lowerSkill.includes('python') || 
        lowerSkill.includes('java') || lowerSkill.includes('html') || 
        lowerSkill.includes('css') || lowerSkill.includes('sql')) {
      languages.push(escapeLatex(skill));
    } else if (lowerSkill.includes('git') || lowerSkill.includes('docker') || 
               lowerSkill.includes('vs code') || lowerSkill.includes('visual studio') || 
               lowerSkill.includes('jenkins') || lowerSkill.includes('intellij')) {
      tools.push(escapeLatex(skill));
    } else {
      frameworks.push(escapeLatex(skill));
    }
  });
  
  // Fallback to default if categorization results in empty arrays
  if (languages.length === 0) languages.push('C\\#', 'HTML/CSS', 'Typescript', 'JavaScript', 'SQL');
  if (tools.length === 0) tools.push('VS Code', 'Visual Studio', 'IntelliJ', 'Git', 'TFS');
  if (frameworks.length === 0) frameworks.push('.NET', 'Linux', 'Jenkins', 'Docker', 'Webpack', 'Github Actions');
  
  return `     \\textbf{Languages}{: ${languages.join(', ')}} \\\\
     \\textbf{Developer Tools}{: ${tools.join(', ')}} \\\\
     \\textbf{Technologies/Frameworks}{: ${frameworks.join(', ')}} \\\\`;
}

// Main function to generate the complete LaTeX resume
function generateLatexResume(data) {
  const experienceSection = generateExperience(data.experience);
  const technicalSkillsSection = generateTechnicalSkills(data.key_skills);
  const educationSection = escapeLatex(data.education || 'Bachelor of Technology in Computer Science and Engineering');
  
  const latexTemplate = `%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\\documentclass[letterpaper,11pt]{article}

\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{fancyhdr}
\\usepackage[english]{babel}
\\usepackage{tabularx}
\\usepackage{fontawesome5}
\\usepackage{multicol}
\\setlength{\\multicolsep}{-3.0pt}
\\setlength{\\columnsep}{-1pt}
\\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \\usepackage[sfdefault]{FiraSans}
% \\usepackage[sfdefault]{roboto}
% \\usepackage[sfdefault]{noto-sans}
% \\usepackage[default]{sourcesanspro}

% serif
% \\usepackage{CormorantGaramond}
% \\usepackage{charter}


\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.6in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1.19in}
\\addtolength{\\topmargin}{-.7in}
\\addtolength{\\textheight}{1.4in}

\\urlstyle{same}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
  \\vspace{-4pt}\\scshape\\raggedright\\large\\bfseries
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\\pdfgentounicode=1

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[1]{
  \\item\\small{
    {#1 \\vspace{-2pt}}
  }
}

\\newcommand{\\classesList}[4]{
    \\item\\small{
        {#1 #2 #3 #4 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & \\textbf{\\small #2} \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubSubheading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\textit{\\small#1} & \\textit{\\small #2} \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeProjectHeading}[2]{
    \\item
    \\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\small#1 & \\textbf{\\small #2}\\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}

\\renewcommand\\labelitemi{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}
\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.0in, label={}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\\begin{document}

%----------HEADING----------
\\begin{center}
    {\\Huge \\scshape Kaustav Chanda} \\\\ \\vspace{1pt}
    Senior Software Engineer \\\\ \\vspace{1pt}
    \\small \\raisebox{-0.1\\height}\\faPhone\\ 9748802973 ~ \\href{mailto:kaustav.chanda.work@gmail.com}{\\raisebox{-0.2\\height}\\faEnvelope\\  \\underline{kaustav.chanda.work@gmail.com}} ~ 
    \\href{https://linkedin.com/in/kaustav-chanda}{\\raisebox{-0.2\\height}\\faLinkedin\\ \\underline{/LinkedIn}}  ~
    \\href{https://github.com/kstv364}{\\raisebox{-0.2\\height}\\faGithub\\ \\underline{/kstv364}} ~
     \\href{https://medium.com/@kstvkmrchanda2}{\\raisebox{-0.2\\height}\\faMedium\\ \\underline{/medium}}  ~
     \\href{https://www.hackerrank.com/profile/Kaustav97}{\\raisebox{-0.2\\height}\\faHackerrank\\ \\underline{/Kaustav97}} ~
    \\vspace{-8pt}
\\end{center}

%-----------EXPERIENCE-----------
\\section{Experience}
  \\resumeSubHeadingListStart
${experienceSection}
  \\resumeSubHeadingListEnd
\\vspace{-14pt}

%
%-----------PROGRAMMING SKILLS-----------
\\section{Technical Skills}
 \\begin{itemize}[leftmargin=0.15in, label={}]
    \\small{\\item{
${technicalSkillsSection}
    }}
 \\end{itemize}
 \\vspace{-16pt}

 
%-----------EDUCATION-----------
\\section{Education}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {Heritage Institute of Technology (DGPA - 8.95) }{July 2016 -- May 2020}
      {B. Tech in CSE} {Kolkata, West Bengal} \\\\
   
  \\resumeSubHeadingListEnd

%-----------INVOLVEMENT---------------
\\section{Achievements}
    \\resumeItemListStart
        \\resumeSubItem{Won the Hyland SPOT award 2021, 2023.}
        \\resumeSubItem{NASA Space Apps Challenge 2017 Finalist.}
        \\resumeSubItem{School Topper in Mathematics}
        \\resumeSubItem{Candidate Fit Score: ${data.fit_score || 0}\\%}
    \\resumeItemListEnd

\\end{document}`;

  return latexTemplate;
}

// n8n execution context
// Assuming the input data comes from previous node as $json

// Get the input data (this would be your JSON matching the schema)
const inputData = $input.all()[0].json;

// Generate the LaTeX resume
const latexResume = generateLatexResume(inputData);

// Return the generated LaTeX content
return {
  json: {
    latex_content: latexResume,
    timestamp: new Date().toISOString(),
    fit_score: inputData.fit_score || 0
  }
};