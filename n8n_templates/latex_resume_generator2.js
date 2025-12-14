// n8n JavaScript Code Node for LaTeX Resume Generation - Business Development Version
// This code takes JSON data and generates a LaTeX resume for business development professionals

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

// Function to generate about me section
function generateAboutMe(aboutMe) {
  if (!aboutMe) {
    return `Passionate Business Development Executive eager to contribute to educational initiatives and student success. Possesses excellent communication and interpersonal skills, committed to building strong relationships with educational partners and driving awareness through engaging field activities.`;
  }
  return escapeLatex(aboutMe);
}

// Function to generate experience section
function generateExperience(experiences) {
  if (!experiences || experiences.length === 0) {
    return `
\\resumeSubheading
{IEMA Research \\& Development Pvt. Ltd.}{March 2024 -- Present}
{Business Development Executive}{Kolkata, West Bengal}
\\resumeItemListStart
\\resumeItem{Responsible for receiving and managing article orders from international clients.}
\\resumeItem{Negotiated pricing, maintained client relationships, and ensured timely publication of content on the website.}
\\resumeItem{Worked closely with cross-functional teams to align business goals and client expectations.}
\\resumeItemListEnd

\\resumeSubheading
{IDBI Capital Markets and Securities Ltd.}{June 2023 -- August 2023}
{Finance Intern}{Kolkata, West Bengal}
\\resumeItemListStart
\\resumeItem{Monitored stock market trends and gained insights into financial markets.}
\\resumeItem{Supported research and analysis by understanding fundamentals of finance.}
\\resumeItem{Assisted senior analysts in preparing financial summaries and client reports.}
\\resumeItemListEnd`;
  }
  
  let experienceSection = '';
  
  experiences.forEach(exp => {
    const title = escapeLatex(exp.title || '');
    const company = escapeLatex(exp.company || '');
    const duration = formatDuration(exp.duration || '');
    const location = escapeLatex(exp.location || 'Kolkata, West Bengal');
    
    experienceSection += `
\\resumeSubheading
{${company}}{${duration}}
{${title}}{${location}}
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

// Function to generate education section
function generateEducation(education) {
  if (!education || education.length === 0) {
    return `
\\resumeSubheading
{Institute of Engineering and Management}{2022 -- 2024}
{Masters of Business Administration in Finance and Marketing}{Kolkata, West Bengal}

\\resumeSubheading
{Institute of Engineering and Management}{2018 -- 2021}
{Bachelor of Business Administration}{Kolkata, West Bengal}`;
  }
  
  let educationSection = '';
  
  education.forEach(edu => {
    const institution = escapeLatex(edu.institution || '');
    const degree = escapeLatex(edu.degree || '');
    const duration = formatDuration(edu.duration || '');
    const location = escapeLatex(edu.location || 'Kolkata, West Bengal');
    
    educationSection += `
\\resumeSubheading
{${institution}}{${duration}}
{${degree}}{${location}}
`;
  });
  
  return educationSection;
}

// Function to generate skills section
function generateSkills(skills) {
  if (!skills || Object.keys(skills).length === 0) {
    return `\\textbf{Technical Tools:} MS Word, MS Excel, Data Management, Presentation Software \\\\
\\textbf{Soft Skills:} Excellent Communication, Interpersonal Skills, Negotiation, Relationship Building, Student Engagement, Critical Thinking, Leadership \\\\
\\textbf{Expertise:} Business Development, Field Sales, Client Relationship Management, Educational Outreach, Event Planning \\& Promotion`;
  }
  
  let skillsSection = '';
  
  if (skills.technical && skills.technical.length > 0) {
    const technicalSkills = skills.technical.map(skill => escapeLatex(skill)).join(', ');
    skillsSection += `\\textbf{Technical Tools:} ${technicalSkills} \\\\`;
  }
  
  if (skills.soft && skills.soft.length > 0) {
    const softSkills = skills.soft.map(skill => escapeLatex(skill)).join(', ');
    skillsSection += `
\\textbf{Soft Skills:} ${softSkills} \\\\`;
  }
  
  if (skills.expertise && skills.expertise.length > 0) {
    const expertiseSkills = skills.expertise.map(skill => escapeLatex(skill)).join(', ');
    skillsSection += `
\\textbf{Expertise:} ${expertiseSkills}`;
  }
  
  return skillsSection || `\\textbf{Technical Tools:} MS Word, MS Excel, Data Management, Presentation Software \\\\
\\textbf{Soft Skills:} Excellent Communication, Interpersonal Skills, Negotiation, Relationship Building, Student Engagement, Critical Thinking, Leadership \\\\
\\textbf{Expertise:} Business Development, Field Sales, Client Relationship Management, Educational Outreach, Event Planning \\& Promotion`;
}

// Function to generate languages section
function generateLanguages(languages) {
  if (!languages || languages.length === 0) {
    return `\\textbf{English:} Professional Proficiency \\\\
\\textbf{Hindi:} Native Proficiency \\\\
\\textbf{Bengali:} Native Proficiency`;
  }
  
  let languagesSection = '';
  
  languages.forEach((lang, index) => {
    const language = escapeLatex(lang.language || '');
    const proficiency = escapeLatex(lang.proficiency || '');
    
    if (index > 0) languagesSection += ' \\\\\\n';
    languagesSection += `\\textbf{${language}:} ${proficiency}`;
  });
  
  return languagesSection;
}

// Function to generate achievements section
function generateAchievements(achievements) {
  if (!achievements || achievements.length === 0) {
    return `\\resumeItem{Demonstrated ability to deliver engaging student demo sessions and organize successful on-ground promotional events.}
\\resumeItem{Proficient in managing outreach data and preparing daily reports to track and analyze field performance.}
\\resumeItem{Highly adaptable to extensive travel and field visits, equipped with a personal 2-wheeler and laptop for efficient independent operations.}
\\resumeItem{Deep passion for the education sector and a commitment to empowering students for a better future.}`;
  }
  
  let achievementsSection = '';
  
  achievements.forEach(achievement => {
    const escapedAchievement = escapeLatex(achievement);
    achievementsSection += `\\resumeItem{${escapedAchievement}}
`;
  });
  
  return achievementsSection.trim();
}

// Main function to generate the complete LaTeX resume
function generateLatexResume(data) {
  const name = escapeLatex(data.name || 'Nilisha Paul');
  const title = escapeLatex(data.job_title || 'Business Development Executive');
  const phone = escapeLatex(data.phone || '8981935726 / 6290748747');
  const email = escapeLatex(data.email || 'nilisha.paul.20@gmail.com');
  const address = escapeLatex(data.address || '41, Dr.C.C.C.Road, Bhadreswar, Hooghly - 712124');
  
  const aboutMeSection = generateAboutMe(data.about_me);
  const experienceSection = generateExperience(data.experience);
  const educationSection = generateEducation(data.education);
  const skillsSection = generateSkills(data.skills);
  const languagesSection = generateLanguages(data.languages);
  const achievementsSection = generateAchievements(data.achievements);
  
  const latexTemplate = `\\documentclass[letterpaper,11pt]{article}

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

\\pagestyle{fancy}
\\fancyhf{}
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Margins
\\addtolength{\\oddsidemargin}{-0.6in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1.19in}
\\addtolength{\\topmargin}{-.7in}
\\addtolength{\\textheight}{1.4in}

\\urlstyle{same}
\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

\\titleformat{\\section}{
  \\vspace{-4pt}\\scshape\\raggedright\\large\\bfseries
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

\\pdfgentounicode=1

% Custom commands
\\newcommand{\\resumeItem}[1]{\\item\\small{{#1 \\vspace{-2pt}}}}
\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
  \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
    \\textbf{#1} & \\textbf{\\small #2} \\\\
    \\textit{\\small#3} & \\textit{\\small #4} \\\\
  \\end{tabular*}\\vspace{-7pt}
}
\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.0in, label={}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{document}

%----------HEADING----------
\\begin{center}
    {\\Huge \\scshape ${name}} \\\\ \\vspace{1pt}
  ${title} \\\\ \\vspace{1pt}
    \\small 
    \\raisebox{-0.1\\height}\\faPhone\\ ${phone} ~ 
    \\href{mailto:${data.email || 'nilisha.paul.20@gmail.com'}}{\\raisebox{-0.2\\height}\\faEnvelope\\  \\underline{${email}}} ~ \\\\
    ${address}
\\end{center}

%-----------ABOUT ME-----------
\\section{About Me}
\\small
${aboutMeSection}

%-----------EXPERIENCE-----------
\\section{Experience}
\\resumeSubHeadingListStart
${experienceSection}
\\resumeSubHeadingListEnd
\\vspace{-14pt}

%-----------EDUCATION-----------
\\section{Education}
\\resumeSubHeadingListStart
${educationSection}
\\resumeSubHeadingListEnd
\\vspace{-14pt}

%-----------SKILLS-----------
\\section{Skills Summary}
\\begin{itemize}[leftmargin=0.15in, label={}]
\\small{\\item{
${skillsSection}
}}
\\end{itemize}
\\vspace{-16pt}

%-----------LANGUAGES-----------
\\section{Languages}
\\begin{itemize}[leftmargin=0.15in, label={}]
\\small{\\item{
${languagesSection}
}}
\\end{itemize}
\\vspace{-16pt}

%-----------ACHIEVEMENTS-----------
\\section{Key Achievements}
\\resumeItemListStart
${achievementsSection}
\\resumeItemListEnd

\\end{document}`;

  return latexTemplate;
}

// n8n execution context
// Assuming the input data comes from previous node as $json

// Get the input data (this would be your JSON matching the business development schema)
const inputData = $input.all()[0].json;

// Generate the LaTeX resume
const latexResume = generateLatexResume(inputData);

// Return the generated LaTeX content
return {
  json: {
    latex_content: latexResume,
    timestamp: new Date().toISOString(),
    candidate_name: inputData.name || 'Nilisha Paul',
    resume_type: 'business_development'
  }
};